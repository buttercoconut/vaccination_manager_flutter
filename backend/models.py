"""
Database models using SQLAlchemy ORM.
"""

from datetime import date
from typing import List, Optional

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .database import Base

# Association table for many-to-many side effects
vaccination_side_effect = Table(
    "vaccination_side_effect",
    Base.metadata,
    Column("vaccination_id", Integer, ForeignKey("vaccinations.id")),
    Column("side_effect_id", Integer, ForeignKey("side_effects.id")),
)

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
    name = Column(String, unique=True, nullable=False)
    manufacturer = Column(String)
    efficacy = Column(String)

    vaccinations = relationship("Vaccination", back_populates="vaccine")

class SideEffect(Base):
    __tablename__ = "side_effects"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)

    vaccinations = relationship(
        "Vaccination", secondary=vaccination_side_effect, back_populates="side_effects"
    )

class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"))
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="vaccinations")
    vaccine = relationship("Vaccine", back_populates="vaccinations")
    side_effects = relationship(
        "SideEffect", secondary=vaccination_side_effect, back_populates="vaccinations"
    )
