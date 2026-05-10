from fastapi import FastAPI, HTTPException
from .shipment_tracking import router as shipment_router

app = FastAPI(title="Trade-Tech Platform API")

app.include_router(shipment_router, prefix="/api/v1")

MOCK_PSW_DATA = {
    "GD-2023-1234": {"gd_number": "GD-2023-1234", "status": "Cleared", "location": "Karachi Port"},
    "GD-2023-5678": {"gd_number": "GD-2023-5678", "status": "In Progress", "location": "Port Qasim"},
}

@app.get("/mock-psw/{gd_number}")
async def mock_psw_endpoint(gd_number: str):
    if gd_number in MOCK_PSW_DATA:
        return MOCK_PSW_DATA[gd_number]
    raise HTTPException(status_code=404, detail="GD not found in PSW records")
