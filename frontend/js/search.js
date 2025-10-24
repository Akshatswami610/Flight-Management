const form = document.getElementById("searchForm")
const tableBody = document.querySelector("#flightsTable tbody")
const resultsSection = document.getElementById("results")
const emptyState = document.getElementById("emptyState")
const resultsLoading = document.getElementById("resultsLoading")
const resultsContent = document.getElementById("resultsContent")
const searchError = document.getElementById("searchError")

async function fetchFlights(origin, destination, date) {
  // Mock implementation of fetchFlights
  return [
    {
      id: 1,
      airline: "Airline A",
      flight_no: "AA100",
      departure: new Date(),
      arrival: new Date(),
      price: 150,
      seats_available: 50,
    },
    {
      id: 2,
      airline: "Airline B",
      flight_no: "BB200",
      departure: new Date(),
      arrival: new Date(),
      price: 200,
      seats_available: 30,
    },
  ]
}

function formatDateTime(date) {
  return date.toLocaleString()
}

function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(amount)
}

form.addEventListener("submit", async (e) => {
  e.preventDefault()

  const origin = document.getElementById("origin").value.trim().toUpperCase()
  const destination = document.getElementById("destination").value.trim().toUpperCase()
  const date = document.getElementById("date").value

  // Validate inputs
  if (!origin || !destination || !date) {
    searchError.innerHTML = '<div class="status error">Please fill in all fields</div>'
    return
  }

  if (origin === destination) {
    searchError.innerHTML = '<div class="status error">Origin and destination cannot be the same</div>'
    return
  }

  searchError.innerHTML = ""
  emptyState.style.display = "none"
  resultsSection.style.display = "block"
  resultsLoading.style.display = "block"
  resultsContent.style.display = "none"

  try {
    const flights = await fetchFlights(origin, destination, date)

    tableBody.innerHTML = ""

    if (!flights || flights.length === 0) {
      resultsLoading.style.display = "none"
      resultsContent.innerHTML =
        '<p style="text-align: center; color: var(--text-secondary); padding: 40px;">No flights found for your search. Try different dates or cities.</p>'
      resultsContent.style.display = "block"
      return
    }

    flights.forEach((f) => {
      const departureTime = formatDateTime(f.departure)
      const arrivalTime = formatDateTime(f.arrival)
      const price = formatCurrency(f.price)

      const row = `
        <tr>
          <td>${f.airline}</td>
          <td><strong>${f.flight_no}</strong></td>
          <td>${departureTime}</td>
          <td>${arrivalTime}</td>
          <td><strong>${price}</strong></td>
          <td>${f.seats_available}</td>
          <td><button onclick="bookNow(${f.id})" style="padding: 8px 16px; font-size: 13px;">Book</button></td>
        </tr>
      `
      tableBody.insertAdjacentHTML("beforeend", row)
    })

    resultsLoading.style.display = "none"
    resultsContent.style.display = "block"
  } catch (error) {
    resultsLoading.style.display = "none"
    resultsContent.innerHTML = `<div class="status error">${error.message}</div>`
    resultsContent.style.display = "block"
  }
})

function bookNow(flightId) {
  Storage.set("selectedFlightId", flightId)
  window.location.href = "booking.html"
}
