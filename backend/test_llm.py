from agent.llm import get_llm

llm = get_llm()

response = llm.invoke("Who are you? Answer in one sentence.")

print(response.content)