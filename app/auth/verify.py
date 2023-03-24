from fastapi import HTTPException
from app.model.user import authorizeUser


def verifyToken(userId, jwt):
    authorized = authorizeUser(userId, jwt)
    if not authorized:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
