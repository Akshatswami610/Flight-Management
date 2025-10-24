const pnr = Storage.get("pnr")
const receiptDiv = document.getElementById("receiptData")
const receiptLoading = document.getElementById("receiptLoading")
const downloadBtn = document.getElementById("downloadBtn")

// Declare necessary functions
function getBooking(pnr) {
  // Placeholder for actual booking retrieval logic
  return new Promise((resolve, reject) => {
    // Simulate fetching booking data
    setTimeout(() => {
      if (pnr) {
        resolve({
          pnr: pnr,
          booking_date: new Date(),
          passenger_name: "John Doe",
          passenger_email: "john.doe@example.com",
          airline: "FlightHub",
          flight_no: "FH123",
          departure: new Date(),
          arrival: new Date(),
          price: 150.75,
        })
      } else {
        reject("No booking found")
      }
    }, 1000)
  })
}

function formatDate(date) {
  return date.toLocaleDateString()
}

function formatDateTime(date) {
  return date.toLocaleString()
}

function formatCurrency(amount) {
  return amount.toLocaleString("en-US", { style: "currency", currency: "USD" })
}

async function loadReceipt() {
  try {
    if (!pnr) {
      throw new Error("No booking found. Please complete a booking first.")
    }

    const data = await getBooking(pnr)

    if (!data) {
      throw new Error("Failed to load booking details")
    }

    // Format receipt data for display
    const receiptHTML = `
      <div class="receipt-section">
        <h3>Booking Information</h3>
        <div class="receipt-row">
          <span>PNR:</span>
          <strong>${data.pnr || pnr}</strong>
        </div>
        <div class="receipt-row">
          <span>Booking Date:</span>
          <span>${formatDate(data.booking_date || new Date())}</span>
        </div>
      </div>

      <div class="receipt-section">
        <h3>Passenger Details</h3>
        <div class="receipt-row">
          <span>Name:</span>
          <span>${data.passenger_name || "N/A"}</span>
        </div>
        <div class="receipt-row">
          <span>Email:</span>
          <span>${data.passenger_email || "N/A"}</span>
        </div>
      </div>

      <div class="receipt-section">
        <h3>Flight Details</h3>
        <div class="receipt-row">
          <span>Airline:</span>
          <span>${data.airline || "N/A"}</span>
        </div>
        <div class="receipt-row">
          <span>Flight Number:</span>
          <span>${data.flight_no || "N/A"}</span>
        </div>
        <div class="receipt-row">
          <span>Departure:</span>
          <span>${formatDateTime(data.departure) || "N/A"}</span>
        </div>
        <div class="receipt-row">
          <span>Arrival:</span>
          <span>${formatDateTime(data.arrival) || "N/A"}</span>
        </div>
      </div>

      <div class="receipt-section">
        <h3>Price Details</h3>
        <div class="receipt-row">
          <span>Base Fare:</span>
          <span>${formatCurrency(data.price || 0)}</span>
        </div>
        <div class="receipt-row total">
          <span>Total Amount:</span>
          <span>${formatCurrency(data.price || 0)}</span>
        </div>
      </div>

      <div class="receipt-section" style="background: var(--primary-light); padding: 15px; border-radius: 8px; margin-top: 20px;">
        <p style="color: var(--text-secondary); font-size: 13px; margin: 0;">
          A confirmation email has been sent to <strong>${data.passenger_email || "your email"}</strong>. 
          Please check your inbox for further details.
        </p>
      </div>
    `

    receiptDiv.innerHTML = receiptHTML
    receiptLoading.style.display = "none"
    receiptDiv.style.display = "block"

    // Store receipt data for download
    window.receiptData = data
  } catch (error) {
    receiptLoading.style.display = "none"
    receiptDiv.innerHTML = `<div class="status error">${error.message}</div>`
    receiptDiv.style.display = "block"
    downloadBtn.disabled = true
  }
}

// Download receipt as PDF-like text file
downloadBtn.addEventListener("click", () => {
  try {
    if (!window.receiptData) {
      throw new Error("No receipt data available")
    }

    const receiptText = `
FLIGHT BOOKING RECEIPT
${"=".repeat(50)}

PNR: ${window.receiptData.pnr || pnr}
Booking Date: ${formatDate(window.receiptData.booking_date || new Date())}

PASSENGER DETAILS
${"-".repeat(50)}
Name: ${window.receiptData.passenger_name}
Email: ${window.receiptData.passenger_email}

FLIGHT DETAILS
${"-".repeat(50)}
Airline: ${window.receiptData.airline}
Flight Number: ${window.receiptData.flight_no}
Departure: ${formatDateTime(window.receiptData.departure)}
Arrival: ${formatDateTime(window.receiptData.arrival)}

PRICE DETAILS
${"-".repeat(50)}
Base Fare: ${formatCurrency(window.receiptData.price)}
Total Amount: ${formatCurrency(window.receiptData.price)}

${"=".repeat(50)}
Thank you for booking with FlightHub!
    `

    const dataStr = "data:text/plain;charset=utf-8," + encodeURIComponent(receiptText)
    const link = document.createElement("a")
    link.href = dataStr
    link.download = `receipt_${pnr}.txt`
    link.click()
  } catch (error) {
    alert("Failed to download receipt: " + error.message)
  }
})

// Load receipt on page load
loadReceipt()
