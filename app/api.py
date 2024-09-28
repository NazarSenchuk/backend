from typing import Annotated
from sqlalchemy import select
from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import model
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt
from app.db import SessionLocal, engine
from app.model import PostSchema, UserSchema, UserLoginSchema, Post, User
from fastapi.middleware.cors import CORSMiddleware



users = []

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)



def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

db_dependency = Annotated[Session,Depends(get_db)]

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]



model.Base.metadata.create_all(bind=engine)
# helpers
@app.get("/api/check_db")
def test(db:db_dependency):
    post = Post(title="hello")
    db.add(post)
    db.commit()
    return {"response":db.query(Post).all()}

def check_user(data: UserLoginSchema,db:db_dependency):
    for user in db.query(User).all():
        if user.email == data.email and user.password == data.password:
            return True
    return False


# route handlers

@app.get("/api/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}


@app.get("/api/posts", tags=["posts"])
async def get_posts(db:db_dependency):
    return { "data": db.query(Post).all() }


@app.post("/api/user/signup", tags=["user"])
async def create_user(db:db_dependency,user: UserSchema = Body(...)):
    User.validate_password(user.password)
    user_check = db.query(User).filter(User.username ==  user.fullname).all()
    
    if not user_check:
        user_created = User(username=user.fullname,password = user.password, email=user.email)
        db.add(user_created)
        db.commit()# replace with db call, making sure to hash the password first
        return sign_jwt(user.email)
    return{"error": "User with this username created"}



@app.get("/api/posts/{id}", tags=["posts"])
async def get_single_post(id: int,db:db_dependency) -> dict:

    post = db.query(Post).filter(Post.id == id).all()
    if post:
        return post
    else:
        return{"error": "Post not found"}


@app.post("/api/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema , db:db_dependency):
    post_created = Post(title= post.title)
    db.add(post_created)
    db.commit()
    return {
        "data": "post added."
    }


@app.post("/api/user/login", tags=["user"])
async def user_login(db:db_dependency ,user: UserLoginSchema = Body(...)):
    if check_user(user,db):
        return sign_jwt(user.email)
    return{"error": "Wrong login or password"}