import datetime
from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.future import select
from db import Base, session
from hashlib import sha256

from db.models.component import Component
from db.models.entry_component import EntryComponent
from utils import moscow_tz

class Entry(Base):
    __tablename__ = "entry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = mapped_column(ForeignKey('account.telegram_id', ondelete='CASCADE', onupdate="CASCADE"))
    create_at = Column(DateTime, default=datetime.datetime.now(moscow_tz))
    completed_at = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    description = Column(String)
    contact = Column(String)
    price = Column(Integer, nullable=True)

    client = relationship('Account', back_populates='entries', lazy="selectin", foreign_keys=[client_id])
    components: Mapped[List['Component']] = relationship(back_populates='entries', lazy="selectin", secondary='entry_component')

    def __init__(self, id=None, client_id=None, description=None, contact=None, **kwargs):
        self.id = int(id) if id else id
        self.client_id = int(client_id) if client_id else client_id
        self.description = description
        self.contact = contact

    async def create(self):
        db_session = await session()
        db_session.add(self)
        await db_session.commit()
        await db_session.close()
        return self

    async def get_client(self, completed=False):
        db_session = await session()
        result = (await db_session.scalars(select(Entry).where(Entry.client_id == self.client_id, Entry.completed == completed))).all()
        await db_session.close()
        return result

    async def get(self):
        db_session = await session()
        result = (await db_session.scalars(select(Entry).where(Entry.id == self.id))).one_or_none()
        await db_session.close()
        return result

    async def get_multi(self, completed=False):
        db_session = await session()
        result = (await db_session.scalars(select(Entry).where(Entry.completed == completed).order_by(Entry.create_at.desc()))).all()
        await db_session.close()
        return result

    async def complete(self):
        db_session = await session()
        try:
            entry = await db_session.get(Entry, self.id)
            if entry:
                entry.completed = True
                entry.completed_at = datetime.datetime.now(tz=moscow_tz)
                await db_session.commit()
        finally:
            await db_session.close()

    async def delete(self):
        db_session = await session()
        result = (await db_session.scalars(select(EntryComponent).where(EntryComponent.entry_id == self.id))).all()
        for component in result:
            await db_session.delete(component)
        await db_session.delete(self)

        await db_session.commit()
        await db_session.close()

    async def get_place(self):
        db_session = await session()
        result = (await db_session.scalars(select(Entry).where(Entry.create_at < self.create_at, Entry.completed == False))).all()
        await db_session.close()
        return len(result) + 1

    async def get_components_dict(self) -> dict:
        db_session = await session()
        result = (await db_session.scalars(select(EntryComponent).where(EntryComponent.entry_id == self.id))).all()
        components = (await db_session.scalars(select(Component).where(Component.id.in_([component.component_id for component in result])))).all()
        await db_session.close()
        return {component.group: component.name for component in components}
