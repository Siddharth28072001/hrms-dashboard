import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use the DATABASE_URL from Render environment
DATABASE_URL = os.environ.get("DATABASE_URL")  

# Fallback for local development
if DATABASE_URL is None:
    DATABASE_URL = "postgresql://postgres:1234@localhost:5432/hrms"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()