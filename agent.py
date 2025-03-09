from agno.agent import Agent
from agno.models.ollama import Ollama


#model = OpenAIChat(base_url="http://localhost:11434/v1",
#                     api_key='ollama',
#                     id="qwen2.5-coder:latest")


model = Ollama(host="localhost:11434",
               id="qwen2.5-coder:3b")

agente = Agent(
    name="Programmer IA",
    model=model,
    instructions=["You are a programmer in python. Only reply code"],
    show_tool_calls=True
)

agente.print_response("Create only one Fibonacci function?", markdown=True, stream=True)
