from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class PassengerInfo(BaseModel):
    name: str
    email: str
    phone: Optional[str]

class BookingRequest(BaseModel):
    flight_id: int
    passenger: PassengerInfo
    seat_pref: Optional[str] = None

class BookingResponse(BaseModel):
    pnr: str
    flight_id: int
    passenger: Dict
    seat_no: Optional[str]
    price_paid: float
    status: str
    created_at: datetime

class FlightRead(BaseModel):
    id: int
    airline: str
    flight_no: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    duration_min: int
    base_price: float
    seats_total: int
    seats_available: int
    price: float

    class Config:
        orm_mode = True
