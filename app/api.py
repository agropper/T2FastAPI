# app/api.py

from fastapi import FastAPI, Body, Depends, Form, Request

from fastapi.templating import Jinja2Templates


from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

import couchdb
from couchdb.mapping import Document, TextField

class Person(Document):
    fullname = TextField()
    email = TextField()
    password = TextField()


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
templates = Jinja2Templates(directory="templates/")

def check_user(data: UserLoginSchema):
#    for user in users:
#        if user.email == data.email and user.password == data.password:
#            return True
#    doc = db[data.email]
    entryValid: bool = False
    person = Person.load(db, data.email)
    try:
        passwd = person.password
    except:
        passwd = None
    if passwd == data.password:
        return True
    else:
        return False


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!."}

@app.get("/form")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post("/form")
def form_post(request: Request, num: int = Form(...)):
    result = "A result"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return { "data": posts }

@app.get("/couch/{id}", tags=["posts"])
async def get_single_doc(id: str) -> dict:
    doc = db[id]
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

@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())

# Save to CouchDB
    doc = post.dict() | {'_id': 'bar'}
    db.save(doc)

    return {
        "data": "post added."
    }

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    person = Person.load(db, user.email)
    if person == None:
        db.save(user.dict() | {'_id': user.email})       
    else:
        if person.email == user.email:
            return {
            "error": "User already exists!"
        }
    return signJWT(user.email)

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

