from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from apps.db_models.user import Base


class Card(Base):
    __tablename__ = "Card"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    card_name = Column(String)
    card_path = Column(String)
    group = Column(String)
    favorites = Column(Boolean)
