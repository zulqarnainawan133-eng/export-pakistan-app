import pytest
import pytest_asyncio
import httpx
from httpx import AsyncClient, ASGITransport, Response
from app.main import app
from app.psw_client import PSWClient

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_track_shipment_success(client):
    app.state.psw_client = PSWClient(base_url="http://test", client=client)
    response = await client.get("/api/v1/track/GD-2023-1234")
    assert response.status_code == 200
    assert response.json()["status"] == "Cleared"
    if hasattr(app.state, "psw_client"):
        del app.state.psw_client

@pytest.mark.asyncio
async def test_track_shipment_invalid_format(client):
    response = await client.get("/api/v1/track/INVALID")
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_track_shipment_not_found(client):
    app.state.psw_client = PSWClient(base_url="http://test", client=client)
    response = await client.get("/api/v1/track/GD-2023-0000")
    assert response.status_code == 404
    if hasattr(app.state, "psw_client"):
        del app.state.psw_client
