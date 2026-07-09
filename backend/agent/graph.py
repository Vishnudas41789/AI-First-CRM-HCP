from datetime import date, datetime

from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.llm import get_llm
from agent.prompts import SYSTEM_PROMPT
from agent.tools import TOOLS

from database.database import SessionLocal
from models.interaction import Interaction

llm = get_llm()
llm_with_tools = llm.bind_tools(TOOLS)

TOOL_MAP = {t.name: t for t in TOOLS}


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def _parse_date(value):
    if not value:
        return date.today()
    value = str(value).strip().lower()
    if value in ("today", ""):
        return date.today()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return date.today()


def _parse_time(value):
    if not value:
        return datetime.now().time()
    value = str(value).strip()
    for fmt in ("%H:%M:%S", "%H:%M", "%I:%M %p", "%I:%M:%S %p"):
        try:
            return datetime.strptime(value, fmt).time()
        except ValueError:
            continue
    return datetime.now().time()


def _interaction_to_dict(row: Interaction):
    return {
        "id": row.id,
        "hcp_name": row.hcp_name,
        "interaction_type": row.interaction_type,
        "interaction_date": str(row.interaction_date) if row.interaction_date else None,
        "interaction_time": str(row.interaction_time) if row.interaction_time else None,
        "attendees": row.attendees,
        "topics_discussed": row.topics_discussed,
        "materials_shared": row.materials_shared,
        "samples_distributed": row.samples_distributed,
        "sentiment": row.sentiment,
        "outcome": row.outcome,
        "follow_up_actions": row.follow_up_actions,
    }


def _save_log_interaction(data: dict):
    db = SessionLocal()
    try:
        row = Interaction(
            hcp_name=data.get("hcp_name") or "Unknown",
            interaction_type=data.get("interaction_type") or "Meeting",
            interaction_date=_parse_date(data.get("interaction_date")),
            interaction_time=_parse_time(data.get("interaction_time")),
            attendees=data.get("attendees"),
            topics_discussed=data.get("discussion") or data.get("products_discussed"),
            materials_shared=data.get("materials_shared"),
            samples_distributed=data.get("samples_shared"),
            sentiment=data.get("sentiment"),
            outcome=data.get("outcome"),
            follow_up_actions=data.get("follow_up"),
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return _interaction_to_dict(row)
    finally:
        db.close()


def _apply_edit(field_name: str, new_value: str):
    field_map = {
        "hcp_name": "hcp_name",
        "interaction_type": "interaction_type",
        "sentiment": "sentiment",
        "outcome": "outcome",
        "attendees": "attendees",
        "discussion": "topics_discussed",
        "topics_discussed": "topics_discussed",
        "materials_shared": "materials_shared",
        "samples_shared": "samples_distributed",
        "samples_distributed": "samples_distributed",
        "follow_up": "follow_up_actions",
        "follow_up_actions": "follow_up_actions",
    }
    column = field_map.get(field_name, field_name)

    db = SessionLocal()
    try:
        row = db.query(Interaction).order_by(Interaction.id.desc()).first()
        if not row:
            return {"error": "No interaction found to edit."}
        if hasattr(row, column):
            setattr(row, column, new_value)
            db.commit()
            db.refresh(row)
            return _interaction_to_dict(row)
        return {"error": f"Unknown field '{field_name}'."}
    finally:
        db.close()


# ---------------------------------------------------------
# LangGraph nodes
# ---------------------------------------------------------

def agent_node(state: AgentState):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": state["user_message"]},
    ]

    response = llm_with_tools.invoke(messages)

    state["_llm_message"] = response

    # Save normal AI responses immediately
    if not getattr(response, "tool_calls", None):
        state["ai_response"] = response.content

    return state


def route_after_agent(state: AgentState):
    message = state["_llm_message"]

    if getattr(message, "tool_calls", None):
        return "execute_tools"

    return "end"


