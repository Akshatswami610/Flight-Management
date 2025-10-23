const form = document.getElementById("searchForm");
const tableBody = document.querySelector("#flightsTable tbody");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const origin = document.getElementById("origin").value;
  const destination = document.getElementById("destination").value;
  const date = document.getElementById("date").value;

  const flights = await fetchFlights(origin, destination, date);

  tableBody.innerHTML = "";
  flights.forEach(f => {
    const row = `
      <tr>
        <td>${f.airline}</td>
        <td>${f.flight_no}</td>
        <td>${new Date(f.departure).toLocaleString()}</td>
        <td>${new Date(f.arrival).toLocaleString()}</td>
        <td>${f.price}</td>
        <td>${f.seats_available}</td>
        <td><button onclick="bookNow(${f.id})">Book</button></td>
      </tr>
    `;
    tableBody.insertAdjacentHTML("beforeend", row);
  });
});

function bookNow(flightId) {
  localStorage.setItem("selectedFlightId", flightId);
  window.location.href = "booking.html";
}
