from .interface_respository import IRepository
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, and_


class SQLRepository(IRepository):

    def __init__(self, session: Session, model):
        self._session = session
        self._model = model

    def create(self, **data):
        record = self._model(**data)
        self.add(record)

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

    def get_by_id(self, id: int):
        return self._session.query(self._model).filter_by(id=id).first()

    def get_all(self):
        return self._session.query(self._model).all()

    def add(self, record):
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def update(self, record):
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def delete(self, id):
        record = self.get_by_id(id)
        if record is not None:
            self._session.delete(record)
            self._session.flush()