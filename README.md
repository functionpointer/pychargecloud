pychargecloud
=============

Fetches data about public ev charge points from chargecloud.de

Used by [Home Assistant Chargecloud Integration](https://github.com/functionpointer/home-assistant-chargecloud-integration)

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


Dev notes
=========

To make a new release, use GitHub website and draft a release manually.
Make sure the version number in pyproject.toml matches the new tag.
GitHub Actions will publish it to pypi.
