"""Abstraksi repository (Dependency Inversion + Interface Segregation)."""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.task import Task


class TaskReader(ABC):
    @abstractmethod
    def get(self, task_id: int) -> Optional[Task]: ...

    @abstractmethod
    def list_all(self) -> List[Task]: ...


class TaskWriter(ABC):
    @abstractmethod
    def add(self, task: Task) -> Task: ...

    @abstractmethod
    def update(self, task: Task) -> Task: ...

    @abstractmethod
    def delete(self, task_id: int) -> bool: ...

    @abstractmethod
    def next_id(self) -> int: ...


class TaskRepository(TaskReader, TaskWriter):
    """Gabungan reader + writer untuk service yang butuh keduanya."""
