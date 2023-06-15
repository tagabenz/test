import json
import asyncio, aiohttp

from models import *

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def get_index_price(async_session):
    index_names=[
        "btc_usd",
        "eth_usd",
    ]
    async with aiohttp.ClientSession() as session:
        for i in index_names:
            async with session.get(f"https://test.deribit.com/api/v2/public/get_index_price?index_name={i}") as response:
                r = await response.json()
                price=str(r['result']['index_price'])
                if i == "btc_usd":object = Index(price=price,ticker='BTC')
                else:object = Index(price=price,ticker='ETH')
                await insert_object(async_session,object)

async def init_models(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def main():
    engine = create_async_engine("postgresql+asyncpg://postgres:test@localhost/postgres",echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(init_models,args=[engine])
    scheduler.add_job(get_index_price,'interval',args=[async_session],seconds=10)
    scheduler.start()

    try:asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):pass


if __name__ == "__main__":
    main()
