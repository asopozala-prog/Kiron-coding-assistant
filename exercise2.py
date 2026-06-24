import asyncio
from dotenv import load_dotenv
import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

load_dotenv()

provider = GoogleProvider(api_key=os.getenv("GEMINI_API_KEY"))
model = GoogleModel("gemini-2.5-flash", provider=provider)


agent = Agent(
    model=model,
    instructions="You are a helpful Python coding assistant.",
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
