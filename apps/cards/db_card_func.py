from sqlalchemy import update
from sqlalchemy.future import select


async def db_get_card_by_name(session, card_table, user_id, card_name):
    exist_card = await session.scalar(
        select(card_table).where(
            card_table.user_id == user_id, card_table.card_name == card_name
        )
    )
    return exist_card


async def db_get_card_by_id(session, card_table, user_id, card_id):
    exist_card = await session.scalar(
        select(card_table).where(
            card_table.user_id == user_id, card_table.id == card_id
        )
    )
    return exist_card


async def db_get_all_card(session, card_table, user_id):
    card_massive = await session.scalars(
        select(card_table).where(card_table.user_id == user_id)
    )
    return card_massive


async def db_add_card(session, card_table, user_id, card, card_path):
    session.add(
        card_table(
            user_id=user_id,
            card_name=card.card_name,
            card_path=card_path,
            group=card.group,
            favorites=card.favorites,
        )
    )
    created_card = await db_get_card_by_name(
        session, card_table, user_id, card.card_name
    )
    return created_card


async def db_update_card(session, card_table, user_id, card):
    await session.execute(
        update(card_table)
        .where(card_table.id == card.id)
        .values(
            card_name=card.card_name,
            card_path=card.card_path,
            group=card.group,
            favorites=card.favorites,
        )
    )
    updated_user = await db_get_card_by_id(
        session, card_table, user_id, card.id
    )
    return updated_user


async def db_delete_card(session, card_table, user_id, card_id):
    current_card = await db_get_card_by_id(
        session, card_table, user_id, card_id
    )
    await session.delete(current_card)
    return current_card
