// charts.js

let typeChart, monthlyChart, distributionChart;

function renderCharts(data) {
  const ctx1 = document.getElementById("typeChart").getContext("2d");
  const ctx2 = document.getElementById("monthlyChart").getContext("2d");
  const ctx3 = document.getElementById("distributionChart").getContext("2d");

  // Group totals by type and month
  const typeTotals = {};
  const monthTotals = {};
  let totalAmount = 0;

  data.forEach(tx => {
    const type = tx.transaction_type;
    const month = (tx.datetime || "").slice(0, 7);
    const amount = tx.amount || 0;

    totalAmount += amount;

    if (type) {
      typeTotals[type] = (typeTotals[type] || 0) + amount;
    }

    if (month) {
      monthTotals[month] = (monthTotals[month] || 0) + amount;
    }
  });

  // Clean up old charts before redrawing
  typeChart?.destroy();
  monthlyChart?.destroy();
  distributionChart?.destroy();

  // Chart 1: Bar Chart - Transaction Volume by Type
  typeChart = new Chart(ctx1, {
    type: "bar",
    data: {
      labels: Object.keys(typeTotals),
      datasets: [{
        label: "Total Volume (RWF)",
        data: Object.values(typeTotals),
        backgroundColor: "#007bff"
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Total Volume by Transaction Type"
        }
      },
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  // Chart 2: Line Chart - Monthly Trends
  const sortedMonths = Object.keys(monthTotals).sort();

  monthlyChart = new Chart(ctx2, {
    type: "line",
    data: {
      labels: sortedMonths,
      datasets: [{
        label: "Monthly Volume (RWF)",
        data: sortedMonths.map(month => monthTotals[month]),
        borderColor: "#28a745",
        backgroundColor: "rgba(40, 167, 69, 0.1)",
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Monthly Transaction Volume Trend"
        }
      },
      responsive: true
    }
  });

  // Chart 3: Pie Chart - Distribution by Type
  const typeColors = generateColors(Object.keys(typeTotals).length);

  distributionChart = new Chart(ctx3, {
    type: "pie",
    data: {
      labels: Object.keys(typeTotals),
      datasets: [{
        data: Object.values(typeTotals),
        backgroundColor: typeColors
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Distribution of Transactions by Type"
        }
      },
      responsive: true
    }
  });
}

// Utility: Generate distinct HSL colors
function generateColors(count) {
  const colors = [];
  for (let i = 0; i < count; i++) {
    const hue = Math.round((360 / count) * i);
    colors.push(`hsl(${hue}, 70%, 60%)`);
  }
  return colors;
}
