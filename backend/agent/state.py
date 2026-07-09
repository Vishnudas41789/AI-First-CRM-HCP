from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    user_message: str

    selected_tool: Optional[str]

    ai_response: Optional[str]

    interaction_data: Dict[str, Any]

    conversation_history: List[Dict[str, str]]

    database_result: Optional[Dict[str, Any]]

    error: Optional[str]

    # Internal LangGraph state
    _llm_message: Any