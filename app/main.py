from fastapi import FastAPI, HTTPException, status
from app.schemas import UserCreate

app = FastAPI(title="Lab 1 - FastAPI User API")

users: list[UserCreate] = []

@app.get("/health")
def health():
    return{"status": "ok"}


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(new_user: UserCreate):
    for existing_user in users:
        if existing_user.user_id == new_user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This user already exists")
    users.append(new_user)
    return new_user