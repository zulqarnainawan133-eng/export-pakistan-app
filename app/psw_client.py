import httpx
from typing import Dict, Any, Optional

class PSWClient:
    def __init__(self, base_url: str = "http://localhost:8000", client: Optional[httpx.AsyncClient] = None):
        self.base_url = base_url
        self.client = client

    async def get_gd_status(self, gd_number: str) -> Optional[Dict[str, Any]]:
        """
        Fetches GD status.
        Returns the data if found (200), None if not found (404),
        and raises httpx.HTTPStatusError for other status codes.
        """
        if self.client:
            return await self._make_request(self.client, gd_number)

        async with httpx.AsyncClient() as client:
            return await self._make_request(client, gd_number)

    async def _make_request(self, client: httpx.AsyncClient, gd_number: str) -> Optional[Dict[str, Any]]:
        response = await client.get(f"{self.base_url}/mock-psw/{gd_number}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
