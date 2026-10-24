"""Implementasi repository di memori. Bisa diganti SQLite tanpa mengubah service."""
from copy import deepcopy
from typing import Dict, List, Optional

from app.models.task import Task
from app.repositories.base import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._data: Dict[int, Task] = {}
        self._counter = 0

    def next_id(self) -> int:
        self._counter += 1
        return self._counter

    def add(self, task: Task) -> Task:
        self._data[task.id] = deepcopy(task)
        return deepcopy(task)

    def get(self, task_id: int) -> Optional[Task]:
        task = self._data.get(task_id)
        return deepcopy(task) if task else None

    def list_all(self) -> List[Task]:
        return [deepcopy(t) for t in self._data.values()]

    def update(self, task: Task) -> Task:
        self._data[task.id] = deepcopy(task)
        return deepcopy(task)

    def delete(self, task_id: int) -> bool:
        return self._data.pop(task_id, None) is not None
