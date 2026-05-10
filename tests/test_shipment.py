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
    # Inject the mock client into app state
    app.state.psw_client = PSWClient(base_url="http://test", client=client)

    response = await client.get("/api/v1/track/GD-2023-1234")

    assert response.status_code == 200
    assert response.json()["status"] == "Cleared"
    assert response.json()["gd_number"] == "GD-2023-1234"

    # Cleanup
    if hasattr(app.state, "psw_client"):
        del app.state.psw_client

@pytest.mark.asyncio
async def test_track_shipment_invalid_format(client):
    response = await client.get("/api/v1/track/INVALID-GD")
    assert response.status_code == 400
    assert "Invalid GD number format" in response.json()["detail"]

@pytest.mark.asyncio
async def test_track_shipment_not_found(client):
    # Inject the mock client into app state
    app.state.psw_client = PSWClient(base_url="http://test", client=client)

    response = await client.get("/api/v1/track/GD-2023-0000")

    assert response.status_code == 404
    assert "Shipment not found" in response.json()["detail"]

    # Cleanup
    if hasattr(app.state, "psw_client"):
        del app.state.psw_client

@pytest.mark.asyncio
async def test_track_shipment_service_error(client, monkeypatch):
    # We want to mock the request that PSWClient makes *internally*
    # Since PSWClient is using the `client` we passed in, and that `client` is
    # configured with ASGITransport(app=app), the call to `client.get` inside
    # track_shipment (which goes to /api/v1/track/...) is what we call from the test.
    # Inside the app, PSWClient calls `client.get` to `http://test/mock-psw/...`.

    original_get = client.get

    async def mock_get(url, *args, **kwargs):
        if "/mock-psw/" in str(url):
            # Return a response that will trigger raise_for_status()
            resp = Response(500, content=b"Internal Server Error")
            # We need to set the request on the response because raise_for_status uses it
            resp.request = httpx.Request("GET", url)
            return resp
        return await original_get(url, *args, **kwargs)

    monkeypatch.setattr(client, "get", mock_get)

    app.state.psw_client = PSWClient(base_url="http://test", client=client)

    response = await client.get("/api/v1/track/GD-2023-1234")

    assert response.status_code == 502
    assert "External PSW service error" in response.json()["detail"]

    # Cleanup
    if hasattr(app.state, "psw_client"):
        del app.state.psw_client
