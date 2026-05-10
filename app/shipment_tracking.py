from fastapi import APIRouter, HTTPException, Depends, Request
import re
import httpx
from .psw_client import PSWClient

router = APIRouter()

def get_psw_client(request: Request):
    client = getattr(request.app.state, "psw_client", None)
    if client:
        return client
    return PSWClient()

@router.get("/track/{gd_number}")
async def track_shipment(gd_number: str, psw_client: PSWClient = Depends(get_psw_client)):
    # Simple validation: GD number should follow a specific format (e.g., GD-YYYY-NNNN)
    if not re.match(r"^GD-\d{4}-\d{4}$", gd_number):
        raise HTTPException(status_code=400, detail="Invalid GD number format. Expected format: GD-YYYY-NNNN")

    try:
        status = await psw_client.get_gd_status(gd_number)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"External PSW service error: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Could not reach PSW service: {e}")

    if status is None:
        raise HTTPException(status_code=404, detail="Shipment not found for the given GD number")

    return status
