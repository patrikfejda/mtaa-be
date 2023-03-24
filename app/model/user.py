from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime, func
from app.db.orm import session, engine
from fastapi import HTTPException
from app.support.jwt import generate_jwt
from app.config import DONT_ALLOW_NOT_UNIQUE_EMAIL, DONT_ALLOW_NOT_UNIQUE_USERNAME
from app.model.classes import User

# Column(Integer, Sequence("userId_seq"), primary_key=True)


Base = declarative_base()

def emailAlreadyExists(email):
    return session.query(User.id).filter_by(email=email).first() is not None

def usernameAlreadyExists(username):
    return session.query(User.id).filter_by(username=username).first() is not None

def userCreate(
    email, password, username=None, displayName=None, profilePhotoUrl=None
):
    if emailAlreadyExists(email) and DONT_ALLOW_NOT_UNIQUE_EMAIL:
        raise HTTPException(status_code=409, detail="This email alredy registered")
    if usernameAlreadyExists(username) and DONT_ALLOW_NOT_UNIQUE_USERNAME:
        raise HTTPException(status_code=409, detail="This username alredy registered")
    new_user = User(
        email=email,
        username=username,
        password=password,
        displayName=displayName,
        profilePhotoUrl=profilePhotoUrl,
        jwt=generate_jwt(),
    )
    session.add(new_user)
    print(new_user)
    session.commit()
    jwt = new_user.jwt
    return jwt, new_user.public_data()

    

def userLogin(username, password):

    user = session.query(User).filter_by(username=username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user.jwt = generate_jwt()
    session.commit()
    return user.jwt, user.public_data()


def userGet(id):
    user = session.query(User).filter_by(id=id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.private_data()


def userUpdate(id, displayName=None, profilePhotoUrl=None):
    user = session.query(User).filter_by(id=id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if displayName is not None:
        user.displayName = displayName
    if profilePhotoUrl is not None:
        user.profilePhotoUrl = profilePhotoUrl
    session.commit()
    return user.public_data()

def userGetAll():
    users = session.query(User).all()
    users = [user.public_data() for user in users]
    return users

def authorize_user(userId, jwt):
    user = session.query(User).filter_by(id=userId).first()
    if user is None:
        return False
    if user.jwt != jwt:
        return False
    return True
