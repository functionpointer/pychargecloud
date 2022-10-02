import pydantic
from aiohttp import ClientSession, ClientResponse
from yarl import URL
from .models import *
import logging

DEFAULT_URL = "https://app.chargecloud.de/emobility:ocpi/6336fe713f2eb7fa04b97ff6651b76f8/app/2.0/locations"


class Api:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession, base_url: str | None = None):
        """Initialize the auth."""
        self.websession = websession
        self.base_url = URL(base_url or DEFAULT_URL)
        self.logger = logging.getLogger("chargecloudapi")

    async def location_by_evse_id(self, evse_id: str, **kwargs) -> list[Location]:
        response = await self.request("GET", self.base_url % {"evse": evse_id})
        response.raise_for_status()
        json = await response.json()
        self.logger.debug(f"got json {json}")
        try:
            resp = Response.parse_obj(json)
            return resp.data
        except pydantic.ValidationError as e:
            self.logger.error(f"json was {json}")
            self.logger.exception(e)
            raise e

    async def request(self, method: str, url: URL, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        return await self.websession.request(
            method,
            url,
            **kwargs,
            headers=headers,
        )
