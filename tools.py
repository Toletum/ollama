from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools


#model = OpenAIChat(base_url="http://localhost:11434/v1",
#                     api_key='ollama',
#                     id="qwen2.5:latest")


model = Ollama(host="localhost:11434",
               id="qwen2.5:latest")


agente = Agent(
    name="Intelligent Assistant",
    model=model,
    instructions=["You are an intelligent assistant designed to answer questions using the provided tools. When asked a question that requires up-to-date information, use the duckduckgo_search tool to find relevant information from the web. After getting the search results, summarize the answer to the user's question based on the information found."],
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True
)

agente.print_response("who is the current POTUS?", markdown=True, stream=True)