def execute_tools_node(state: AgentState):
    message = state["_llm_message"]
    tool_call = message.tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call.get("args", {})

    state["selected_tool"] = tool_name
    tool_fn = TOOL_MAP.get(tool_name)

    if tool_fn is None:
        state["error"] = f"Unknown tool: {tool_name}"
        state["ai_response"] = "Sorry, I couldn't process that request."
        return state

    result = tool_fn.invoke(tool_args)

    # ---------------------------------------------------------
    # Log Interaction
    # ---------------------------------------------------------
    if tool_name == "log_interaction":
        db_row = _save_log_interaction(result)

        state["database_result"] = db_row
        state["interaction_data"] = result
        state["ai_response"] = f"""
        ✅ Interaction Logged Successfully!

        The interaction has been saved successfully.

        HCP Name: {result.get("hcp_name")}
        Interaction Type: {result.get("interaction_type")}
        Date: {result.get("interaction_date")}
        Time: {result.get("interaction_time")}
        Discussion: {result.get("discussion") or result.get("products_discussed")}
        Sentiment: {result.get("sentiment")}
        Materials Shared: {result.get("materials_shared")}

        Would you like to edit this interaction or generate a follow-up action?
        """

    # ---------------------------------------------------------
    # Edit Interaction
    # ---------------------------------------------------------
    elif tool_name == "edit_interaction":
        db_row = _apply_edit(result["field_name"], result["new_value"])

        state["database_result"] = db_row
        state["interaction_data"] = {
            result["field_name"]: result["new_value"]
        }

        state["ai_response"] = f"""
        ✅ Interaction Updated Successfully!

        Updated Field:
        {result["field_name"].replace("_", " ").title()}

        New Value:
        {result["new_value"]}

        The interaction has been updated successfully.
        """

    # ---------------------------------------------------------
    # Summarize Interaction
    # ---------------------------------------------------------
    elif tool_name == "summarize_interaction":
        state["interaction_data"] = result

        discussion = result.get("discussion") or "No discussion available."

        state["ai_response"] = (
            f"Summary:\n\n{discussion}"
        )

    # ---------------------------------------------------------
    # Suggest Follow-up
    # ---------------------------------------------------------
    elif tool_name == "suggest_followup":
        state["interaction_data"] = result

        discussion = result.get("discussion") or ""
        sentiment = (result.get("sentiment") or "").lower()

        if sentiment == "negative":
            state["ai_response"] = (
                "Suggested Follow-up:\n\n"
                "- Schedule another meeting.\n"
                "- Address the doctor's concerns.\n"
                "- Share additional clinical evidence."
            )

        elif sentiment == "positive":
            state["ai_response"] = (
                "Suggested Follow-up:\n\n"
                "- Share additional product information.\n"
                "- Schedule the next visit.\n"
                "- Continue engagement."
            )

        else:
            state["ai_response"] = (
                f"Suggested Follow-up:\n\n"
                f"Review the discussion and plan the next meeting.\n\n"
                f"Discussion: {discussion}"
            )

    # ---------------------------------------------------------
    # Next Best Action
    # ---------------------------------------------------------
    elif tool_name == "next_best_action":
        state["interaction_data"] = result

        discussion = result.get("discussion") or ""
        outcome = result.get("outcome") or ""

        state["ai_response"] = (
            "Next Best Action:\n\n"
            f"• Follow up regarding: {discussion}\n"
            f"• Target outcome: {outcome}\n"
            "• Schedule the next HCP visit.\n"
            "• Share supporting product information."
        )

    # ---------------------------------------------------------
    # Default
    # ---------------------------------------------------------
    else:
        state["interaction_data"] = result
        state["ai_response"] = "Task completed successfully."

    return state


# ---------------------------------------------------------
# Build graph
# ---------------------------------------------------------

builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("execute_tools", execute_tools_node)

builder.set_entry_point("agent")

builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "execute_tools": "execute_tools",
        "end": END,
    },
)

builder.add_edge("execute_tools", END)

graph = builder.compile()