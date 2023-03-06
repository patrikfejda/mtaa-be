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
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name,
            self.fullname,
            self.nickname,
        )
    
print(User.__table__)

print(Base.metadata.create_all(engine))

# User(name='ed', fullname='Ed Jones', nickname='edsnickname')

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")
session.add(ed_user)
