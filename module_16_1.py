from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
  return ("Главная страница")

@app.get("/user/admin")
async def admin():
  return ("Вы вошли как администратор")

@app.get("/user/{user_id}")
async def users_id(user_id: str):
  return (f"Вы вошли как пользоваетль №{user_id}")

@app.get("/user")
async def new_user(username: str, age: int):
  return (f"Информация о пользователе. Имя: {username}, Возраст: {age}")
