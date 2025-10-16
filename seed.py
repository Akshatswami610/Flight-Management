# seed.py
from datetime import datetime, timedelta
import random
from app.database import SessionLocal, engine, Base
from app.models import Flight

Base.metadata.create_all(bind=engine)
db = SessionLocal()

airports = ["DEL","BOM","BLR","MAA","HYD","COK","CCU","PNQ"]
airlines = ["IndiFly", "AirPy", "NeoAir", "SpiceSim"]

def random_datetime(days_ahead_min=1, days_ahead_max=30):
    base = datetime.utcnow()
    delta = timedelta(days=random.randint(days_ahead_min, days_ahead_max),
                      hours=random.randint(0,23),
                      minutes=random.choice([0,15,30,45]))
    return base + delta

db.query(Flight).delete()
db.commit()

for _ in range(120):
    o, d = random.sample(airports, 2)
    dep = random_datetime()
    dur = random.randint(60, 300)
    arr = dep + timedelta(minutes=dur)
    seats = random.choice([80,120,150,180,200])
    available = random.randint(0, seats)
    f = Flight(
        airline=random.choice(airlines),
        flight_no=f"IF{random.randint(100,999)}",
        origin=o,
        destination=d,
        departure=dep,
        arrival=arr,
        duration_min=dur,
        base_price=round(random.uniform(2000,15000),2),
        seats_total=seats,
        seats_available=available,
        meta=None
    )
    db.add(f)

db.commit()
print("Seeded flights:", db.query(Flight).count())
db.close()
