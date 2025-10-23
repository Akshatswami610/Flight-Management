from datetime import datetime

def compute_dynamic_price(base_price: float, seats_total: int, seats_available: int, departure: datetime, demand: float = 1.0):
    if seats_total <= 0:
        return base_price
    seat_factor = 1 - (seats_available / seats_total)
    time_factor = 1.0
    price = base_price * (1 + seat_factor * 0.5) * demand * time_factor
    return round(price, 2)
