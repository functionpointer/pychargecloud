import sys

import chargecloudapi
from chargecloudapi.api import operatorIDs
import aiohttp
import asyncio
import logging


async def main():
    evse_ids = [
        "DE*REK*E100241*002",
        "DE*REK*E100196*001",
        "DE*REK*E10032*002",
        "DE*GVG*E00003*001",
        "DE*ERE*E0008*OMN15L",
        "DE*UFC*E210004",
        "DE*ION*E207101",
        "DE*EDR*E11000150*2",
        "DESWME052601",
        "DE*SWM*E052601",
        "DE*TNK*E00136*02",
    ]
    results: dict[str, dict[str, list[chargecloudapi.Location]]] = {
        evse_id: {} for evse_id in evse_ids
    }
    for operator_id in operatorIDs:
        async with aiohttp.ClientSession() as session:
            api = chargecloudapi.Api(session)

            for evse_id in evse_ids:
                locations = await api.location_by_evse_id(evse_id, operator_id)
                results[evse_id][operator_id.name] = locations

    for evse_id, res in results.items():
        print(f"evse_id {evse_id}:")
        for operator_name, locations in res.items():
            print(f"{operator_name:12s}-> {locations}")


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
