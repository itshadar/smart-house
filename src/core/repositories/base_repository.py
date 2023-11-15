from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Union, Coroutine, Any

T = TypeVar("T")
S = TypeVar("S")


class IRepository(Generic[T, S], ABC):
    @abstractmethod
    def create(self, data: S) -> Union[T, Coroutine[Any, Any, T]]:
        ...

    @abstractmethod
    def list_all(self) -> Union[list[T], Coroutine[Any, Any, list[T]]]:
        ...

    @abstractmethod
    def get_by_id(self, record_id: int) -> Union[T, Coroutine[Any, Any, T]]:
        ...

    @abstractmethod
    def update(self, record: T) -> Union[T, Coroutine[Any, Any, T]]:
        ...

    @abstractmethod
    def delete(self, record_id: int) -> Union[None, Coroutine[Any, Any, None]]:
        ...
