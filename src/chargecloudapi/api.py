import datetime

import pydantic
from aiohttp import ClientSession, ClientResponse
from yarl import URL
from .models import *
import logging

operatorIDs = [
    OperatorID(name="maingau", op_id="606a0da0dfdd338ee4134605653d4fd8"),
    OperatorID(name="SW Kiel", op_id="6336fe713f2eb7fa04b97ff6651b76f8"),
    OperatorID(name="Rheinenergie", op_id="c4ce9bb82a86766833df8a4818fa1b5c"),
]


class Api:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession):
        """Initialize the auth."""
        self.websession = websession
        self.logger = logging.getLogger("chargecloudapi")

    async def perform_smart_api_call(
        self, evse_id: str, call_data: SmartCallData | None
    ) -> tuple[Location | None, SmartCallData]:
        """
        Perform API request with automatic operatorId choice.

        When calling for a specific evse for the first time, set call_data = None.
        This function will automatically try some operatorIDs and find the best one.
        It will then return a SmartCallData along with the result.

        If you want to repeat the API request, specify the SmartCallData object for improved efficiency.
        """

        if call_data is None:
            call_data = SmartCallData(
                evse_id=evse_id,
                last_call=datetime.datetime.now().isoformat(),
                operator_id=None,
            )
        if call_data.evse_id != evse_id:
            raise ValueError("call_data does not fit to evse_id")

        ret = None
        if call_data.operator_id is not None:
            ret = await self.location_by_evse_id(evse_id, call_data.operator_id)
            if len(ret) == 0:
                self.logger.warning(f"empty resp from {call_data.operator_id.name}")
                call_data.operator_id = None

        if call_data.operator_id is None:
            self.logger.debug(f"trying all operators")
            for opid in operatorIDs:
                ret = await self.location_by_evse_id(evse_id=evse_id, operator_id=opid)
                if len(ret) != 0:
                    call_data.operator_id = opid
                    self.logger.info(f"found operator {opid.name}")
                    break
        if ret is None:
            return None, call_data
        else:
            return ret[0], call_data

    async def location_by_evse_id(
        self, evse_id: str, operator_id: str | OperatorID, **kwargs
    ) -> list[Location]:
        """
        Perform API request.
        Usually yields just one Location object.

        for the operator id, see chargecloudapi.api.operatorIDs for examples
        """
        if isinstance(operator_id, OperatorID):
            operator_id = operator_id.op_id
        elif not operator_id:
            raise ValueError("no operator_id given")
        url_template = "https://app.chargecloud.de/emobility:ocpi/{}/app/2.0/locations"

        url_obj = URL(url_template.format(operator_id))
        response = await self.request("GET", url_obj % {"evse": evse_id})

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
