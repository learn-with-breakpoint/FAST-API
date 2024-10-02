from fastapi import FastAPI, HTTPException, status
import os
from pydantic import BaseModel
from utils import BookDatabaseConnection, dict_to_query


# create connection to the database
host = "localhost"
database = "bookstore"
user = "admin"
password = "LocalPasswordOnly"
book_db = BookDatabaseConnection(host, database, user, password)


class BookMeta(BaseModel):
    title: str = None
    preface: str = None
    author: str = None
    price: float = None


user_name = os.environ["GITHUB_USER"]
app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"hello world! user: {user_name} "}


@app.get("/posts", status_code=status.HTTP_200_OK)
def posts():
    query = """SELECT * FROM books"""
    data = book_db.execute_query(query=query, params=None, fetchall=True)
    return {"data": data}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: BookMeta):
    values = [payload.title, payload.author, payload.preface, payload.price]
    final_query = """INSERT INTO books (title, author, preface, price)
    VALUES (%s, %s, %s, %s)
    RETURNING * """
    rows = book_db.execute_query(query=final_query, params=values,
                                 fetchall=False, commit=True)
    return rows


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_with_id(id: str):
    return None


@app.delete("/posts/{id}", status_code=status.HTTP_410_GONE)
def delete_post(id: str):
    return None


@app.patch("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: str, payload: BookMeta):
    return None
