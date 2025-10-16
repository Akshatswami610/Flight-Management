# app/simulator.py
import asyncio
import random
from datetime import datetime, timedelta
from .database import SessionLocal
from .crud import update_seats, get_all_flights
from .pricing import compute_dynamic_price
from .models import Flight
from sqlalchemy.orm import Session

# Global in-memory demand levels by route (simple)
demand_levels = {}  # e.g. {("DEL","BOM"): 1.2}

async def periodic_demand_and_seat_changes(interval_seconds: int = 10):
    """
    This coroutine runs indefinitely and simulates demand changes and seat
    adjustments for random flights. Run it in background on app startup.
    """
    while True:
        try:
            db = SessionLocal()
            flights = db.query(Flight).all()
            if not flights:
                await asyncio.sleep(interval_seconds)
                continue

            # choose a few random flights to change
            for _ in range(max(1, len(flights)//10)):
                f = random.choice(flights)
                # simulate random bookings or cancellations
                change = random.choices([-2,-1,0,0,0,1,1,2], weights=[1,3,20,20,20,3,2,1])[0]
                # ensure seats don't go negative
                new_available = max(0, min(f.seats_total, f.seats_available + change))
                if new_available != f.seats_available:
                    f.seats_available = new_available
                    db.add(f)
            db.commit()

            # random walk for demand_levels per route key
            routes = {(f.origin, f.destination) for f in flights}
            for route in routes:
                base = demand_levels.get(route, 1.0)
                base *= random.uniform(0.98, 1.05)
                base = max(0.7, min(2.5, base))
                demand_levels[route] = base

        except Exception as e:
            print("Simulator error:", e)
        finally:
            db.close()
        await asyncio.sleep(interval_seconds)
