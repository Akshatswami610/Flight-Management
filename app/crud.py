from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from .models import Flight, Booking, BookingStatus
import uuid

# --- Flight Queries ---

def get_all_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Flight).offset(skip).limit(limit).all()

def search_flights(db: Session, origin=None, destination=None, date=None):
    q = db.query(Flight)
    if origin:
        q = q.filter(Flight.origin == origin)
    if destination:
        q = q.filter(Flight.destination == destination)
    if date:
        start = datetime.fromisoformat(date + "T00:00:00")
        end = start + timedelta(days=1)
        q = q.filter(Flight.departure >= start, Flight.departure < end)
    return q.all()

def get_flight(db: Session, flight_id: int):
    return db.query(Flight).filter(Flight.id == flight_id).first()


# --- Booking Logic ---

def try_reserve_and_create_booking(db: Session, flight_id: int, passenger: dict, seat_pref: str, simulated_price: float):
    flight = db.query(Flight).filter(Flight.id == flight_id).with_for_update().first()
    if not flight:
        raise ValueError("Flight not found")
    if flight.seats_available <= 0:
        raise ValueError("No seats available")

    flight.seats_available -= 1

    pnr = str(uuid.uuid4())[:8].upper()
    booking = Booking(
        flight_id=flight_id,
        passenger=passenger,
        seat_no=seat_pref,
        price_paid=simulated_price,
        status=BookingStatus.PENDING,
        pnr=pnr
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def confirm_booking_payment(db: Session, pnr: str, success: bool, txn_id: str = None):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if not booking:
        raise ValueError("Booking not found")

    if success:
        booking.status = BookingStatus.CONFIRMED
    else:
        booking.status = BookingStatus.FAILED
        # release seat
        flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
        if flight:
            flight.seats_available += 1

    db.commit()
    db.refresh(booking)
    return booking

def cancel_booking(db: Session, pnr: str):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if not booking:
        raise ValueError("Booking not found")
    if booking.status == BookingStatus.CANCELLED:
        raise ValueError("Already cancelled")

    booking.status = BookingStatus.CANCELLED
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    if flight:
        flight.seats_available += 1

    db.commit()
    db.refresh(booking)
    return booking

def get_booking_by_pnr(db: Session, pnr: str):
    return db.query(Booking).filter(Booking.pnr == pnr).first()

def get_bookings_by_email(db: Session, email: str):
    return db.query(Booking).filter(Booking.passenger["email"].astext == email).order_by(Booking.created_at.desc()).all()
