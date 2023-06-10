import asyncio, aiohttp
import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# call api for get currency index
async def get_index():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get("https://www.derebit.com/api/v2/public/get_index?currency=BTC") as response:

            print(await response.text())


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_index, 'interval', seconds=3)
    scheduler.start()

    try:asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):pass
