from google import genai
from fastapi import HTTPException, APIRouter
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@router.get("/Welcome", tags=["Welcome"])
async def Welcome():
    return {"message": "Welcome to everyone"}


@router.post("/chat", tags=["Verify"])
async def verify_text(user_message: str):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_message
    )
    return {"AI explain":  response.text}


@router.post("/chat-fact", tags=["Verify"])
async def verify_fact(claim: str):
