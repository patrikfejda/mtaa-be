from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import crud
from app.config import settings
from app.db.dependencies import get_db


async def get_user_by_token_or_fail(
    db: Annotated[Session, Depends(get_db)], token: str, exception: Exception = JWTError()
):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        subject: str = payload.get("sub")
        if subject is None:
            raise exception
    except JWTError:
        raise exception

    user = crud.get_user_by_username(db=db, username=subject)
    if user is None:
        raise exception
    return user
