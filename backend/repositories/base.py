from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any

from sqlalchemy.orm import Session

T = TypeVar('T')


class AsyncIteratorWrapper:
    """The following is a utility class that transforms a
        regular iterable to an asynchronous one.

        link: https://www.python.org/dev/peps/pep-0492/#example-2
    """

    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value

class BaseRepository(Generic[T], ABC):
    def __init__(self, db_session: Session, model_class: type):
        self.db_session = db_session
        self.model_class = model_class

    @abstractmethod
    def create(self, obj_in: Any) -> T:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass

    @abstractmethod
    def update(self, id: int, obj_in: Any) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
