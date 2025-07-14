"""API Client for the Flatlib Natal Chart Add-on."""
import aiohttp
import asyncio
from typing import Dict, Any

class ApiClient:
    """API Client to communicate with the Flatlib server."""

    def __init__(self, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self._session = session
        # Supervisor DNS резолвит slug аддона в его IP-адрес
        self._api_url = f"http://flatlib_server:8080/natal"

    async def get_natal_chart(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Get natal chart data from the add-on."""
        try:
            async with self._session.post(self._api_url, json=payload) as response:
                response.raise_for_status()
                return await response.json()
        except asyncio.TimeoutError:
            raise ApiError("Timeout communicating with API")
        except aiohttp.ClientError as err:
            raise ApiError(f"Error communicating with API: {err}")

class ApiError(Exception):
    """Exception to indicate a general API error."""