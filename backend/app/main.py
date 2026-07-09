from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.interaction import router as interaction_router

from database.database import Base
from database.database import engine

from models.interaction import Interaction

app = FastAPI(
    title="AI First CRM",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interaction_router)
@app.get("/")
def home():

    return {
        "message": "AI First CRM Backend Running Successfully 🚀"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }