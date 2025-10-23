import asyncio
import random
from .database import SessionLocal
from .models import Flight

demand_levels = {}

async def periodic_demand_and_seat_changes(interval_seconds: int = 12):
    while True:
        await asyncio.sleep(interval_seconds)
        db = SessionLocal()
        flights = db.query(Flight).all()
        for f in flights:
            route = (f.origin, f.destination)
            demand_levels[route] = random.uniform(0.8, 1.3)
        db.close()
