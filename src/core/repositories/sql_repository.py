from typing import Any, Type, TypeVar, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.sql import Select, and_, select

from pydantic import BaseModel

from src.core.models import Base
from src.core.repositories.base_repository import IRepository
from src.core.exceptions import RecordNotFoundException

TModel = TypeVar("TModel", bound=Base)
TModelSchema = TypeVar("TModelSchema", bound=BaseModel)


class SQLRepository(IRepository[TModel, TModelSchema]):
    def __init__(self, session: AsyncSession, model: Type[TModel]):
        self._session = session
        self._model = model

    async def create(self, data: TModelSchema) -> TModel:
        record_data = data.model_dump()
        record = self._model(**record_data)
        await self.add(record)
        return record

    def _build_statement(self, *attrs: str, **filters: Any) -> Select:
        select_entities = self._get_select_entities(*attrs)
        statement = select(*select_entities)
        statement = self._filter_statement(statement, **filters)
        return statement

    def _get_select_entities(self, *attributes: str) -> list[Any]:
        select_entities = []
        for attr in attributes:
            if not hasattr(self._model, attr):
                raise ValueError(f"Invalid column name {attr}")
            select_entities.append(getattr(self._model, attr))

        if not select_entities:
            select_entities = [self._model]

        return select_entities

    def _filter_statement(self, statement: Select, **filters: Any) -> Select:
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

    async def get_by_id(self, record_id: int) -> TModel:
        statement = self._build_statement(id=record_id)
        record: TModel | None = await self.get_scalar(statement)
        if not record:
            raise RecordNotFoundException(
                f"{self._model.__name__} with ID {record_id} not found."
            )
        else:
            return record

    async def get_col_by_id(self, col_name: str, record_id: int) -> Any:
        statement = self._build_statement(col_name, id=record_id)
        col_value = await self.get_scalar(statement)
        if not col_value:
            raise RecordNotFoundException(
                f"{self._model.__name__} with ID {record_id} not found."
            )
        else:
            return col_value

    async def list_all(self) -> list[TModel]:
        statement = self._build_statement()
        result = await self._session.execute(statement)
        return list(result.scalars().all())

    async def get_all(self, statement: Select) -> list[Any]:
        result = await self._session.execute(statement)
        return list(result.all())

    async def get_scalar(self, statement: Select) -> Any:
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

    async def delete(self, record_id: int) -> None:
        record = await self.get_by_id(record_id)
        if record is not None:
            await self._session.delete(record)
            await self._session.flush()
