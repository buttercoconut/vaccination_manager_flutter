"""SQLAlchemy models for the vaccination manager."""

from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)

    vaccinations = relationship("Vaccination", back_populates="user")

class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=True)
    efficacy = Column(String, nullable=True)

    vaccinations = relationship("Vaccination", back_populates="vaccine")

class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"), nullable=False)
    date = Column(Date, nullable=False)
    side_effects = Column(JSON, nullable=True)

    user = relationship("User", back_populates="vaccinations")
    vaccine = relationship("Vaccine", back_populates="vaccinations")
