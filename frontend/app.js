let allData = [];
let filteredData = [];

window.onload = async () => {
  try {
    const response = await fetch("cleaned_transactions.json");
    allData = await response.json();

    populateTypeFilter();
    filteredData = [...allData];
    renderTable(filteredData);
    renderCharts(filteredData);
  } catch (error) {
    console.error("Failed to load transactions:", error);
  }
};

function populateTypeFilter() {
  const typeSelect = document.getElementById("filterType");
  const types = Array.from(new Set(allData.map(tx => tx.transaction_type))).sort();
  types.forEach(type => {
    const option = document.createElement("option");
    option.value = type;
    option.textContent = type;
    typeSelect.appendChild(option);
  });
}

document.getElementById("applyFilters").addEventListener("click", () => {
  applyFilters();
});

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

document.getElementById("searchInput").addEventListener("input", () => {
  applyFilters();
});

function applyFilters() {
  const searchTerm = document.getElementById("searchInput").value.toLowerCase();
  const selectedType = document.getElementById("filterType").value;
  const minAmount = parseFloat(document.getElementById("minAmount").value) || 0;
  const maxAmount = parseFloat(document.getElementById("maxAmount").value) || Infinity;
  const startDate = new Date(document.getElementById("startDate").value);
  const endDate = new Date(document.getElementById("endDate").value);

  filteredData = allData.filter(tx => {
    const typeMatch = selectedType === "all" || tx.transaction_type === selectedType;
    const amount = parseFloat(tx.amount) || 0;
    const amountMatch = amount >= minAmount && amount <= maxAmount;
    const date = new Date(tx.datetime);
    const dateMatch =
      (isNaN(startDate) || date >= startDate) &&
      (isNaN(endDate) || date <= endDate);

    const searchMatch =
      searchTerm === "" ||
      JSON.stringify(tx).toLowerCase().includes(searchTerm);

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
      <td>${tx.receiver || "-"}</td>
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
Receiver: ${tx.receiver || "-"}
Balance: ${tx.balance ?? "-"}
Transaction ID: ${tx.transaction_id || "-"}
Raw Message:
${tx.raw_body || "-"}
  `.trim();

  document.getElementById("transactionDetails").textContent = details;
}
