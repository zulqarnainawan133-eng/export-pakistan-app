import pytest
from app.raast_service import raast_service
from app.database import db

@pytest.mark.asyncio
async def test_release_funds_success():
    # GD-2023-1234 is 'Cleared' in the mock database
    gd_number = "GD-2023-1234"
    result = await raast_service.release_funds(gd_number)

    assert result["success"] is True
    assert "released to farmer" in result["message"]

@pytest.mark.asyncio
async def test_release_funds_fails_if_not_cleared():
    # GD-2023-5678 is 'In Progress' in the mock database
    gd_number = "GD-2023-5678"
    result = await raast_service.release_funds(gd_number)

    assert result["success"] is False
    assert "must be 'Cleared'" in result["error"]

@pytest.mark.asyncio
async def test_release_funds_fails_if_not_found():
    gd_number = "GD-0000-0000"
    result = await raast_service.release_funds(gd_number)

    assert result["success"] is False
    assert "Shipment not found" in result["error"]

@pytest.mark.asyncio
async def test_release_funds_after_status_update():
    gd_number = "GD-2023-9999" # Currently 'Pending'

    # First attempt should fail
    result1 = await raast_service.release_funds(gd_number)
    assert result1["success"] is False

    # Update status to 'Cleared'
    db.update_shipment_status(gd_number, "Cleared")

    # Second attempt should succeed
    result2 = await raast_service.release_funds(gd_number)
    assert result2["success"] is True
