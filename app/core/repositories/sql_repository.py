from .base_repository import IRepository
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
#from sqlalchemy.future import select

#from sqlalchemy.sql import select, and_
from typing import Union


class SQLRepository(IRepository):

    def __init__(self, session: AsyncSession, model):
        self._session = session
        self._model = model

    async def create(self, **data):
        record = self._model(**data)
        await self.add(record)

    def _build_statement(self, *attrs, **filters):
        select_entities = self._get_select_entities(*attrs)
        statement = select().add_columns(*select_entities)
        statement = self._filter_statement(statement, **filters)
        return statement

    def _get_select_entities(self, *attributes):

        select_entities = []

        for attr in attributes:
            if not hasattr(self._model, attr):
                raise ValueError(f"Invalid column name {attr}")

            select_entities.append(getattr(self._model, attr))

        if not select_entities:
            select_entities = [self._model]

        # Create the select statement
        return select_entities

    def _filter_statement(self, statement, **filters):
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self._model, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model, c) == v)

        if len(where_clauses) == 1:
            statement = statement.where(where_clauses[0])
        elif len(where_clauses) > 1:
            statement = statement.where(and_(*where_clauses))
        return statement

    async def get_by_id(self, id: int):
        return await self._session.get(self._model, id)

    async def list_all(self):
        result = await self._session.execute(statement=select(self._model))
        return result.all()

    async def get_all(self, statement):
        result = await self._session.execute(statement)
        return result.all()

    async def get_scalar(self, statement):
        result = await self._session.execute(statement)
        return result.scalar()

    async def add(self, record):
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def update(self, record):
        self._session.add(record)
        await self._session.flush()
        #await self._session.refresh(record)
        return record

    async def delete(self, id):
        record = await self.get_by_id(id)
        if record is not None:
            await self._session.delete(record)
            await self._session.flush()
