from typing import List

from db import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.future import select


class Component(Base):
    __tablename__ = 'component'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    group = Column(String)
    price = Column(Integer)
    hide = Column(Boolean, default=False)
    entries: Mapped[List["Entry"]] = relationship(back_populates="components", lazy="selectin", secondary='entry_component')

    def __init__(self, id=None, name=None, group=None, price=None):
        self.id = id
        self.price = price
        self.name = name
        self.group = group

    async def create(self):
        db_session = await session()
        db_session.add(self)
        await db_session.commit()
        await db_session.close()
        return self

    async def get(self):
        db_session = await session()
        result = (await db_session.scalars(select(Component).filter(Component.id == self.id))).one_or_none()
        await db_session.close()
        return result

    async def update(self, price=None, name=None, hide=None):
        db_session = await session()
        component = await db_session.get(Component, self.id)
        if price:
            component.price = price
        if name:
            component.name = name
        if isinstance(hide, bool):
            component.hide = hide

        await db_session.commit()
        await db_session.refresh(component)
        await db_session.close()

        return component

    async def delete(self):
        db_session = await session()
        component = await db_session.get(Component, self.id)
        await db_session.delete(component)
        await db_session.commit()
        await db_session.close()
        return self

    @staticmethod
    async def get_all():
        db_session = await session()
        result = (await db_session.scalars(select(Component))).all()
        await db_session.close()
        return result

    @staticmethod
    async def get_groups():
        db_session = await session()
        result = (await db_session.scalars(select(Component.group).distinct())).all()
        await db_session.close()
        return result

    @staticmethod
    async def get_group(group):
        db_session = await session()
        result = (await db_session.scalars(select(Component).filter(Component.group == group))).all()
        await db_session.close()
        return result

