# app/api.py
import os
import stripe

from fastapi import FastAPI, Body, Depends, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

import couchdb
from couchdb.mapping import Document, TextField

from decouple import config

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


users = []

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")

# stripe.api_key = os.environ["STRIPE_KEY"]
# This is a terrible idea, only used for demo purposes!
stripe.api_key = config("STRIPE_SECRET_KEY")
app.state.stripe_customer_id = None



# @app.get("/", tags=["root"])
# async def read_root() -> dict:
#    return {"message": "Welcome to your blog!."}

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "hasCustomer": app.state.stripe_customer_id is not None})


@app.get("/success")
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


@app.get("/cancel")
async def cancel(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})


@app.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    data = await request.json()

    if not app.state.stripe_customer_id:
        customer = stripe.Customer.create(
            description="Demo customer",
        )
        app.state.stripe_customer_id = customer["id"]

    checkout_session = stripe.checkout.Session.create(
        customer=app.state.stripe_customer_id,
        success_url="http://localhost:8081/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:8081/cancel",
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price": data["priceId"],
            "quantity": 1
        }],
    )
    return {"sessionId": checkout_session["id"]}


@app.post("/create-portal-session")
async def create_portal_session():
    session = stripe.billing_portal.Session.create(
        customer=app.state.stripe_customer_id,
        return_url="http://localhost:8081"
    )
    return {"url": session.url}


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

