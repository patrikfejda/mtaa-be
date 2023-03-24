from app.db.orm import session
from fastapi import HTTPException
from app.model.classes import Status


def statusCreate(
    status: str,
    userId: int,
    latitude: str,
    longitude: str,
):
    status = Status(
        status=status, userId=userId, latitude=latitude, longitude=longitude
    )
    session.add(status)
    session.commit()
    return status.private_data()


def statusGet(statusId):
    status = session.query(Status).filter(Status.id == statusId).first()
    if status is None:
        raise HTTPException(404, "Status not found")
    return status.public_data()


def statusGetAll():
    return [status.public_data() for status in session.query(Status).all()]


def statusDelete(userId, statusId):
    # check if status exists
    status = session.query(Status).filter(Status.id == statusId).first()
    if status is None:
        raise HTTPException(404, "Status not found")
    if status.userId != int(userId):
        raise HTTPException(403, "You can only delete your own statuses")
    session.query(Status).filter(Status.id == statusId).delete()
    session.commit()
    return True
