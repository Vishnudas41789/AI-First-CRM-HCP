from fastapi import APIRouter
from fastapi import HTTPException

from services.interaction_service import process_chat

router = APIRouter(
    prefix="/interaction",
    tags=["Interaction AI"],
)


@router.post("/chat")
async def chat(message: dict):

    try:
        if "message" not in message:
            raise HTTPException(
                status_code=400,
                detail="message field is required."
            )

        response = process_chat(message["message"])

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )