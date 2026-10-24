"""Logika bisnis. Hanya bergantung pada abstraksi repository, bukan implementasi."""
from datetime import date
from typing import Callable, List, Optional

from app.core.exceptions import (
    InvalidTaskError,
    TaskAlreadyDoneError,
    TaskNotFoundError,
)
from app.models.task import Priority, Status, Task
from app.repositories.base import TaskRepository


class TaskService:
    def list_tasks(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        overdue: Optional[bool] = None,
    ) -> List[Task]:
        tasks = self._repo.list_all()
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if priority is not None:
            tasks = [t for t in tasks if t.priority == priority]
        if overdue:
            today = self._today()
            tasks = [
                t for t in tasks
                if t.deadline is not None
                and t.deadline < today
                and t.status == Status.PENDING
            ]
        return tasks