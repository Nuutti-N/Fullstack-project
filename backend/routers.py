
from google import genai
from backend.supabase_client import supabase
from backend.users import get_current_user
from fastapi import HTTPException, APIRouter, Depends, status
from backend.config import settings
from backend.logger import logger

router = APIRouter()
client = genai.Client(api_key=settings.gemini_api_key)


@router.get("/Welcome", tags=["Welcome"])
async def Welcome():
    logger.info("Welcome_endpoint_called")
    return {"message": "Welcome to the AI Agent"}


@router.post("/chat", tags=["Verify"])
async def verify_text(user_message: str, current_user=Depends(get_current_user)):
    try:
        logger.info("chat_request user_id=%s message_len=%s",
                    current_user.id, len(user_message))
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_message
        )
        return {"AI explain":  response.text}
    except Exception as e:
        logger.error("chat_error user_id=%s error=%s",
                     current_user.id, e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat-fact", tags=["Verify"])
async def verify_fact(claim: str, current_user=Depends(get_current_user)):
    try:
        logger.info(
            f"Fact check requested by user {current_user.id}: {claim[:50]}")
        prompt = f"Is this statement true or false? {claim}\n\nRespond with only one word: True, False, or Unclear. Nothing else."

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        results = response.text.strip().upper()
        logger.info("Fact check result for user user_id=%s status=%s",
                    current_user.id, results)

        supabase.table("fact_checks").insert({
            "user_id": current_user.id,
            "claim": claim,
            "answer": results
        }).execute()

        return {
            "claim": claim,
            "is_true": results == "TRUE",
            "status": results
        }
    except Exception as e:
        logger.error("fact_chat_error user_id=%s error=%s",
                     current_user.id, e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/History", tags=["Verify"])
async def get_my_facts(current_user=Depends(get_current_user)):
    try:
        data = supabase.table("fact_checks").select(
            "*").eq("user_id", current_user.id).execute()
        logger.info(
            "history_request user_id=%s items=%s", current_user.id, len(data.data or []))
        return data.data
    except Exception as e:
        logger.error("history_check_error user_id=%s error=%s",
                     current_user.id, e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_history/{fact_id}", tags=["Verify"])
async def delete_my_facts(fact_id: int, current_user=Depends(get_current_user)):
    logger.info(
        "delete_history_unexcpected_response user_id=%s fact_id=%s", current_user.id)
    data = supabase.table("fact_checks").delete().eq(
        "id", fact_id).eq("user_id", current_user.id).execute()
    if data.data is None:
        raise HTTPException(
            status_code=500, detail="Unexpected response from database")
    if data.data == []:

        raise HTTPException(status_code=404, detail="no matching history item")
    return {"deleted": True}


@router.delete("/delete_all_history/", tags=["Verify"])
async def delet_all_facts(current_user=Depends(get_current_user)):
    try:
        data = supabase.table("fact_checks").delete().eq(
            "user_id", current_user.id).execute()
        return {"deleted": "All history deleted"}
    except Exception as e:  # If any other error happens, store it in 'e'
        # Send 500 error with the error message
        raise HTTPException(status_code=500, detail=str(e))
