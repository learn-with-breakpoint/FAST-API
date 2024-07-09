from fastapi import FastAPI
import os
from fastapi.params import Body

user_name = os.environ["GITHUB_USER"]
app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"hello world! user: {user_name} "}


@app.get("/posts")
def posts():
    return {"this is your first post"}


@app.post("/createposts")
def create_posts(payload: dict = Body()):
    return f"Title {payload['title']} | context: {payload['context']}"
