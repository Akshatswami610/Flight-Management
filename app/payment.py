import random
import uuid

def simulate_payment(amount: float, success_rate: float = 0.9):
    ok = random.random() < success_rate
    return {
        "success": ok,
        "txn_id": str(uuid.uuid4()) if ok else None,
        "reason": None if ok else "payment_failed"
    }
