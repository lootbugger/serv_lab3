import abc
from typing import List, Optional, TypeVar, Generic, Any
from django.db import models

ModelType = TypeVar("ModelType", bound=models.Model)


class AbstractRepository(abc.ABC, Generic[ModelType]):
    @abc.abstractmethod
    def get_all(self) -> List[ModelType]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, pk: Any) -> Optional[ModelType]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, data: dict) -> ModelType:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, pk: Any, data: dict) -> Optional[ModelType]:
        """Оновити існуючий об'єкт за його ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, pk: Any) -> None:
        """Видалити об'єкт за його ID."""
        raise NotImplementedError
