import asyncio
from dotenv import load_dotenv
import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.toolsets import FunctionToolset
from pydantic_ai.tools import RunContext, ToolCallPart, ToolDefinition
from typing import Any

load_dotenv()

provider = GoogleProvider(api_key=os.getenv("GEMINI_API_KEY"))
model = GoogleModel("gemini-2.5-flash", provider=provider)


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
    from pathlib import Path
    return [str(p) for p in Path(".").glob(pattern)]


def delete_file(path: str) -> str:
    """Delete a file at the given path."""
    os.remove(path)
    return f"File deleted: {path}"


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
        print(f"→ Calling tool: {call.tool_name}")
        print(f"  Args: {args}")
        return args


agent = Agent(
    model=model,
    instructions="You are a helpful Python coding assistant with file system access.",
    capabilities=[FileOperations()],
)


async def main():
    history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = await agent.run(user_input, message_history=history)
        history = result.all_messages()
        print(f"Assistant: {result.output}\n")

asyncio.run(main())
