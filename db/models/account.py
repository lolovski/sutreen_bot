from typing import List

from db import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.future import select


class Account(Base):
    __tablename__ = 'account'

    telegram_id = Column(String, primary_key=True, autoincrement=False)
    first_name = Column(String, nullable=True)
    telephone = Column(String)
    entries: Mapped[List["Entry"]] = relationship(back_populates="client", lazy="selectin", uselist=True)

    def __init__(self, telegram_id=None, telephone=None, first_name=None):
        self.first_name = first_name
        self.telegram_id = telegram_id
        self.telephone = telephone

    async def create(self):
        db_session = await session()
        db_session.add(self)
        await db_session.commit()
        await db_session.close()
        return self


    async def get_account(self):
        db_session = await session()
        result = (await db_session.scalars(select(Account).filter(Account.telegram_id == self.telegram_id))).one_or_none()
        await db_session.close()
        return result

    async def get_person_id(self):
        db_session = await session()
        result = (await db_session.scalars(select(Account).filter(Account.id == self.id))).one_or_none()
        await db_session.close()
        return result.person.id

    async def get_person_name(self):
        db_session = await session()
        result = (await db_session.scalars(select(Account).filter(Account.id == self.id))).one_or_none()
        await db_session.close()
        return result.first_name

    @staticmethod
    async def get_all():
        db_session = await session()
        result = (await db_session.scalars(select(Account))).all()
        await db_session.close()
        return result
