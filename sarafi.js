const rates = { USD: 42000, EUR: 45000, IRR: 1 };

document.getElementById('convert').addEventListener('click', () => {
  const from = document.getElementById('from').value;
  const to = document.getElementById('to').value;
  const amount = parseFloat(document.getElementById('amount').value);
  if (isNaN(amount)) return;
  const result = amount * (rates[from] / rates[to]);
  document.getElementById('result').textContent = result.toFixed(2);
});
