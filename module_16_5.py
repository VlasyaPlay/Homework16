from fastapi import FastAPI, Path, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated, Dict, List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users: List['User'] = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get('/users/{user_id}')
def get_users(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")


@app.post('/user/{username}/{age}')
def register_user(username: str = Path(min_length=5,
                                       max_length=20,
                                       description="Enter username",
                                       example="Vlasya"),
                  age: int = Path(ge=18,
                                  le=120,
                                  description="Enter age",
                                  example="31")) -> User:
    max_id = max((user.id for user in users), default=0)
    user_id = max_id + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int = Path(ge=1,
                                    le=100,
                                    description="Enter User ID",
                                    example="1"),
                username: str = Path(min_length=5,
                                     max_length=20,
                                     description="Enter username",
                                     example="Vlasya"),
                age: int = Path(ge=18,
                                le=120,
                                description="Enter age",
                                example="31")):
    try:
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
def delete_user(user_id: int = Path(ge=1,
                                    le=100,
                                    description="Enter User ID",
                                    example="1")):
    try:
        for user in users:
            if user.id == user_id:
                users.remove(user)
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")