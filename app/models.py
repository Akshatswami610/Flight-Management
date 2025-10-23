from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class BookingStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

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
    base_price = Column(Float)
    seats_total = Column(Integer)
    seats_available = Column(Integer)
    meta = Column(JSON, nullable=True)

    bookings = relationship("Booking", back_populates="flight")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    pnr = Column(String(12), unique=True, index=True, nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id", ondelete="CASCADE"), nullable=False)
    passenger = Column(JSON, nullable=False)   # name, email, phone
    seat_no = Column(String, nullable=True)
    price_paid = Column(Float, nullable=False)
    status = Column(SAEnum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    flight = relationship("Flight", back_populates="bookings")

    __table_args__ = (
        UniqueConstraint("pnr", name="uq_bookings_pnr"),
    )
