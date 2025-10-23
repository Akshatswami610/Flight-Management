const pnr = localStorage.getItem("pnr");
const receiptDiv = document.getElementById("receiptData");

async function loadReceipt() {
  const data = await getBooking(pnr);
  receiptDiv.textContent = JSON.stringify(data, null, 2);
}

document.getElementById("downloadBtn").addEventListener("click", () => {
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(receiptDiv.textContent);
  const link = document.createElement("a");
  link.href = dataStr;
  link.download = `receipt_${pnr}.json`;
  link.click();
});

loadReceipt();
