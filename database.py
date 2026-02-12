from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///./microbiome.db"  # File-based, no Docker!
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
