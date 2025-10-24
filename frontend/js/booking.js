const form = document.getElementById("bookingForm")
const statusDiv = document.getElementById("status")
const formError = document.getElementById("formError")
const flightId = Storage.get("selectedFlightId")

// Declare validation functions
function validateName(name) {
  return name.length >= 3
}

function validateEmail(email) {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailPattern.test(email)
}

// Declare bookFlight function
async function bookFlight(flightId, passengerDetails) {
  // Simulate booking process
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ pnr: "ABC123" })
    }, 1000)
  })
}

// Validate form on input
document.getElementById("name").addEventListener("blur", function () {
  if (this.value && !validateName(this.value)) {
    this.style.borderColor = "var(--danger)"
    formError.innerHTML = '<div class="status error">Name must be at least 3 characters</div>'
    formError.style.display = "block"
  } else {
    this.style.borderColor = ""
    formError.style.display = "none"
  }
})

document.getElementById("email").addEventListener("blur", function () {
  if (this.value && !validateEmail(this.value)) {
    this.style.borderColor = "var(--danger)"
    formError.innerHTML = '<div class="status error">Please enter a valid email address</div>'
    formError.style.display = "block"
  } else {
    this.style.borderColor = ""
    formError.style.display = "none"
  }
})

form.addEventListener("submit", async (e) => {
  e.preventDefault()

  const name = document.getElementById("name").value.trim()
  const email = document.getElementById("email").value.trim()

  // Validate inputs
  if (!validateName(name)) {
    formError.innerHTML = '<div class="status error">Please enter a valid name (at least 3 characters)</div>'
    formError.style.display = "block"
    return
  }

  if (!validateEmail(email)) {
    formError.innerHTML = '<div class="status error">Please enter a valid email address</div>'
    formError.style.display = "block"
    return
  }

  if (!flightId) {
    formError.innerHTML = '<div class="status error">No flight selected. Please go back and select a flight.</div>'
    formError.style.display = "block"
    return
  }

  formError.style.display = "none"
  const submitBtn = form.querySelector("button[type='submit']")
  submitBtn.disabled = true
  submitBtn.textContent = "Processing..."

  try {
    const booking = await bookFlight(flightId, { name, email })

    if (booking.pnr) {
      Storage.set("pnr", booking.pnr)
      Storage.set("bookingData", booking)

      statusDiv.innerHTML = `
        <div class="status success">
          <strong>Booking Confirmed!</strong><br>
          PNR: <strong>${booking.pnr}</strong><br><br>
          <button onclick="viewReceipt('${booking.pnr}')" style="margin-top: 10px;">View Receipt</button>
        </div>
      `

      setTimeout(() => {
        window.location.href = "receipt.html"
      }, 2000)
    } else {
      throw new Error("No PNR received from server")
    }
  } catch (error) {
    formError.innerHTML = `<div class="status error">${error.message}</div>`
    formError.style.display = "block"
    submitBtn.disabled = false
    submitBtn.textContent = "Confirm Booking"
  }
})

function viewReceipt(pnr) {
  Storage.set("pnr", pnr)
  window.location.href = "receipt.html"
}
