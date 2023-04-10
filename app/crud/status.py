from sqlalchemy.orm import Session

from app import models, schemas


def get_all_statuses(db: Session):
    return db.query(models.Status).all()


def get_status(db: Session, status_id: int):
    return db.query(models.Status).filter(models.Status.id == status_id).first()


def create_status(db: Session, status: schemas.StatusCreate, author_id: int):
    db_status = models.Status(**status.dict(), author_id=author_id)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


def delete_status(db: Session, status_id: int):
    db_status = get_status(db=db, status_id=status_id)
    db.delete(db_status)
    db.commit()
