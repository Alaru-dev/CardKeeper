from sqlalchemy import update
from sqlalchemy.future import select


async def db_get_card(session, card_table, user_id, card_name):
    exist_card = await session.scalar(
        select(card_table).where(
            card_table.user_id == user_id, card_table.card_name == card_name
        )
    )
    return exist_card


async def db_get_all_card(session, card_table, user_id):
    card_massive = await session.scalars(
        select(card_table).where(card_table.user_id == user_id)
    )
    return card_massive


async def db_add_card(session, card_table, card, card_path):
    created_card = session.add(
        card_table(
            user_id=card.user_id,
            card_name=f"{card.card_name}",
            card_path=card_path,
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
