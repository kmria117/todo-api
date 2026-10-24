"""Tempat wiring dependency: satu-satunya tempat yang tahu implementasi konkret."""
from functools import lru_cache

from app.repositories.base import TaskRepository
from app.repositories.in_memory import InMemoryTaskRepository
from app.services.task_service import TaskService


@lru_cache
def get_repository() -> TaskRepository:
    return InMemoryTaskRepository()  # ganti ke SQLite di sini saja


def get_task_service() -> TaskService:
    return TaskService(get_repository())
