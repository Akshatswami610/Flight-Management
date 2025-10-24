const API_BASE = "http://127.0.0.1:8000"

// Fetch flights with error handling
async function fetchFlights(origin, destination, date) {
  try {
    const response = await fetch(
      `${API_BASE}/flights/search?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}&date=${date}`,
    )

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error("[v0] Flight search error:", error)
    throw new Error("Failed to fetch flights. Please try again.")
  }
}

// Book flight with validation
async function bookFlight(flightId, passenger) {
  try {
    if (!flightId || !passenger.name || !passenger.email) {
      throw new Error("Missing required booking information")
    }

    const response = await fetch(`${API_BASE}/bookings/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        flight_id: flightId,
        passenger_name: passenger.name,
        passenger_email: passenger.email,
      }),
    })

    if (!response.ok) {
      throw new Error(`Booking failed: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error("[v0] Booking error:", error)
    throw new Error("Failed to complete booking. Please try again.")
  }
}

// Get booking details with error handling
async function getBooking(pnr) {
  try {
    if (!pnr) {
      throw new Error("PNR is required")
    }

    const response = await fetch(`${API_BASE}/bookings/${pnr}`)

    if (!response.ok) {
      throw new Error(`Failed to fetch booking: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error("[v0] Get booking error:", error)
    throw new Error("Failed to load booking details. Please try again.")
  }
}
