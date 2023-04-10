from fastapi import File, Form, UploadFile
from pydantic.dataclasses import dataclass

from .base_model import AppBaseModel, AppBaseModelConfig


class User(AppBaseModel):
    id: int
    email: str
    username: str
    display_name: str | None
    profile_photo_url: str | None


class UserCreate(AppBaseModel):
    email: str
    username: str
    password: str


@dataclass(config=AppBaseModelConfig)
class UserUpdate:
    display_name: str | None = Form(None)
    profile_photo: UploadFile | None = File(None)
