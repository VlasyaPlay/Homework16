from fastapi import FastAPI
from typing import Annotated
from fastapi import Path

app = FastAPI()


@app.get("/")
async def read_root():
    return ("Главная страница")


@app.get("/user/admin")
async def admin():
    return ("Вы вошли как администратор")


@app.get("/user/{user_id}")
async def users_id(user_id: Annotated[int, Path(ge=1,
                                                le=100,
                                                description="Enter User ID",
                                                example="1")]):
    return (f"Вы вошли как пользоваетль №{user_id}")


@app.get("/user/{username}/{age}")
async def new_user(username: str = Path(min_length=5,
                                        max_length=20,
                                        description="Enter username",
                                        example="Vlasya"),
                   age: int = Path(ge=18,
                                   le=120,
                                   description="Enter age",
                                   example="31")):
    return (f"Информация о пользователе. Имя: {username}, Возраст: {age}")