from fastapi import FastAPI, Depends, HTTPException, status


app = FastAPI()


@app.get("/Welcome to safe your life", tags=["get to know"])
async def Cyber():
    return {"Welcome to everyone"}
