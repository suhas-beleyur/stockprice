async function getStock() {
  const s = document.getElementById('symbol').value;
  const p = document.getElementById('period').value;

  const res = await fetch(`/api/stock/${s}?period=${p}`);
  const data = await res.json();

  if (!res.ok) return alert("⚠️ No data found for this stock!");

  document.getElementById('name').innerText = data.symbol;
  document.getElementById('price').innerText =
    `Price: $${data.currentPrice.toFixed(2)} (Change: ${data.change.toFixed(2)}, ${data.changePercent.toFixed(2)}%)`;

  const x = data.history.map(h => h.date);
  const y = data.history.map(h => h.close);

  Plotly.newPlot("chart", [{
    x, y, type: 'scatter', mode: 'lines', name: s
  }], {
    title: `${s} Stock Price`,
    xaxis: { title: 'Date' },
    yaxis: { title: 'Price (USD)' },
    paper_bgcolor: '#fff',
    plot_bgcolor: '#f8f9fa'
  });
}

window.onload = getStock;
console.log("✅ Script loaded successfully!");
