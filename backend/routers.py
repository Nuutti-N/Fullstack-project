
from google import genai
from google.genai.types import GenerateContentConfig
from backend.supabase_client import supabase
from backend.users import get_current_user
from fastapi import HTTPException, APIRouter, Depends, Request, Query, Body, Path
from backend.config import settings
from backend.logger import logger
from backend.rate_limiter import limiter
import json

router = APIRouter()
client = genai.Client(api_key=settings.gemini_api_key)


@router.get("/welcome", tags=["welcome"])
async def welcome():
    logger.info("Welcome_endpoint_called")
    return {"message": "Welcome to the AI Agent"}


@router.post("/chat", tags=["verify"])
@limiter.limit("5/minute")
async def verify_text(request: Request, user_message: str = Body(min_length=1, max_length=2000), current_user=Depends(get_current_user)):
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
async def verify_fact(request: Request, text: str = Body(min_length=5, max_length=2000), current_user=Depends(get_current_user)):
    try:
        logger.info("Fact check requested by user user_id=%s claim=%s",
                    current_user.id, text[:50])
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=text,
            config=GenerateContentConfig(
                response_mime_type="application/json",
                system_instruction=[
                    """You are a AI generated evaluator. Your job is to analyze AI generate text or code and determine if it is safe to trust and use. Your task to identify any misleading, outdated or harmful content.\n\n Give a trust score from 0 to 100 to use ai generated text or code, and give for me information where is the probably mistakes and what is good.
                 Return your response as Json only, no other text, with exactly these fields:
                 "trust_score": <number 0-100>,
                 "verdict": <can use|let's explore more|do not use>,
                 "risks": "[<risk>, <risk>]",
                 "pros": "[<pros>, <pros>]",
                 "recommend": "<what the user should do>"""
                ])
        )

        data = json.loads(response.text.strip())
        logger.info("Fact check result for user user_id=%s trust_score=%s verdict=%s risks=%s pros=%s recommend=%s",
                    current_user.id, data["trust_score"], data["verdict"], data["risks"], data["pros"], data["recommend"])

        supabase.table("fact_checks").insert({
            "user_id": current_user.id,
            "claim": text,
            "trust_score": data["trust_score"],
            "verdict": data["verdict"],
            "risks": data["risks"],
            "pros": data["pros"],
            "recommend": data["recommend"]
        }).execute()

        return {
            "claim": text,
            "score": data["trust_score"],
            "verdict": data["verdict"],
            "risks": data["risks"],
            "pros": data["pros"],
            "recommend": data["recommend"],
        }
    except json.JSONDecodeError as e:
        logger.error("analyze_error_json user_id=%s error=%s",
                     current_user.id, e, exc_info=True)
        raise HTTPException(
            status_code=500, detail="Bad requests, invalid JSON")
    except Exception as e:
        logger.error("fact_chat_error user_id=%s error=%s",
                     current_user.id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history", tags=["verify"])
async def get_my_facts(current_user=Depends(get_current_user), limit: int = Query(20, ge=0), offset: int = Query(0, ge=0)):
    try:
        logger.info("History_check_requested_user user_id=%s", current_user.id)
        data = supabase.table("fact_checks").select(
            "*").eq("user_id", current_user.id).range(offset, offset + limit - 1).execute()
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
            "delete_history_unexpected_response user_id=%s fact_id=%s", current_user.id, fact_id)
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
    except HTTPException:
        raise
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
