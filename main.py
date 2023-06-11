import json
import asyncio, aiohttp

from models import Base

from sqlalchemy.ext.asyncio import create_async_engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler


DATABASE_URL="postgresql+asyncpg://postgres:test@localhost/postgres"


async def get_index_price():
    index_names=[
        "btc_usd",
        "eth_usd",
    ]
    async with aiohttp.ClientSession() as session:
        for i in index_names:
            async with session.get(f"https://test.deribit.com/api/v2/public/get_index_price?index_name={i}") as response:
                print(await response.json())


async def init_models():
    engine = create_async_engine(DATABASE_URL,echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_index_price, 'interval', seconds=3)
    scheduler.start()

    try:asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):pass
    
    
    

    

