from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.auth.dependencies import get_current_user
from app.db.dependencies import get_db

SessionDependency = Annotated[Session, Depends(get_db)]
CurrentUserDependency = Annotated[schemas.User, Depends(get_current_user)]
