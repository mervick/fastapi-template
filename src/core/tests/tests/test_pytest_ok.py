import pytest
from httpx import AsyncClient


async def test_pytest_ok() -> None:
    with pytest.raises(ZeroDivisionError):
        assert 1 / 0


async def test_health(api_client: AsyncClient) -> None:
    await api_client.get("health")


async def test_health_404(api_client: AsyncClient) -> None:
    response = await api_client.get("health/404")
    assert response.status_code == 404
