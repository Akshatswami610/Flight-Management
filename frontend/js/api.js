const API_BASE = "http://127.0.0.1:8000";

async function fetchFlights(origin, destination, date) {
  const res = await fetch(`${API_BASE}/flights/search?origin=${origin}&destination=${destination}&date=${date}`);
  return res.json();
}

async function bookFlight(flightId, passenger) {
  const res = await fetch(`${API_BASE}/bookings/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      flight_id: flightId,
      passenger_name: passenger.name,
      passenger_email: passenger.email
    })
  });
  return res.json();
}

async function getBooking(pnr) {
  const res = await fetch(`${API_BASE}/bookings/${pnr}`);
  return res.json();
}
