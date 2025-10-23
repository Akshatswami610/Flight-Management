const form = document.getElementById("bookingForm");
const statusDiv = document.getElementById("status");
const flightId = localStorage.getItem("selectedFlightId");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;

  const booking = await bookFlight(flightId, { name, email });

  if (booking.pnr) {
    statusDiv.innerHTML = `
      ✅ Booking confirmed!<br>
      <strong>PNR:</strong> ${booking.pnr}
      <br><br>
      <button onclick="viewReceipt('${booking.pnr}')">View Receipt</button>
    `;
  } else {
    statusDiv.textContent = "❌ Booking failed.";
  }
});

function viewReceipt(pnr) {
  localStorage.setItem("pnr", pnr);
  window.location.href = "receipt.html";
}
