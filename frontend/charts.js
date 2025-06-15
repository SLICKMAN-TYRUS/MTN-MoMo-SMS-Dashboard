let volumeByTypeChart, monthlySummaryChart, paymentsVsDepositsChart;

function renderCharts(data) {
  const ctx1 = document.getElementById("volumeByTypeChart").getContext("2d");
  const ctx2 = document.getElementById("monthlySummaryChart").getContext("2d");
  const ctx3 = document.getElementById("paymentsVsDepositsChart").getContext("2d");

  // Prepare data aggregations
  const typeTotals = {};
  const monthTotals = {};
  let paymentsTotal = 0;
  let depositsTotal = 0;

  data.forEach(tx => {
    const type = tx.transaction_type || "Unknown";
    const amount = parseFloat(tx.amount) || 0;
    const month = (tx.datetime || "").slice(0, 7); // YYYY-MM

    // Sum by type
    typeTotals[type] = (typeTotals[type] || 0) + amount;

    // Sum by month
    if (month) monthTotals[month] = (monthTotals[month] || 0) + amount;

    // Sum payments vs deposits (simple heuristic)
    if (type.toLowerCase().includes("payment")) paymentsTotal += amount;
    else if (type.toLowerCase().includes("deposit")) depositsTotal += amount;
  });

  // Sort months for line chart
  const sortedMonths = Object.keys(monthTotals).sort();

  // Destroy old charts if they exist
  volumeByTypeChart?.destroy();
  monthlySummaryChart?.destroy();
  paymentsVsDepositsChart?.destroy();

  // Chart 1: Bar chart - Total Volume by Transaction Type
  volumeByTypeChart = new Chart(ctx1, {
    type: "bar",
    data: {
      labels: Object.keys(typeTotals),
      datasets: [{
        label: "Total Volume (RWF)",
        data: Object.values(typeTotals),
        backgroundColor: "#ffd500" // MTN Yellow
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Total Transaction Volume by Type",
          color: "#002c5f",
          font: { size: 18, weight: "700" }
        },
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: "#002c5f" },
          grid: { color: "#eee" }
        },
        x: {
          ticks: { color: "#002c5f" },
          grid: { display: false }
        }
      }
    }
  });

  // Chart 2: Line chart - Monthly Transaction Volume
  monthlySummaryChart = new Chart(ctx2, {
    type: "line",
    data: {
      labels: sortedMonths,
      datasets: [{
        label: "Monthly Volume (RWF)",
        data: sortedMonths.map(m => monthTotals[m]),
        borderColor: "#002c5f",
        backgroundColor: "rgba(0, 44, 95, 0.2)",
        fill: true,
        tension: 0.3,
        pointRadius: 5,
        pointHoverRadius: 7
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Monthly Transaction Volume Trend",
          color: "#002c5f",
          font: { size: 18, weight: "700" }
        },
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: "#002c5f" },
          grid: { color: "#eee" }
        },
        x: {
          ticks: { color: "#002c5f" },
          grid: { display: false }
        }
      }
    }
  });

  // Chart 3: Pie chart - Payments vs Deposits Distribution
  paymentsVsDepositsChart = new Chart(ctx3, {
    type: "pie",
    data: {
      labels: ["Payments", "Deposits", "Others"],
      datasets: [{
        data: [paymentsTotal, depositsTotal, Math.max(0, Object.values(typeTotals).reduce((a, b) => a + b, 0) - paymentsTotal - depositsTotal)],
        backgroundColor: [
          "#ffd500",    // Yellow for Payments
          "#002c5f",    // Dark Blue for Deposits
          "#888888"     // Gray for Others
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Distribution of Payments vs Deposits",
          color: "#002c5f",
          font: { size: 18, weight: "700" }
        },
        legend: {
          position: "bottom",
          labels: { color: "#002c5f", font: { size: 14 } }
        }
      }
    }
  });
}
