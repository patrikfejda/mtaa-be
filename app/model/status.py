from app.db.orm import session
from fastapi import HTTPException
from app.support.jwt import generate_jwt
from app.config import DONT_ALLOW_NOT_UNIQUE_EMAIL, DONT_ALLOW_NOT_UNIQUE_USERNAME
from app.model.classes import Status, User


def statusCreate(
    status: str,
    user_id: int,
    latitude: str,
    longitude: str,
):
    status = Status(
        status=status, user_id=user_id, latitude=latitude, longitude=longitude
    )
    session.add(status)
    session.commit()
    return status.private_data()

def statusGet(status_id):
    return session.query(Status).filter(Status.id == status_id).first().private_data()

def statusGetAll():
    return [status.public_data() for status in session.query(Status).all()]



def statusDelete(user_id, status_id):
    if session.query(Status).filter(Status.id == status_id).first().user_id != user_id:
        raise HTTPException(403, "You can only delete your own statuses")
    session.query(Status).filter(Status.id == status_id).delete()
    session.commit()
    return True


