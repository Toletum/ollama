from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo


model = OpenAIChat(base_url="http://localhost:11434/v1",
                   api_key='ollama',
                   model='llama3.2:latest')


agente = Agent(
    name="Intelligent Assistant",
    model=model,
    instructions=["You are an intelligent assistant designed to answer questions using the provided tools. When asked a question that requires up-to-date information, use the duckduckgo_search tool to find relevant information from the web. After getting the search results, summarize the answer to the user's question based on the information found."],
    tools=[DuckDuckGo()],
    show_tool_calls=True
)

agente.print_response("who is the current POTUS?", markdown=True)
