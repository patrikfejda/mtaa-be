from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine


engine = create_engine(
    f"postgresql://postgres:postgres@mtaa-db:5432/mtaa_db", future=True
)


Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    username = Column(String)
    display_name = Column(String)
    profile_photo_url = Column(String)
    created_at = Column(String)

    def __repr__(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "display_name": self.display_name,
            "profile_photo_url": self.profile_photo_url,
            "created_at": self.created_at
        }

def create_table():  
    Base.metadata.create_all(engine)

# User(name='ed', fullname='Ed Jones', nickname='edsnickname')

# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()
# ed_user = User(email="patrikfejda@gmail.com", username="patrikfejda", display_name="Patrik Fejda")
# session.add(ed_user)
