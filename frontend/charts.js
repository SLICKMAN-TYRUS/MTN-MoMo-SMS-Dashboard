let volumeByTypeChart, monthlySummaryChart, paymentsVsDepositsChart;

function renderCharts(data) {
  const ctx1 = document.getElementById("volumeByTypeChart").getContext("2d");
  const ctx2 = document.getElementById("monthlySummaryChart").getContext("2d");
  const ctx3 = document.getElementById("paymentsVsDepositsChart").getContext("2d");

  // Reset previous charts
  volumeByTypeChart?.destroy();
  monthlySummaryChart?.destroy();
  paymentsVsDepositsChart?.destroy();

  const typeTotals = {};
  const monthTotals = {};
  let paymentsTotal = 0;
  let depositsTotal = 0;

  data.forEach(tx => {
    const type = tx.transaction_type || "Unknown";
    const amount = parseFloat(tx.amount) || 0;
    const month = (tx.datetime || "").slice(0, 7); // YYYY-MM

    typeTotals[type] = (typeTotals[type] || 0) + amount;
    if (month) monthTotals[month] = (monthTotals[month] || 0) + amount;

    if (type.toLowerCase().includes("payment")) paymentsTotal += amount;
    else if (type.toLowerCase().includes("deposit")) depositsTotal += amount;
  });

  const sortedMonths = Object.keys(monthTotals).sort();
  const complementaryColors = [
    "#00c7b1", // Turquoise
    "#ff6b6b", // Coral
    "#6c5ce7", // Purple
    "#f5f5f5"  // Light Gray
  ];

  // Volume by Type - Bar Chart
  volumeByTypeChart = new Chart(ctx1, {
    type: "bar",
    data: {
      labels: Object.keys(typeTotals),
      datasets: [{
        label: "Total Volume (RWF)",
        data: Object.values(typeTotals),
        backgroundColor: Object.keys(typeTotals).map((_, i) =>
          [ "#ffd500", "#002c5f", ...complementaryColors ][i % 6]
        ),
        borderRadius: 6,
        hoverOffset: 10
      }]
    },
    options: {
      responsive: true,
      animation: {
        duration: 1000,
        easing: "easeOutBounce"
      },
      plugins: {
        title: {
          display: true,
          text: "Total Transaction Volume by Type",
          color: "#002c5f",
          font: { size: 20, weight: "bold" }
        },
        tooltip: {
          backgroundColor: "#002c5f",
          titleColor: "#fff",
          bodyColor: "#ffd500"
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

  // Monthly Trend - Line Chart
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
        tension: 0.4,
        pointBackgroundColor: "#ffd500",
        pointHoverRadius: 7
      }]
    },
    options: {
      responsive: true,
      animation: {
        duration: 1200,
        easing: "easeInOutQuart"
      },
      plugins: {
        title: {
          display: true,
          text: "Monthly Transaction Volume Trend",
          color: "#002c5f",
          font: { size: 20, weight: "bold" }
        },
        tooltip: {
          backgroundColor: "#ffd500",
          titleColor: "#002c5f",
          bodyColor: "#002c5f"
        },
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: "#002c5f" },
          grid: { color: "#f0f0f0" }
        },
        x: {
          ticks: { color: "#002c5f" },
          grid: { display: false }
        }
      }
    }
  });

  // Payments vs Deposits - Donut Chart
  const otherTotal = Math.max(0, Object.values(typeTotals).reduce((a, b) => a + b, 0) - paymentsTotal - depositsTotal);

  paymentsVsDepositsChart = new Chart(ctx3, {
    type: "doughnut",
    data: {
      labels: ["Payments", "Deposits", "Others"],
      datasets: [{
        data: [paymentsTotal, depositsTotal, otherTotal],
        backgroundColor: ["#ffd500", "#002c5f", "#888888"],
        hoverOffset: 12
      }]
    },
    options: {
      responsive: true,
      cutout: "60%",
      animation: {
        animateRotate: true,
        duration: 1500
      },
      plugins: {
        title: {
          display: true,
          text: "Distribution of Payments vs Deposits",
          color: "#002c5f",
          font: { size: 20, weight: "bold" }
        },
        tooltip: {
          backgroundColor: "#002c5f",
          titleColor: "#fff",
          bodyColor: "#ffd500"
        },
        legend: {
          position: "bottom",
          labels: {
            color: "#002c5f",
            font: { size: 14 }
          }
        }
      }
    }
  });
}
