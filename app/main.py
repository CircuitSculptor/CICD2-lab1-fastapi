from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Base, UserDB
from app.schemas import UserCreate, UserRead

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab 3 - FastAPI SQLAlchemy User API")

users: list[UserCreate] = []

@app.get("/health")
def health():
    return{"status": "ok"}


@app.get("/hello")
def hello():
    return{"message":"Hello from FastAPI"}


@app.post("/api/users", 
    response_model=UserRead, 
    status_code=status.HTTP_201_CREATED,)
def add_user(new_user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(**new_user.model_demp())
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    excpet IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email or student_id already exists",
        )
    
    return db_user



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

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for existing_user in users:
        if existing_user.user_id == user_id:
            return existing_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )