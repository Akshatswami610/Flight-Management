# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uvicorn

from .database import SessionLocal, engine, Base
from . import models, crud, pricing, simulator

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Search API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    # start background simulator
    import asyncio
    asyncio.create_task(simulator.periodic_demand_and_seat_changes(interval_seconds=12))

@app.get("/flights", response_model=List[models.FlightRead])
def list_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rows = crud.get_all_flights(db, skip=skip, limit=limit)
    out = []
    for r in rows:
        # compute dynamic price
        route = (r.origin, r.destination)
        demand = simulator.demand_levels.get(route, 1.0)
        price = pricing.compute_dynamic_price(
            r.base_price, r.seats_total, r.seats_available, r.departure, demand)
        out.append({**r.__dict__, "price": price})
    return out

@app.get("/search", response_model=List[models.FlightRead])
def search_flights(origin: Optional[str] = Query(None),
                   destination: Optional[str] = Query(None),
                   date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
                   sort_by: Optional[str] = Query(None, regex="^(price|duration|departure)$"),
                   order: str = Query("asc", regex="^(asc|desc)$"),
                   db: Session = Depends(get_db)):
    rows = crud.search_flights(db, origin=origin, destination=destination, date=date)
    out = []
    for r in rows:
        route = (r.origin, r.destination)
        demand = simulator.demand_levels.get(route, 1.0)
        price = pricing.compute_dynamic_price(
            r.base_price, r.seats_total, r.seats_available, r.departure, demand)
        obj = {**r.__dict__, "price": price}
        out.append(obj)

    # Sorting
    reverse = (order == "desc")
    if sort_by == "price":
        out.sort(key=lambda x: x["price"], reverse=reverse)
    elif sort_by == "duration":
        out.sort(key=lambda x: x["duration_min"], reverse=reverse)
    elif sort_by == "departure":
        out.sort(key=lambda x: x["departure"], reverse=reverse)

    return out

@app.get("/flights/{flight_id}", response_model=models.FlightRead)
def get_flight(flight_id: int, db: Session = Depends(get_db)):
    r = crud.get_flight(db, flight_id)
    if not r:
        raise HTTPException(status_code=404, detail="Flight not found")
    route = (r.origin, r.destination)
    demand = simulator.demand_levels.get(route, 1.0)
    price = pricing.compute_dynamic_price(
            r.base_price, r.seats_total, r.seats_available, r.departure, demand)
    return {**r.__dict__, "price": price}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
