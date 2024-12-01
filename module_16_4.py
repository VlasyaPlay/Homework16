from fastapi import FastAPI, Path, status, Body, HTTPException
from typing import Annotated, Dict, List, Optional
from pydantic import BaseModel

app = FastAPI()

users: List['User'] = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/users')
def get_users():
    return users


@app.post('/user/{username}/{age}')
def register_user(username: str = Path(min_length=5,
                                       max_length=20,
                                       description="Enter username",
                                       example="Vlasya"),
                  age: int = Path(ge=18,
                                  le=120,
                                  description="Enter age",
                                  example="31")) -> User:
    user_id = len(users) + 1
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
