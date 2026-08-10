import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

pytestmark = [pytest.mark.api, pytest.mark.anyio]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def api_client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


async def test_health_confirms_database_connection(api_client: AsyncClient) -> None:
    response = await api_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}


async def test_quality_summary_exposes_known_dataset(
    api_client: AsyncClient,
) -> None:
    response = await api_client.get("/api/quality/summary")

    assert response.status_code == 200
    summary = response.json()
    assert summary["total_transactions"] == 4825
    assert summary["inconsistent_transactions"] == 200
    assert summary["transactions_without_items"] == 100
    assert float(summary["inconsistency_rate"]) == pytest.approx(0.0415)
    assert summary["first_transaction_date"] <= summary["last_transaction_date"]


async def test_inconsistent_filter_returns_only_flagged_rows(
    api_client: AsyncClient,
) -> None:
    response = await api_client.get(
        "/api/transactions",
        params={"only_inconsistent": True, "limit": 10},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["count"] == 10
    assert result["only_inconsistent"] is True
    assert all(item["inconsistent_amount_flag"] == 1 for item in result["items"])


async def test_transaction_detail_returns_404_for_unknown_id(
    api_client: AsyncClient,
) -> None:
    response = await api_client.get("/api/transactions/999999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Transacción no encontrada."


async def test_transaction_limit_is_validated(api_client: AsyncClient) -> None:
    response = await api_client.get("/api/transactions", params={"limit": 101})

    assert response.status_code == 422
