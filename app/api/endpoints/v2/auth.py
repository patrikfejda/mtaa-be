from fastapi import APIRouter, HTTPException, status

from app import crud, schemas
from app.api.dependencies import CurrentUserDependency, SessionDependency
from app.auth.jwt_token import create_access_token

router = APIRouter()


@router.post("/login", response_model=schemas.AuthResponse)
async def auth_login(auth: schemas.AuthLogin, db: SessionDependency):
    user = crud.authenticate_user(db=db, username=auth.username, password=auth.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(auth.username)
    return {"access_token": access_token, "user": user}


@router.post("/register", response_model=schemas.AuthResponse)
async def auth_register(user: schemas.UserCreate, db: SessionDependency):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered"
        )
    new_user = crud.create_user(db=db, user=user)
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "user": new_user}


@router.get("/check", response_model=schemas.User)
async def auth_check(current_user: CurrentUserDependency):
    return current_user
