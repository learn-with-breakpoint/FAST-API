from fastapi import FastAPI
import os
from pydantic import BaseModel


# creating posts variable in memory
posts_data = {1: {"title": "someone's biography",
                  "content": "self propaganda",
                  "author": "weirdo who has lots of free time",
                  "price": 200,
                  "id": 1}}


class BookMeta(BaseModel):
    title: str
    content: str
    author: str
    price: float


user_name = os.environ["GITHUB_USER"]
app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"hello world! user: {user_name} "}


@app.get("/posts")
def posts():
    return {"data": posts_data}


@app.post("/posts")
def create_posts(payload: BookMeta):
    post_dict = payload.model_dump()
    id = len(posts_data) + 1
    post_dict["id"] = id
    posts_data[id] = post_dict
    return post_dict
