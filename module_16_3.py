from fastapi import FastAPI, Path
from typing import Annotated, Dict

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
def get_users() -> dict:
    return users


@app.post('/user/{username}/{age}')
def register_user(username: str = Path(min_length=5,
                                       max_length=20,
                                       description="Enter username",
                                       example="Vlasya"),
                  age: int = Path(ge=18,
                                  le=120,
                                  description="Enter age",
                                  example="31")) -> str:
    max_key = max(map(int, users.keys()), default=0)
    new_key = str(max_key + 1)

    users[new_key] = f'Имя: {username}, возраст: {age}'
    return f'User {new_key} is registered'


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
                                example="31")) -> str:
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str] = f'Имя: {username}, возраст: {age}'
        return f'The user {user_id} is updated'
    else:
        return f'User {user_id} not found'


@app.delete('/user/{user_id}')
def delete_user(user_id: int = Path(ge=1,
                                    le=100,
                                    description="Enter User ID",
                                    example="1")) -> str:
    user_id_str = str(user_id)
    if user_id_str in users:
        del users[user_id_str]
        return f'User {user_id} is deleted'
    else:
        return f'User {user_id} not found'