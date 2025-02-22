"""
Модуль описывает репозиторий, работающий в оперативной памяти
"""

from itertools import count
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class MemoryRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в оперативной памяти. Хранит данные в словаре.
    """

    def __init__(self) -> None:
        self._container: dict[int, T] = {}
        self._counter = count(1)

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'Trying to add object {obj} with filled `pk` attribute')
        pk = next(self._counter)
        self._container[pk] = obj
        obj.pk = pk
        return pk

    def get(self, pk: int) -> T | None:
        return self._container.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        if where is None:
            return list(self._container.values())
        return [obj for obj in self._container.values()
                if all(getattr(obj, attr) == value for attr, value in where.items())]

    def get_all_by_pattern(self, patterns: dict[str, str]) -> list[T]:
        return [obj for obj in self._container.values()
                if all(value in getattr(obj, attr) for attr, value in patterns.items())]

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('Attempt to update object with unknown primary key')
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        self._container.pop(pk)
