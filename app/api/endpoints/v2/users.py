from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from filetype import is_image

from app import crud, schemas
from app.api.dependencies import CurrentUserDependency, SessionDependency

router = APIRouter()


@router.get("/", response_model=list[schemas.User])
async def get_all_users(current_user: CurrentUserDependency, db: SessionDependency):
    return crud.get_all_users(db=db)


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    user_update: Annotated[schemas.UserUpdate, Depends()],
    current_user: CurrentUserDependency,
    db: SessionDependency,
):
    if user_update.profile_photo and not is_image(user_update.profile_photo.file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File extension is not supported",
        )
    return crud.update_user(db=db, db_user=current_user, user_update=user_update)
