from fastapi import FastAPI
import os

user_name = os.environ["GITHUB_USER"]
app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"hello world! user: {user_name} "}


@app.get("/posts")
def posts():
    return {"this is your first post"}

# note the path indicator always go to the first match
