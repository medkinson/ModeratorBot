from sqlalchemy import Column, Integer, BigInteger
from bot.database.base import Base

class ModeratorStats(Base):
    __tablename__ = 'ModeratorStats'

    chat_id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, primary_key=True)
    warns = Column(Integer, default=0)
