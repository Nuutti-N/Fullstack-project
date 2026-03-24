from fastapi import FastAPI, Depends, HTTPException, status


app = FastAPI()


@app.get("/Welcome", tags=["Welcome"])
async def Cyber():
    return {"Welcome to everyone"}
