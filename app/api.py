# app/api.py

from fastapi import FastAPI, Body

from app.model import PostSchema, UserSchema, UserLoginSchema
# from app.auth.auth_handler import signJWT

import couchdb

couch = couchdb.Server('http://couchdb00.hagopian.net:5984/')
db = couch['hieofone2']

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users = []

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!."}

@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return { "data": posts }

@app.get("/couch/{id}", tags=["posts"])
async def get_single_doc(id: int) -> dict:
# Can't figure out how to pass in the id - silly!
    doc = db['e2082f83ebe29de3fdb40faa2a014412']
    return {
        "data": doc
    }

@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }

@app.post("/posts", tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())

# Save to CouchDB
    doc = post.dict()
    db.save(doc)

    return {
        "data": "post added."
    }

# @app.post("/user/signup", tags=["user"])
# async def create_user(user: UserSchema = Body(...)):
#     users.append(user) # replace with db call, making sure to hash the password first
#     return signJWT(user.email)