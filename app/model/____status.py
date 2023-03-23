from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine


engine = create_engine(
    f"postgresql://postgres:postgres@mtaa-db:5432/mtaa_db", future=True
)


Base = declarative_base()
class Status(Base):
    __tablename__ = "statuses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    status = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    created_at = Column(String)

    def __repr__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": self.created_at
        }

def create_table():
    print("Creating table statuses")
    Base.metadata.create_all(engine)

# User(name='ed', fullname='Ed Jones', nickname='edsnickname')

# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()
# ed_user = User(email="patrikfejda@gmail.com", username="patrikfejda", display_name="Patrik Fejda")
# session.add(ed_user)
