from fastapi import APIRouter, HTTPException, status

from app import crud, schemas
from app.api.dependencies import CurrentUserDependency, SessionDependency

router = APIRouter()


@router.get("/", response_model=list[schemas.Status])
def get_all_statuses(current_user: CurrentUserDependency, db: SessionDependency):
    return crud.get_all_statuses(db=db)


@router.post("/", response_model=schemas.Status, status_code=status.HTTP_201_CREATED)
def create_status(
    status_create: schemas.StatusCreate, current_user: CurrentUserDependency, db: SessionDependency
):
    return crud.create_status(db=db, status=status_create, author_id=current_user.id)


@router.delete("/{status_id}")
def delete_status(status_id: int, current_user: CurrentUserDependency, db: SessionDependency):
    db_status = crud.get_status(db=db, status_id=status_id)
    if not db_status or db_status.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return crud.delete_status(db=db, status_id=status_id)
