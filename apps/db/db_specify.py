from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .db_credentials import DB_URL

engine = create_async_engine(DB_URL, echo=False)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
