
from google import genai
from backend.supabase_client import supabase
from backend.users import get_current_user
from fastapi import HTTPException, APIRouter, Depends, status, Request, Query, Path
from backend.config import settings
from backend.logger import logger
from backend.rating_limiter import limiter
import json

router = APIRouter()
client = genai.Client(api_key=settings.gemini_api_key)


@router.get("/welcome", tags=["welcome"])
async def Welcome():
    logger.info("Welcome_endpoint_called")
    return {"message": "Welcome to the AI Agent"}


@router.post("/chat", tags=["verify"])
async def verify_text(user_message: str = Query(min_length=1, max_length=2000), current_user=Depends(get_current_user)):
    try:
        logger.info("chat_request user_id=%s message_len=%s",
                    current_user.id, len(user_message))
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_message
        )
        logger.info("chat_request_succees user_id=%s message_len=%s",
                    current_user.id, len(response.text or ""))
        return {"AI explain":  response.text}
    except Exception as e:
        logger.error("chat_error user_id=%s error=%s",
                     current_user.id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/analyze", tags=["verify"])
@limiter.limit("5/minute")
async def verify_fact(request: Request, text: str = Query(min_length=5, max_length=2000), current_user=Depends(get_current_user)):
    try:
        logger.info(
            f"Fact check requested by user {current_user.id}: {text[:50]}")
        prompt = f"""You are a AI generated evaluator. Your job is to analyze AI generate text or code and determine if it is safe to trust and use. Your task to identify any misleading, outdated or harmful content.\n\n Give a trust scofe from 0 to 100 to use ai generated text or code, and give for me information where is the propably mistakes and what is good.
        Analyze this text:
        {text}
        
        Return your response as Json only, no other text, with exacty these fields:
        {{
            "trust_score": <number 0-100>,
            "verdict": <can use|let's explore more|do not use>,
            "risks": "[<risk>, <risk>]",
            "pros": "[<pros>, <pros>]",
            "recommend": "<what the user should do>",
        }}
        """
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        data = json.loads(response.text.strip())
        logger.info("Fact check result for user user_id=%s status=%s",
                    current_user.id, data["verdict"])

        supabase.table("fact_checks").insert({
            "user_id": current_user.id,
            "claim": text,
            "answer": data["verdict"]
        }).execute()

        return {
            "claim": text,
            "score": data["trust_score"],
            "verdict": data["verdict"],
            "risks": data["risks"],
            "pros": data["pros"],
            "recommend": data["recommend"],
        }
    except Exception as e:
        logger.error("fact_chat_error user_id=%s error=%s",
                     current_user.id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history", tags=["verify"])
async def get_my_facts(current_user=Depends(get_current_user)):
    try:
        logger.info("History_check_requested_user user_id=%s", current_user.id)
        data = supabase.table("fact_checks").select(
            "*").eq("user_id", current_user.id).execute()
        logger.info(
            "history_request user_id=%s items=%s", current_user.id, len(data.data or []))
        return data.data
    except Exception as e:
        logger.error("history_check_error user_id=%s error=%s",
                     current_user.id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/delete_history/{fact_id}", tags=["verify"])
async def delete_my_facts(fact_id: int = Path(ge=1), current_user=Depends(get_current_user)):
    try:
        logger.info(
            "delete_history_unexcpected_response user_id=%s fact_id=%s", current_user.id, fact_id)
        data = supabase.table("fact_checks").delete().eq(
            "id", fact_id).eq("user_id", current_user.id).execute()
        if data.data is None:
            logger.error("delete_history_error user_id=%s error=%s",
                         current_user.id, fact_id)
            raise HTTPException(
                status_code=500, detail="Unexpected response from database")
        if data.data == []:
            logger.warning(
                "delete_history_error user_id=%s fact_id=%s", current_user.id, fact_id)
            raise HTTPException(
                status_code=404, detail="no matching history item")
        logger.info("delete_history_success user_id=%s fact_id=%s",
                    current_user.id, fact_id)
        return {"deleted": True}
    except Exception as e:
        logger.error(
            "delete_history_error user_id=%s fact_id=%s error=%s", current_user.id, fact_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/delete_all_history/", tags=["verify"])
async def delete_all_facts(current_user=Depends(get_current_user)):
    try:
        logger.info("delete_all_history_requestes user_id=%s", current_user.id)
        data = supabase.table("fact_checks").delete().eq(
            "user_id", current_user.id).execute()
        logger.info("delete_all_history_succees user_id=%s", current_user.id)
        return {"deleted": "All history deleted"}
    except Exception as e:  # If any other error happens, store it in 'e'
        # Send 500 error with the error message
        logger.error("delete_all_history_error user_id=%s error=%s",
                     current_user.id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
