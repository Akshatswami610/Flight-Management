# SQLAlchemy models + Pydantic schemas

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import Boolean
from sqlalchemy.types import JSON
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import Optional
from .database import Base

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, index=True)
    airline = Column(String, index=True)
    flight_no = Column(String, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    departure = Column(DateTime, index=True)
    arrival = Column(DateTime, index=True)
    duration_min = Column(Integer)
    base_price = Column(Float)      # base fare
    seats_total = Column(Integer)
    seats_available = Column(Integer)
    # optional JSON for extra data
    meta = Column(String, nullable=True)

# Pydantic schemas
class FlightRead(BaseModel):
    id: int
    airline: str
    flight_no: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    duration_min: int
    price: float
    seats_available: int

    class Config:
        orm_mode = True

class FlightSearchParams(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD
    sort_by: Optional[str] = Field(None, regex="^(price|duration|departure)$")
    order: Optional[str] = Field("asc", regex="^(asc|desc)$")
