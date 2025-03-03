import openai

client = openai.OpenAI(base_url="http://localhost:11434/v1", api_key='ollama')

response = client.chat.completions.create(
    model="qwen2.5-coder:1.5b",
    messages=[{"role": "user", "content": "python fibonacci?"}]
)

print(response.choices[0].message.content)
