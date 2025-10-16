# app/pricing.py
from datetime import datetime
from math import exp

def compute_dynamic_price(base_price: float,
                          seats_total: int,
                          seats_available: int,
                          departure: datetime,
                          demand_level: float = 1.0):
    """
    Simple heuristic:
      - seats_factor: lower seats_available => increased price
      - time_factor: closer to departure => increased price
      - demand_level: multiplier from simulator

    Returns float price.
    """

    # seats factor: exponential when <30% seats left
    if seats_total <= 0:
        seats_factor = 1.0
    else:
        pct = seats_available / seats_total
        # map pct in (0,1] to a multiplier between 1 and 2.5
        seats_factor = 1.0 + (1.5 * (1 - pct))  # linear; adjust to taste

    # time factor: more aggressive close to departure
    now = datetime.utcnow()
    delta_hours = max(1.0, (departure - now).total_seconds() / 3600.0)
    # less hours => higher multiplier; using inverse log
    time_factor = 1.0 + (1.0 / (delta_hours ** 0.6))  # control steepness

    # demand multiplier
    demand_factor = demand_level

    price = base_price * seats_factor * time_factor * demand_factor
    # prevent absurd tiny/huge values
    price = max(5.0, round(price, 2))
    return price
