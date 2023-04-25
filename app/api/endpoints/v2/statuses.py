from fastapi import APIRouter, HTTPException, status
import unicodedata

from app import crud, schemas
from app.api.dependencies import CurrentUserDependency, SessionDependency

router = APIRouter()

NOT_APPROPIATE_WORDS = ['fuck', 'nigga', 'chuj', 'pica', 'pice', 'pici', 'debil', 'kurva', 'skurven', 'kurvu']

@router.get("/", response_model=list[schemas.Status])
def get_all_statuses(current_user: CurrentUserDependency, db: SessionDependency):
    return crud.get_all_statuses(db=db)


@router.post("/", response_model=schemas.Status, current_user=CurrentUserDependency, status_code=status.HTTP_201_CREATED)
def create_status(
    status_create: schemas.StatusCreate, db: SessionDependency
):
    # CHECK FOR NOT APPROPRIATE WORDS
    normalized_sentence = unicodedata.normalize('NFKD', status_create.text).encode('ASCII', 'ignore').decode('utf-8')
    lowercase_sentence = normalized_sentence.casefold()
    if any(word in lowercase_sentence for word in NOT_APPROPIATE_WORDS):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return crud.create_status(db=db, status=status_create, author_id=current_user.id)


@router.delete("/{status_id}")
def delete_status(status_id: int, current_user: CurrentUserDependency, db: SessionDependency):
    db_status = crud.get_status(db=db, status_id=status_id)
    if not db_status or db_status.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return crud.delete_status(db=db, status_id=status_id)
