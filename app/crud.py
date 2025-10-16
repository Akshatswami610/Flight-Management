# app/crud.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models

def get_all_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()

def search_flights(db: Session, origin=None, destination=None, date=None):
    q = db.query(models.Flight)
    if origin:
        q = q.filter(models.Flight.origin == origin)
    if destination:
        q = q.filter(models.Flight.destination == destination)
    if date:
        # match departure date
        start = datetime.fromisoformat(date + "T00:00:00")
        end = start + timedelta(days=1)
        q = q.filter(models.Flight.departure >= start, models.Flight.departure < end)
    return q.all()

def get_flight(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()

def update_seats(db: Session, flight_id: int, seats_delta: int):
    f = get_flight(db, flight_id)
    if not f:
        return None
    f.seats_available = max(0, f.seats_available + seats_delta)
    db.commit()
    db.refresh(f)
    return f
