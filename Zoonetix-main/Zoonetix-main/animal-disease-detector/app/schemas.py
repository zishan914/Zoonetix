from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


class AdminUserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_admin: bool
    created_at: datetime | None = None
    prediction_count: int = 0

    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    message: str
    treatment: dict = {}


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "your name",
                "password": "securepassword123",
                "confirm_password": "securepassword123",
            }
        }


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }


class UserResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
