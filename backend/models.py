"""SQLAlchemy ORM models for the vaccination manager.

- User: basic user profile.
- Vaccine: vaccine catalog.
- Vaccination: user vaccination record.
"""

from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    vaccinations = relationship("Vaccination", back_populates="user")

class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    manufacturer = Column(String)
    efficacy = Column(String)
    interval_days = Column(Integer, nullable=False)  # days between doses

    vaccinations = relationship("Vaccination", back_populates="vaccine")

class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"), nullable=False)
    date = Column(Date, nullable=False)
    side_effects = Column(JSON, default={})  # e.g., {"fever": true}

    user = relationship("User", back_populates="vaccinations")
    vaccine = relationship("Vaccine", back_populates="vaccinations")
