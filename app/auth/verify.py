from fastapi import HTTPException
from app.model.user import authorize_user

def verify_token(user_id, jwt):
    authorized = authorize_user(user_id, jwt)
    if not authorized:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return True

