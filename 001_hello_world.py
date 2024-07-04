from fastapi import FastAPI
import os

user_name = os.environ["GITHUB_USER"]
app = FastAPI()

@app.get("/")
async def root():
    return {"message": f"hello world! user: {user_name} "}