class MockDatabase:
    def __init__(self):
        self.shipments = {
            "GD-2023-1234": {"status": "Cleared", "farmer_id": "FARMER-001", "amount": 1000.0},
            "GD-2023-5678": {"status": "In Progress", "farmer_id": "FARMER-002", "amount": 2500.0},
            "GD-2023-9999": {"status": "Pending", "farmer_id": "FARMER-003", "amount": 500.0},
        }

    def get_shipment(self, gd_number: str):
        return self.shipments.get(gd_number)

    def update_shipment_status(self, gd_number: str, status: str):
        if gd_number in self.shipments:
            self.shipments[gd_number]["status"] = status

db = MockDatabase()
