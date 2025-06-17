let allData = [];
let filteredData = [];

window.onload = async () => {
  try {
    document.getElementById("loader").style.display = "block";

    // Load local static JSON file instead of Flask API
    const response = await fetch("http://localhost:5000/api/transactions")



    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    allData = await response.json();

    // Ensure a consistent datetime field
    allData = allData.map(tx => ({
      ...tx,
      datetime: tx.transaction_date || tx.datetime || null
    }));

    populateTypeFilter();
    filteredData = [...allData];
    renderTable(filteredData);
    renderCharts(filteredData); // from charts.js
  } catch (error) {
    console.error("Failed to load transactions:", error);
    alert("Error loading data. Make sure 'cleaned_transactions.json' is in the same folder as this HTML file.");
  } finally {
    document.getElementById("loader").style.display = "none";
  }
};

function populateTypeFilter() {
  const typeSelect = document.getElementById("filterType");
  typeSelect.innerHTML = '<option value="all">All</option>';

  const types = Array.from(new Set(allData.map(tx => tx.transaction_type))).sort();
  types.forEach(type => {
    const option = document.createElement("option");
    option.value = type;
    option.textContent = type;
    typeSelect.appendChild(option);
  });
}

document.getElementById("applyFilters").addEventListener("click", applyFilters);

document.getElementById("clearFilters").addEventListener("click", () => {
  document.getElementById("searchInput").value = "";
  document.getElementById("filterType").value = "all";
  document.getElementById("startDate").value = "";
  document.getElementById("endDate").value = "";
  document.getElementById("minAmount").value = "";
  document.getElementById("maxAmount").value = "";

  filteredData = [...allData];
  renderTable(filteredData);
  renderCharts(filteredData);
});

document.getElementById("searchInput").addEventListener("input", applyFilters);

function applyFilters() {
  const searchTerm = document.getElementById("searchInput").value.toLowerCase();
  const selectedType = document.getElementById("filterType").value;
  const minAmount = parseFloat(document.getElementById("minAmount").value) || 0;
  const maxAmount = parseFloat(document.getElementById("maxAmount").value) || Infinity;
  const startDateInput = document.getElementById("startDate").value;
  const endDateInput = document.getElementById("endDate").value;
  const startDate = startDateInput ? new Date(startDateInput) : null;
  const endDate = endDateInput ? new Date(endDateInput) : null;

  filteredData = allData.filter(tx => {
    const typeMatch = selectedType === "all" || tx.transaction_type === selectedType;
    const amount = parseFloat(tx.amount) || 0;
    const amountMatch = amount >= minAmount && amount <= maxAmount;

    const txDate = tx.datetime ? new Date(tx.datetime) : null;
    const dateMatch =
      (!startDate || (txDate && txDate >= startDate)) &&
      (!endDate || (txDate && txDate <= endDate));

    const searchMatch =
      searchTerm === "" ||
      Object.values(tx).some(value =>
        String(value).toLowerCase().includes(searchTerm)
      );

    return typeMatch && amountMatch && dateMatch && searchMatch;
  });

  renderTable(filteredData);
  renderCharts(filteredData);
}

function renderTable(data) {
  const tbody = document.querySelector("#transactionTable tbody");
  tbody.innerHTML = "";

  if (data.length === 0) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 4;
    td.style.textAlign = "center";
    td.textContent = "No transactions found.";
    tr.appendChild(td);
    tbody.appendChild(tr);
    return;
  }

  data.forEach(tx => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${tx.transaction_type || "-"}</td>
      <td>${tx.amount ?? "-"}</td>
      <td>${tx.datetime ? new Date(tx.datetime).toLocaleString() : "-"}</td>
      <td>${tx.receiver !== undefined && tx.receiver !== null ? tx.receiver : "-"}</td>
    `;
    tr.addEventListener("click", () => showDetails(tx));
    tbody.appendChild(tr);
  });
}

function showDetails(tx) {
  const details = `
Transaction Type: ${tx.transaction_type || "-"}
Amount: ${tx.amount ?? "-"} RWF
Date: ${tx.datetime ? new Date(tx.datetime).toLocaleString() : "-"}
Sender: ${tx.sender || "-"}
Receiver: ${tx.receiver !== undefined && tx.receiver !== null ? tx.receiver : "-"}
Balance: ${tx.balance ?? "-"}
Transaction ID: ${tx.transaction_id || "-"}
Raw Message:
${tx.raw_body || "-"}
  `.trim();

  document.getElementById("transactionDetails").textContent = details;
}
