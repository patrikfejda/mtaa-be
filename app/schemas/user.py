from fastapi import File, Form, UploadFile
from pydantic import EmailStr, Field
from pydantic.dataclasses import dataclass

from .base_model import AppBaseModel, AppBaseModelConfig


class User(AppBaseModel):
    id: int
    email: str
    username: str
    display_name: str | None
    profile_photo_url: str | None


class UserCreate(AppBaseModel):
    email: EmailStr
    username: str = Field(min_length=3)
    password: str = Field()


@dataclass(config=AppBaseModelConfig)
class UserUpdate:
    display_name: str | None = Form(None)
    profile_photo: UploadFile | None = File(None)
