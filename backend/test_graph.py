from agent.graph import graph

result = graph.invoke({
    "user_message": "Today I met Dr. Smith and discussed Product X efficiency. The sentiment was positive and I shared brochures.",
    "selected_tool": None,
    "ai_response": None,
    "interaction_data": {},
    "conversation_history": [],
    "database_result": None,
    "error": None,
})

print(result)