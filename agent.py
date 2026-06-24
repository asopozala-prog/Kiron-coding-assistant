# agent.py - Unified agent with all 6 exercises combined

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


# ============================================================================
# TOOLS (Exercises 1-3)
# ============================================================================

def read_file(path: str) -> str:
    """Read the contents of a file at the given path."""
    with open(path) as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    """Write content to a file at the given path."""
    with open(path, "w") as f:
        f.write(content)
    return f"File written: {path}"


def search_files(pattern: str) -> list[str]:
    """Search for files matching a glob pattern."""
    return [str(p) for p in Path(".").glob(pattern)]


def delete_file(path: str) -> str:
    """Delete a file at the given path."""
    os.remove(path)
    return f"File deleted: {path}"


def load_skill(skill_name: str) -> str:
    """Load the instructions for a named skill.
    
    Args:
        skill_name: The filename (without .md) of the skill to load.
    
    Returns:
        The full content of the skill file as a string.
    """
    path = Path("skills") / f"{skill_name}.md"
    if not path.exists():
        return f"Skill '{skill_name}' not found."
    skill = frontmatter.load(path)
    return skill.content


# ============================================================================
# CAPABILITIES (Exercises 3-6)
# ============================================================================

class FileOperations(AbstractCapability[Any]):
    """Exercise 3: File system tools + Exercise 4: Execution hooks"""
    
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
        """Exercise 4: Log tool calls in real time"""
        print(f"→ Calling tool: {call.tool_name}")
        print(f"  Args: {args}")
        return args


class ReasoningEffort(AbstractCapability[Any]):
    """Exercise 5: Dynamic reasoning effort based on task complexity"""
    
    def get_model_settings(self) -> Callable[[RunContext[Any]], ModelSettings]:
        def _set_reasoning_effort(ctx: RunContext[Any]) -> ModelSettings:
            prompt = ctx.prompt or ""
            
            # Simple: short prompts or keywords like "quick", "simple"
            if len(prompt) < 50 or any(
                word in prompt.lower() for word in ["simple", "quick", "short", "list"]
            ):
                effort = "low"
            # Complex: longer prompts or keywords like "explain", "analyse", "debug"
            elif any(
                word in prompt.lower() for word in ["complex", "explain", "analyse", "debug", "why", "how"]
            ):
                effort = "high"
            else:
                effort = "medium"
            
            print(f"[Reasoning effort: {effort}]")
            return ModelSettings(thinking=effort)
        
        return _set_reasoning_effort


class Skills(AbstractCapability[Any]):
    """Exercise 6: Dynamic skill loading from markdown files"""
    
    def get_instructions(self) -> str:
        """Append available skills to system prompt"""
        skills_dir = Path("skills")
        if not skills_dir.exists():
            return ""
        
        lines = ["Available skills (use load_skill() to load one when relevant):\n"]
        for filename in skills_dir.glob("*.md"):
            try:
                skill = frontmatter.load(filename)
                name = skill.metadata.get("name", filename.stem)
                description = skill.metadata.get("description", "No description.")
                lines.append(f"- **{name}**: {description}")
            except Exception as e:
                print(f"Warning: Could not load skill {filename}: {e}")
        
        return "\n".join(lines) if len(lines) > 1 else ""
    
    def get_toolset(self) -> FunctionToolset:
        """Expose load_skill tool"""
        toolset = FunctionToolset()
        toolset.add_function(load_skill)
        return toolset


# ============================================================================
# UNIFIED AGENT (All 6 exercises)
# ============================================================================

agent = Agent(
    model=model,
    instructions="""You are a helpful Python coding assistant with file system access.

You can:
- Read, write, search, and delete files
- Remember previous conversations
- Adjust your reasoning depth based on task complexity
- Load and apply specialized skills when needed

Always be clear about what you're doing and ask for confirmation before deleting files.""",
    capabilities=[FileOperations(), ReasoningEffort(), Skills()],
)


# ============================================================================
# INTERACTIVE LOOP (Exercise 2: Conversation state)
# ============================================================================

async def main():
    """Run the agent in interactive mode with conversation history"""
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
