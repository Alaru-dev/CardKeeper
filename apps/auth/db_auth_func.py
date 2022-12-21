from sqlalchemy import update
from sqlalchemy.future import select


async def db_get_user_by_name(session, user_table, name):
    exist_user = await session.scalar(
        select(user_table).where(user_table.username == name)
    )
    return exist_user


async def db_get_user_by_id(session, user_table, id):
    exist_user = await session.scalar(
        select(user_table).where(user_table.id == id)
    )
    return exist_user


async def db_add_user(session, user_table, user):
    session.add(user_table(username=user.username, password=user.password))
    created_user = await session.scalar(
        select(user_table).where(user_table.username == user.username)
    )
    return created_user


async def db_update_user(session, user_table, user):
    await session.execute(
        update(user_table)
        .where(user_table.id == user.id)
        .values(username=user.username, password=user.password)
    )
    updated_user = await session.scalar(
        select(user_table).where(user_table.username == user.username)
    )
    return updated_user


async def db_delete_user(session, user_table, id):
    current_user = await session.scalar(
        select(user_table).where(user_table.id == id)
    )
    await session.delete(current_user)
    return current_user
