from fastapi import FastAPI, HTTPException, status
import os
from pydantic import BaseModel


# creating posts variable in memory
posts_data = {1: {"title": "someone's biography",
                  "content": "self propaganda",
                  "author": "weirdo who has lots of free time / Money",
                  "price": 200,
                  "id": 1}}


class BookMeta(BaseModel):
    title: str = None
    content: str = None
    author: str = None
    price: float = None


def remove_none_values(in_dict_: dict):
    """
    Remove dictionary entries with None values.

    Args:
    in_dict_ (dict): The dictionary to process.

    Returns:
    dict: The processed dictionary.
    """
    return {key: value for key, value in in_dict_.items()
            if value is not None}


def update_the_post_with_id(
        id: int, book_dict: dict, posts: dict[dict]) -> dict:
    id = int(id)
    for _, p in posts.items():
        if p["id"] == id:
            p.update(book_dict)
            return {'message': f"post with id {id} has been updated."}
    # in-case where we didn't find any post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found.")


def delete_the_post_with_id(id: int, posts: dict[dict]) -> dict:
    id = int(id)
    for v, p in posts.items():
        if p["id"] == id:
            posts.pop(v)
            return {'message': f"post with id {id} was deleted."}
    # in-case where we didn't find any post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found.")


def find_the_post_with_id(id: int, posts: dict[dict]) -> dict:
    id = int(id)
    for _, p in posts.items():
        if p["id"] == id:
            return p

    # in-case where we didn't find any post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found.")


user_name = os.environ["GITHUB_USER"]
app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"hello world! user: {user_name} "}


@app.get("/posts", status_code=status.HTTP_200_OK)
def posts():
    return {"data": posts_data}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: BookMeta):
    post_dict = payload.model_dump()
    id = len(posts_data) + 1
    post_dict["id"] = id
    posts_data[id] = post_dict
    return post_dict


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_with_id(id: str, posts_data: list = posts_data):
    return find_the_post_with_id(id=int(id), posts=posts_data)


@app.delete("/posts/{id}", status_code=status.HTTP_410_GONE)
def delete_post(id: str):
    return delete_the_post_with_id(id=id, posts=posts_data)


@app.patch("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: str, payload: BookMeta):
    book_dict = payload.model_dump()
    book_dict = remove_none_values(book_dict)
    return update_the_post_with_id(
        id=id, book_dict=book_dict, posts=posts_data)
