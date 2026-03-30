from google import genai
from supabase_client import supabase
from users import get_current_user
from fastapi import FastAPI, HTTPException, APIRouter, Depends
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@router.get("/Welcome", tags=["Welcome"])
async def Welcome():
    return {"message": "Welcome to everyone"}


@router.post("/chat", tags=["Verify"])
async def verify_text(user_message: str, current_user=Depends(get_current_user)):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_message
    )
    return {"AI explain":  response.text}


@router.post("/chat-fact", tags=["Verify"])
async def verify_fact(claim: str, current_user=Depends(get_current_user)):
    prompt = f"Is this statement true or false? {claim}\n\nRespond with only one word: True, False, or Unclear. Nothing else."

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    results = response.text.strip().upper()

    supabase.table("fact_checks").insert({
        "user_id": current_user.id,
        "claim": claim,
        "answer": results
    }).execute()

    return {
        "claim": claim,
        "is_true": results == "True",
        "status": results
    }


@router.get("/History", tags=["Verify"])
async def get_my_facts(current_user=Depends(get_current_user)):
    data = supabase.table("fact_checks").select(
        "*").eq("user_id", current_user.id).execute()
    return data.data


@router.delete("/my_facts/{fact_id}", tags=["Verify"])
async def delete_my_facts(fact_id: int, current_user=Depends(get_current_user)):
    try:
        data = supabase.table("fact_checks").delete().eq(
            "id", fact_id).eq("user_id", current_user.id).execute()
        return {"deleted": True}
    except Exception as e:
