// Money shown as a profit or loss, e.g. +£12.50, -£4.00, £0.00.
export function formatPnL(amount) {
  const sign = amount > 0 ? '+' : amount < 0 ? '-' : '';
  return `${sign}£${Math.abs(amount).toFixed(2)}`;
}

// Whole pounds for chart axis labels, e.g. £20, -£40.
export function formatPounds(amount) {
  return amount < 0 ? `-£${Math.abs(amount)}` : `£${amount}`;
}
