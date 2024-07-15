from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_URL = "sqlite:///:memory:"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)