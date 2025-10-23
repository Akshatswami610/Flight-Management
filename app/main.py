from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uvicorn

from .database import SessionLocal, engine, Base
from . import models, crud, pricing, simulator, schemas, payment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    import asyncio
    asyncio.create_task(simulator.periodic_demand_and_seat_changes(interval_seconds=10))

@app.get("/flights", response_model=List[schemas.FlightRead])
def list_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rows = crud.get_all_flights(db, skip=skip, limit=limit)
    out = []
    for r in rows:
        route = (r.origin, r.destination)
        demand = simulator.demand_levels.get(route, 1.0)
        price = pricing.compute_dynamic_price(r.base_price, r.seats_total, r.seats_available, r.departure, demand)
        out.append({**r.__dict__, "price": price})
    return out

@app.get("/search", response_model=List[schemas.FlightRead])
def search_flights(origin: Optional[str] = None, destination: Optional[str] = None, date: Optional[str] = None, db: Session = Depends(get_db)):
    rows = crud.search_flights(db, origin=origin, destination=destination, date=date)
    out = []
    for r in rows:
        route = (r.origin, r.destination)
        demand = simulator.demand_levels.get(route, 1.0)
        price = pricing.compute_dynamic_price(r.base_price, r.seats_total, r.seats_available, r.departure, demand)
        out.append({**r.__dict__, "price": price})
    return out

@app.post("/book", response_model=schemas.BookingResponse)
def book_flight(req: schemas.BookingRequest, db: Session = Depends(get_db)):
    f = crud.get_flight(db, req.flight_id)
    if not f:
        raise HTTPException(status_code=404, detail="Flight not found")

    route = (f.origin, f.destination)
    demand = simulator.demand_levels.get(route, 1.0)
    price = pricing.compute_dynamic_price(f.base_price, f.seats_total, f.seats_available, f.departure, demand)

    booking = crud.try_reserve_and_create_booking(db, f.id, req.passenger.dict(), req.seat_pref, price)
    pay_result = payment.simulate_payment(price)

    booking = crud.confirm_booking_payment(db, booking.pnr, pay_result["success"], pay_result.get("txn_id"))

    return schemas.BookingResponse(
        pnr=booking.pnr,
        flight_id=booking.flight_id,
        passenger=booking.passenger,
        seat_no=booking.seat_no,
        price_paid=booking.price_paid,
        status=booking.status.value,
        created_at=booking.created_at
    )

@app.get("/booking/{pnr}", response_model=schemas.BookingResponse)
def get_booking(pnr: str, db: Session = Depends(get_db)):
    booking = crud.get_booking_by_pnr(db, pnr)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return schemas.BookingResponse(
        pnr=booking.pnr,
        flight_id=booking.flight_id,
        passenger=booking.passenger,
        seat_no=booking.seat_no,
        price_paid=booking.price_paid,
        status=booking.status.value,
        created_at=booking.created_at
    )

@app.post("/booking/{pnr}/cancel", response_model=schemas.BookingResponse)
def cancel_booking(pnr: str, db: Session = Depends(get_db)):
    booking = crud.cancel_booking(db, pnr)
    return schemas.BookingResponse(
        pnr=booking.pnr,
        flight_id=booking.flight_id,
        passenger=booking.passenger,
        seat_no=booking.seat_no,
        price_paid=booking.price_paid,
        status=booking.status.value,
        created_at=booking.created_at
    )

@app.get("/bookings", response_model=List[schemas.BookingResponse])
def bookings_by_email(email: str, db: Session = Depends(get_db)):
    rows = crud.get_bookings_by_email(db, email)
    return [
        schemas.BookingResponse(
            pnr=b.pnr,
            flight_id=b.flight_id,
            passenger=b.passenger,
            seat_no=b.seat_no,
            price_paid=b.price_paid,
            status=b.status.value,
            created_at=b.created_at
        )
        for b in rows
    ]

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
