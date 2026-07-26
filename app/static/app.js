const statusElement = document.querySelector("#api-status");
const errorElement = document.querySelector("#error-message");
const filterElement = document.querySelector("#only-inconsistent");
const tableBody = document.querySelector("#transactions-body");

function money(value) {
  return new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
    minimumFractionDigits: 2,
  }).format(Number(value));
}

async function requestJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`La consulta ${url} respondió ${response.status}.`);
  }
  return response.json();
}

async function loadHealth() {
  try {
    const health = await requestJson("/health");
    statusElement.textContent = health.database === "connected"
      ? "API y PostgreSQL conectados"
      : "Conexión incompleta";
    statusElement.className = "status-ok";
  } catch (error) {
    statusElement.textContent = "API sin conexión a PostgreSQL";
    statusElement.className = "status-error";
    throw error;
  }
}

async function loadSummary() {
  const summary = await requestJson("/api/quality/summary");
  document.querySelector('[data-testid="total-transactions"]').textContent =
    summary.total_transactions.toLocaleString("es-AR");
  document.querySelector('[data-testid="inconsistent-transactions"]').textContent =
    summary.inconsistent_transactions.toLocaleString("es-AR");
  document.querySelector('[data-testid="inconsistency-rate"]').textContent =
    `${(Number(summary.inconsistency_rate) * 100).toFixed(2)}%`;
  document.querySelector('[data-testid="without-items"]').textContent =
    summary.transactions_without_items.toLocaleString("es-AR");
}

function transactionRow(transaction) {
  const row = document.createElement("tr");
  row.dataset.testid = "transaction-row";
  const result = transaction.inconsistent_amount_flag === 1
    ? '<span class="badge badge-error">Inconsistente</span>'
    : '<span class="badge badge-ok">Consistente</span>';
  row.innerHTML = `
    <td>${transaction.transaction_id}</td>
    <td>${money(transaction.transaction_amount)}</td>
    <td>${money(transaction.calculated_item_amount)}</td>
    <td>${money(transaction.amount_difference)}</td>
    <td>${transaction.item_count}</td>
    <td>${result}</td>
  `;
  return row;
}

async function loadTransactions() {
  const onlyInconsistent = filterElement.checked;
  const result = await requestJson(
    `/api/transactions?only_inconsistent=${onlyInconsistent}&limit=20`,
  );
  tableBody.replaceChildren(...result.items.map(transactionRow));
}

async function loadDashboard() {
  errorElement.hidden = true;
  try {
    await Promise.all([loadHealth(), loadSummary(), loadTransactions()]);
  } catch (error) {
    errorElement.textContent = error.message;
    errorElement.hidden = false;
  }
}

document.querySelector("#refresh-button").addEventListener("click", loadDashboard);
filterElement.addEventListener("change", loadTransactions);
loadDashboard();
