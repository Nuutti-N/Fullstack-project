from fastapi import FastAPI, HTTPException, APIRouter


router = APIRouter()


@router.get
@router.get("/Welcome", tags=["Welcome"])
async def Welcome():
    return {"Welcome to everyone"}
