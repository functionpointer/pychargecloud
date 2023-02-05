import sys

import chargecloudapi
import aiohttp
import asyncio
import logging


async def main():
    operator_IDs = {
        "maingau": "606a0da0dfdd338ee4134605653d4fd8",
        "SW Kiel": "6336fe713f2eb7fa04b97ff6651b76f8",
        "Rheinenergie": "c4ce9bb82a86766833df8a4818fa1b5c",
    }
    evse_ids = [
        "DE*REK*E100241*002",
        "DE*REK*E100196*001",
        "DE*REK*E10032*002",
        "DE*GVG*E00003*001",
        "DE*ERE*E0008*OMN15L",
        "DE*UFC*E210004",
        "DE*ION*E207101",
        "DE*EDR*E11000150*2",
    ]
    results: dict[str, dict[str, list[chargecloudapi.Location]]] = {
        evse_id: {} for evse_id in evse_ids
    }
    for operator_name, operator_id in operator_IDs.items():
        async with aiohttp.ClientSession() as session:
            base_url = f"https://app.chargecloud.de/emobility:ocpi/{operator_id}/app/2.0/locations"
            api = chargecloudapi.Api(session, base_url=base_url)

            for evse_id in evse_ids:
                locations = await api.location_by_evse_id(evse_id)
                results[evse_id][operator_name] = locations

    for evse_id, res in results.items():
        print(f"evse_id {evse_id}:")
        for operator_name, locations in res.items():
            print(f"{operator_name:12s}-> {locations}")


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
