from typing import Annotated

from fastapi import Depends, HTTPException, Query, WebSocket, WebSocketException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.auth.helpers import get_user_by_token_or_fail
from app.db.dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v2/auth/login")

SessionDependency = Annotated[Session, Depends(get_db)]


async def get_current_user(
    db: SessionDependency,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await get_user_by_token_or_fail(db=db, token=token, exception=credentials_exception)


async def get_current_websocket_user(
    db: SessionDependency,
    token: Annotated[str, Query()],
):
    ws_credentials_exception = WebSocketException(
        code=status.WS_1008_POLICY_VIOLATION, reason="Could not validate credentials"
    )
    return await get_user_by_token_or_fail(db=db, token=token, exception=ws_credentials_exception)


CurrentUserDependency = Annotated[models.User, Depends(get_current_user)]
CurrentWebsocketUserDependency = Annotated[models.User, Depends(get_current_websocket_user)]
