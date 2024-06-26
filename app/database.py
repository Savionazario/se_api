from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:81606700@localhost:5433/condo_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20, 
    max_overflow=0,
)
# conn = engine.connect() 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()