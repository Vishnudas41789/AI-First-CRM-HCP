from datetime import datetime
from typing import Optional

from langchain_core.tools import tool


@tool
def log_interaction(
    hcp_name: Optional[str] = None,
    interaction_date: Optional[str] = None,
    interaction_time: Optional[str] = None,
    interaction_type: Optional[str] = None,
    attendees: Optional[str] = None,
    products_discussed: Optional[str] = None,
    discussion: Optional[str] = None,
    sentiment: Optional[str] = None,
    materials_shared: Optional[str] = None,
    samples_shared: Optional[str] = None,
    outcome: Optional[str] = None,
    follow_up: Optional[str] = None,
):
    """
    Log a new HCP interaction.
    """

    return {
        "tool": "log_interaction",
        "hcp_name": hcp_name,
        "interaction_date": interaction_date,
        "interaction_time": interaction_time,
        "interaction_type": interaction_type,
        "attendees": attendees,
        "products_discussed": products_discussed,
        "discussion": discussion,
        "sentiment": sentiment,
        "materials_shared": materials_shared,
        "samples_shared": samples_shared,
        "outcome": outcome,
        "follow_up": follow_up,
        "created_at": datetime.now().isoformat(),
    }


@tool
def edit_interaction(
    field_name: str,
    new_value: str,
):
    """
    Edit an existing interaction field.
    """

    return {
        "tool": "edit_interaction",
        "field_name": field_name,
        "new_value": new_value,
    }


@tool
def summarize_interaction(
    discussion: str,
):
    """
    Generate a short summary of the discussion.
    """

    return {
        "tool": "summarize_interaction",
        "discussion": discussion,
    }


@tool
def suggest_followup(
    discussion: Optional[str] = None,
    sentiment: Optional[str] = None,
):
    """
    Suggest follow-up actions.
    """

    return {
        "tool": "suggest_followup",
        "discussion": discussion,
        "sentiment": sentiment,
    }


@tool
def next_best_action(
    discussion: Optional[str] = None,
    outcome: Optional[str] = None,
):
    """
    Recommend the next sales action.
    """

    return {
        "tool": "next_best_action",
        "discussion": discussion,
        "outcome": outcome,
    }


TOOLS = [
    log_interaction,
    edit_interaction,
    summarize_interaction,
    suggest_followup,
    next_best_action,
]