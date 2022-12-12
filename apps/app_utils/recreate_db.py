import asyncio
from apps import Base
from apps.db.db_specify import engine


async def recreate_db_force():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(recreate_db_force())
