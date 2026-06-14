"""
Database configuration using SQLAlchemy and PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# In a real project, use environment variables
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/vaccination_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
