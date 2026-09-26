from fastapi import FastAPI, HTTPException, status, Response
from app.schemas import UserCreate

app = FastAPI(title="Lab 1 - FastAPI User API")

users: list[UserCreate] = []

@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/hello")
def hello():
    return{"message":"Hello from FastAPI"}


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(new_user: UserCreate):
    for existing_user in users:
        if existing_user.user_id == new_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="This user already exists"
            )
    users.append(new_user)
    return new_user

@app.get("/api/users", status_code=status.HTTP_200_OK)
def get_users():
    return users

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for index, existing_user in enumerate(users):
        if existing_user.user_id == user_id:
            users.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )