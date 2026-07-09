from agent.graph import graph


def process_chat(user_message: str):
    initial_state = {
        "user_message": user_message,
        "selected_tool": None,
        "ai_response": "",
        "interaction_data": {},
        "conversation_history": [],
        "database_result": None,
        "error": None,
    }

    result = graph.invoke(initial_state)

    print("\n================ RESULT ================\n")
    print(result)
    print("\n========================================\n")

    return {
        "success": True,
        "user_message": result.get("user_message"),
        "selected_tool": result.get("selected_tool"),
        "ai_response": result.get("ai_response"),
        "interaction_data": result.get("interaction_data"),
        "database_result": result.get("database_result"),
        "error": result.get("error"),
    }