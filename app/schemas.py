from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints

class UserCreate(BaseModel):
    name: NameStr
    emai;: EmailStr
    age: int = Field(gt=18, lt=120)
    student_id: StudentIdStr

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: NameStr
    email: EmailStr
    age: int
    student_id: StudentIdStr



