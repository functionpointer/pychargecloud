pychargecloud
=============

Fetches data about public ev charge points from chargecloud.de

Example:
```python
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


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

```

See also src/main.py
