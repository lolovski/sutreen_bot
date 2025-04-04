from typing import List

from db import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.future import select

class EntryComponent(Base):
    __tablename__ = 'entry_component'
    entry_id = Column(Integer, ForeignKey('entry.id', ondelete='CASCADE'), primary_key=True)
    component_id = Column(Integer, ForeignKey('component.id'), primary_key=True)

    def __init__(self, entry_id, component_id):
        self.entry_id = entry_id
        self.component_id = component_id

    async def create(self):
        db_session = await session()
        db_session.add(self)
        await db_session.commit()
        await db_session.close()
        return self