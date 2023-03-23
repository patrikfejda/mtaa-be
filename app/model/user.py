from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime, func
from app.db.orm import session, engine
from fastapi import HTTPException
from app.support.jwt import generate_jwt
from app.config import DONT_ALLOW_NOT_UNIQUE_EMAIL, DONT_ALLOW_NOT_UNIQUE_USERNAME


# Column(Integer, Sequence("user_id_seq"), primary_key=True)


Base = declarative_base()


class User(Base):
    __tablename__ = "usersxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    id = Column(Integer, primary_key=True)
    # email = Column(String)
    # username = Column(String)
    # password = Column(String)
    # jwt = Column(String)
    # display_name = Column(String)
    # profile_photo_url = Column(String)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_safe_data(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "display_name": self.display_name,
            "profile_photo_url": self.profile_photo_url,
            "created_at": self.created_at,
        }

    def __repr__(self):
        return (
            "<User(id='%s', email='%s', username='%s', display_name='%s', profile_photo_url='%s', created_at='%s')>"
            % (
                self.id,
                self.email,
                self.username,
                self.display_name,
                self.profile_photo_url,
                self.created_at,
            )
        )


def create_table():
    print("Creating table users")
    # Base.metadata.create_all(engine)

def emailAlreadyExists(email):
    return session.query(User.id).filter_by(email=email).first() is not None

def usernameAlreadyExists(username):
    return session.query(User.id).filter_by(username=username).first() is not None

def userCreate(
    email, password, username=None, display_name=None, profile_photo_url=None
):
    if emailAlreadyExists(email) and DONT_ALLOW_NOT_UNIQUE_EMAIL:
        raise HTTPException(status_code=409, detail="This email alredy registered")
    if usernameAlreadyExists(username) and DONT_ALLOW_NOT_UNIQUE_USERNAME:
        raise HTTPException(status_code=409, detail="This username alredy registered")
    new_user = User(
        email=email,
        username=username,
        password=password,
        display_name=display_name,
        profile_photo_url=profile_photo_url,
        jwt=generate_jwt(),
    )
    session.add(new_user)
    print(new_user)
    session.commit()
    jwt = new_user.jwt
    return jwt, new_user.to_safe_data()

    

def userLogin(username, password):

    user = session.query(User).filter_by(username=username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user.jwt = generate_jwt()
    session.commit()
    return user.jwt, user.to_safe_data()


def userGet(id):
    user = session.query(User).filter_by(id=id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_safe_data()


def userUpdate(id, display_name=None, profile_photo_url=None):
    user = session.query(User).filter_by(id=id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if display_name is not None:
        user.display_name = display_name
    if profile_photo_url is not None:
        user.profile_photo_url = profile_photo_url
    session.commit()
    return user.to_safe_data()

def userGetAll():
    users = session.query(User).all()
    users = [user.to_safe_data() for user in users]
    return users

def authorize_user(user_id, jwt):
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        return False
    if user.jwt != jwt:
        return False
    return True
