from app.database import db
from typing import Dict, Any

class RaastService:
    async def call_raast_api(self, farmer_id: str, amount: float) -> bool:
        """
        Mock RAAST API call.
        """
        print(f"RAAST: Releasing {amount} to farmer {farmer_id}")
        return True

    async def release_funds(self, gd_number: str) -> Dict[str, Any]:
        shipment = db.get_shipment(gd_number)

        if not shipment:
            return {"success": False, "error": "Shipment not found"}

        if shipment["status"] != "Cleared":
            return {
                "success": False,
                "error": f"Funds cannot be released. Shipment status is '{shipment['status']}', but must be 'Cleared'."
            }

        # Call RAAST API
        payment_success = await self.call_raast_api(shipment["farmer_id"], shipment["amount"])

        if payment_success:
            return {"success": True, "message": f"Funds of {shipment['amount']} released to farmer {shipment['farmer_id']}"}
        else:
            return {"success": False, "error": "RAAST payment failed"}

raast_service = RaastService()
