import os

from sqlalchemy import update
from sqlalchemy.future import select

from apps.db.card_storage_settings import StoragePath


async def db_get_card(session, card_table, card_name):
    exist_card = await session.scalar(
        select(card_table).where(card_table.card_name == card_name)
    )
    return exist_card


async def db_get_all_card(session, card_table, user_id):
    card_massive = await session.scalars(
        select(card_table).where(card_table.user_id == user_id)
    )
    return card_massive


async def db_add_card(session, card_table, card):
    created_card = session.add(
        card_table(
            user_id=card.user_id,
            card_name=f"{card.user_id}{card.card_name}",
            card_path=os.path.join(StoragePath, str(card.user_id)),
            group=card.group,
            favorites=card.favorites,
        )
    )
    exist_card = await session.scalar(
        select(card_table).where(card_table.card_name == card.card_name)
    )
    return exist_card


# async def db_update_card(session, card_table, user):
#     updated_user = await session.execute(update(card_table).where(card_table.id == user.id).values(username=user.username, password=user.password))
#     return updated_user
#
#
# async def db_delete_card(session, card_table, user):
#     current_user = await session.scalar(select(card_table).where(card_table.username == user.username))
#     created_user = await session.delete(current_user)
#     return created_user
#
# print(os.path.join(StoragePath, 1))
