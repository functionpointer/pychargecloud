import sys

import chargecloudapi
import aiohttp
import asyncio
import logging


async def main():
    async with aiohttp.ClientSession() as session:
        api = chargecloudapi.Api(session)
        locations = await api.location_by_evse_id("DECCH*ECCH1800155EBG*2")
        print(locations)

        evse_ids = ["DE*REK*E100241*002",
                    "DE*REK*E100196*001",
                    "DE*REK*E10032*002",
                    "DE*GVG*E00003*001",
                    "DE*ERE*E0008*OMN15L",
                    "DE*UFC*E210004",
                    "DE*ION*E207101",
                    ]

        for evse_id in evse_ids:
            locations = await api.location_by_evse_id(evse_id)
            print(f"{evse_id}: {locations}")


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
