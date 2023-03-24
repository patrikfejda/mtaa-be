from fastapi import HTTPException
from app.model.user import authorize_user


def verify_token(userId, jwt):
    authorized = authorize_user(userId, jwt)
    if not authorized:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
