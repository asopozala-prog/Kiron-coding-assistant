import asyncio
from dotenv import load_dotenv
import os
from pathlib import Path
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.toolsets import FunctionToolset
from pydantic_ai.tools import RunContext, ToolCallPart, ToolDefinition
from pydantic_ai.settings import ModelSettings
from typing import Any, Callable
import frontmatter

load_dotenv()

provider = GoogleProvider(api_key=os.getenv("GEMINI_API_KEY"))
model = GoogleModel("gemini-2.5-flash", provider=provider)

WORK_DIR = Path(__file__).parent / "legal_files" / "work_files"

FILE_ALIASES = {
    "messy case data": "messy_case_data.txt",
    "messy data": "messy_case_data.txt",
    "case data": "messy_case_data.txt",
    "messy": "messy_case_data.txt",
    "template": "case_file_template.txt",
    "case file": "case_file_template.txt",
    "case template": "case_file_template.txt",
    "sample contract": "sample_contract.md",
    "contract": "sample_contract.md",
    "sample": "sample_contract.md",
}

PROTECTED_FILES = {
    "alex.md",
    "case_file_template.txt",
    "messy_case_data.txt",
    "sample_contract.md",
}


def resolve_filename(user_mention: str) -> str:
    text = user_mention.lower().strip()

    if text in FILE_ALIASES:
        return FILE_ALIASES[text]

    for alias, filename in FILE_ALIASES.items():
        if alias in text:
            return filename

    return user_mention


def find_best_match(query: str) -> str | None:
    """Find the best matching file in work_files by keyword similarity."""
    query = query.lower().strip()
    words = [w for w in query.replace("_", " ").split() if len(w) > 2]

    if not words:
        return None

    candidates = []
    for path in WORK_DIR.iterdir():
        if not path.is_file():
            continue

        name = path.name.lower()
        score = sum(1 for word in words if word in name)

        if score > 0:
            candidates.append((score, path.name))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]


def _safe_path(filename: str) -> Path:
    filename = filename.replace("\\", "/").strip()
    filename = os.path.basename(filename)
    path = (WORK_DIR / filename).resolve()
    work_root = WORK_DIR.resolve()

    if work_root not in path.parents and path != work_root:
        raise ValueError("Access denied. Files must stay inside work_files.")
    return path


def read_file(filename: str) -> str:
    """Read the contents of a file in work_files."""
    actual_filename = resolve_filename(filename)
    
    if actual_filename == filename:
        best = find_best_match(filename)
        if best:
            actual_filename = best
    
    file_path = _safe_path(actual_filename)

    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: File '{actual_filename}' not found."
    except Exception as e:
        return f"Error reading file '{actual_filename}': {e}"


def write_file(filename: str, content: str) -> str:
    """Write content to a file in work_files."""
    actual_filename = resolve_filename(filename)
    
    if actual_filename == filename:
        best = find_best_match(filename)
        if best:
            actual_filename = best
    
    file_path = _safe_path(actual_filename)

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"File written: {actual_filename}"
    except Exception as e:
        return f"Error writing file '{actual_filename}': {e}"


def search_files(pattern: str) -> list[str]:
    """Search for files in work_files."""
    pattern = pattern.strip()
    matches = []
    for p in WORK_DIR.glob(pattern):
        if p.is_file():
            matches.append(p.name)
    return sorted(matches)


def delete_file(filename: str) -> str:
    """Delete a file in work_files."""
    actual_filename = resolve_filename(filename)

    if actual_filename == filename:
        best = find_best_match(filename)
        if best:
            actual_filename = best

    if actual_filename in PROTECTED_FILES:
        return (
            "Hey Alex, this file is your working base‼️ 🦕\n"
            "If you really want to delete it, please contact our programmer."
        )

    file_path = _safe_path(actual_filename)

    try:
        file_path.unlink()
        return f"File deleted: {actual_filename}"
    except FileNotFoundError:
        return f"Error: File '{actual_filename}' not found."
    except Exception as e:
        return f"Error deleting file '{actual_filename}': {e}"


def load_skill(skill_name: str) -> str:
    """Load a skill from skills/."""
    path = Path("skills") / f"{skill_name}.md"
    if not path.exists():
        return f"Skill '{skill_name}' not found."
    skill = frontmatter.load(path)
    return skill.content


class FileOperations(AbstractCapability[Any]):
    def get_toolset(self) -> FunctionToolset:
        toolset = FunctionToolset()
        toolset.add_function(read_file)
        toolset.add_function(write_file)
        toolset.add_function(search_files)
        toolset.add_function(delete_file)
        return toolset

    async def before_tool_execute(
        self,
        ctx: RunContext[Any],
        *,
        call: ToolCallPart,
        tool_def: ToolDefinition,
        args: dict[str, Any],
    ) -> dict[str, Any]:
        print(f"-> Calling tool: {call.tool_name}")
        print(f"   Args: {args}")
        return args


class Skills(AbstractCapability[Any]):
    def get_instructions(self, ctx: RunContext[Any] | None = None) -> str:
        skills_dir = Path("skills")
        if not skills_dir.exists():
            return ""

        lines = [
            "Available skills: use load_skill(skill_name) when relevant. "
            "Loaded skills should guide how you work.\n"
        ]

        for filename in skills_dir.glob("*.md"):
            try:
                skill = frontmatter.load(filename)
                name = skill.metadata.get("name", filename.stem)
                description = skill.metadata.get("description", "No description.")
                lines.append(f"- {name}: {description}")
            except Exception as e:
                print(f"Warning: Could not load skill {filename}: {e}")

        return "\n".join(lines)

    def get_toolset(self) -> FunctionToolset:
        toolset = FunctionToolset()
        toolset.add_function(load_skill)
        return toolset


agent = Agent(
    model=model,
    instructions="""You are Kiron, a helpful legal document assistant for Alex.

Alex works in a legal office and uses you to handle confidential files locally.

CRITICAL: When Alex mentions a file, ALWAYS call the file tool immediately.
Do not ask for clarification. The tools will resolve the filename.

Examples:
- "read messy case data" → call read_file("messy case data")
- "create case template" → call write_file("case template", ...)
- "delete sample contract" → call delete_file("sample contract")

Rules:
- Use the work_files folder as the default workspace.
- Call file tools with whatever name Alex uses.
- The tools will map it to the correct file.
- Never ask "what is the exact filename?"
- You may create, read, and edit files in the working folder.
- Do not delete protected core files such as alex.md, case_file_template.txt, messy_case_data.txt, or sample_contract.md.
- You may delete only new demo-created files.
- Be direct and action-oriented.
- Keep the tone friendly, clear, and practical.""",
    capabilities=[FileOperations(), Skills()],
)


async def main():
    history = []
    print("🦕 Kiron Coding Assistant")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            result = await agent.run(user_input, message_history=history)
            history = result.all_messages()
            print(f"Assistant: {result.output}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")


if __name__ == "__main__":
    asyncio.run(main())