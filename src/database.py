from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_URL = "sqlite:///eshop.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal  = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def create_all():
    Base.metadata.create_all(bind=engine)

def generate_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()