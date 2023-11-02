from .base_repository import IRepository
from sqlalchemy import select, and_, Select, Row
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, TypeVar

TModel = TypeVar('TModel')


class SQLRepository(IRepository):

    def __init__(self, session: AsyncSession, model: Type[TModel]):
        self._session = session
        self._model = model

    async def create(self, **data) -> TModel:
        record = self._model(**data)
        await self.add(record)
        return record

    def _build_statement(self, *attrs, **filters) -> Select:
        select_entities = self._get_select_entities(*attrs)
        statement = select().add_columns(*select_entities)
        statement = self._filter_statement(statement, **filters)
        return statement

    def _get_select_entities(self, *attributes) -> list[any]:

        select_entities = []

        for attr in attributes:
            if not hasattr(self._model, attr):
                raise ValueError(f"Invalid column name {attr}")

            select_entities.append(getattr(self._model, attr))

        if not select_entities:
            select_entities = [self._model]

        return select_entities

    def _filter_statement(self, statement, **filters) -> Select:
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

    async def get_by_id(self, id: int) -> TModel:
        return await self._session.get(self._model, id)

    async def list_all(self) -> list[TModel]:
        result = await self._session.execute(statement=select(self._model))
        return result.scalars().all()

    async def get_all(self, statement: Select) -> list[Row] | Row:
        result = await self._session.execute(statement)
        return result.all()

    async def get_scalar(self, statement: Select) -> TModel:
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def add(self, record: TModel) -> TModel:
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def update(self, record: TModel) -> TModel:
        self._session.add(record)
        await self._session.flush()
        return record

    async def delete(self, id: int):
        record = await self.get_by_id(id)
        if record is not None:
            await self._session.delete(record)
            await self._session.flush()
