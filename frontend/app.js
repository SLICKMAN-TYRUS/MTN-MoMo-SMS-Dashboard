// app.js

let allData = [];

window.onload = async function () {
  try {
    const response = await fetch("cleaned_transactions.json");
    allData = await response.json();

    populateTypeFilter();
    renderTable(allData);
    renderCharts(allData); // from charts.js
  } catch (err) {
    console.error("Failed to load data:", err);
  }
};

// Populate transaction type dropdown
function populateTypeFilter() {
  const filter = document.getElementById("filterType");
  const types = [...new Set(allData.map(tx => tx.transaction_type))];
  types.sort().forEach(type => {
    const opt = document.createElement("option");
    opt.value = type;
    opt.textContent = type;
    filter.appendChild(opt);
  });
}

// Filter logic
document.getElementById("applyFilters").addEventListener("click", () => {
  const type = document.getElementById("filterType").value;
  const min = parseInt(document.getElementById("minAmount").value) || 0;
  const max = parseInt(document.getElementById("maxAmount").value) || Infinity;
  const start = new Date(document.getElementById("startDate").value);
  const end = new Date(document.getElementById("endDate").value);

  const filtered = allData.filter(tx => {
    const amount = tx.amount || 0;
    const date = new Date(tx.datetime || "");
    return (
      (type === "all" || tx.transaction_type === type) &&
      amount >= min &&
      amount <= max &&
      (!isNaN(start) ? date >= start : true) &&
      (!isNaN(end) ? date <= end : true)
    );
  });

  renderTable(filtered);
  renderCharts(filtered);
});

// Render transaction table
function renderTable(data) {
  const tbody = document.querySelector("#transactionTable tbody");
  tbody.innerHTML = "";

  data.forEach(tx => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${tx.transaction_type}</td>
      <td>${tx.amount ?? "-"}</td>
      <td>${tx.datetime ?? "-"}</td>
      <td>${tx.receiver ?? "-"}</td>
    `;
    row.addEventListener("click", () => showDetails(tx));
    tbody.appendChild(row);
  });
}

// Show full transaction details
function showDetails(tx) {
  const details = `
Transaction Type: ${tx.transaction_type}
Amount: ${tx.amount ?? "-"} RWF
Date: ${tx.datetime ?? "-"}
Sender: ${tx.sender ?? "-"}
Receiver: ${tx.receiver ?? "-"}
Balance: ${tx.balance ?? "-"}
Transaction ID: ${tx.transaction_id ?? "-"}
Raw Message:
${tx.raw_body}
  `.trim();

  document.getElementById("transactionDetails").textContent = details;
}
