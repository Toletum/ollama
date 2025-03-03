from phi.agent import Agent
from phi.model.openai import OpenAIChat


model = OpenAIChat(base_url="http://localhost:11434/v1",
                     api_key='ollama',
                     id="qwen2.5-coder:1.5b")

agente = Agent(
    name="Programmer IA",
    model=model,
    instructions=["You are a programmer in python."],
    show_tool_calls=True,
    markdown=True,
    stream=True
)

agente.print_response("Fibonacci in python?", markdown=True)
