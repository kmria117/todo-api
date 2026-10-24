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
    def __init__(
        self,
        repository: TaskRepository,
        today: Callable[[], date] = date.today,
    ) -> None:
        # Repository dan "jam" di-inject lewat konstruktor, jadi mudah di-fake saat test.
        self._repo = repository
        self._today = today

    # ---------- validasi ----------
    def _validate_title(self, title: str) -> str:
        if title is None or not title.strip():
            raise InvalidTaskError("Judul tidak boleh kosong")
        return title.strip()

    def _validate_deadline(self, deadline: Optional[date]) -> None:
        if deadline is not None and deadline < self._today():
            raise InvalidTaskError("Deadline tidak boleh di masa lalu")

    def _get_or_raise(self, task_id: int) -> Task:
        task = self._repo.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Tugas {task_id} tidak ditemukan")
        return task

    def _ensure_editable(self, task: Task) -> None:
        if task.status == Status.DONE:
            raise TaskAlreadyDoneError("Tugas yang sudah selesai tidak bisa diubah")

    # ---------- use case ----------
    def create_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        deadline: Optional[date] = None,
    ) -> Task:
        title = self._validate_title(title)
        self._validate_deadline(deadline)
        task = Task(
            id=self._repo.next_id(),
            title=title,
            description=description,
            priority=priority,
            deadline=deadline,
        )
        return self._repo.add(task)

    def get_task(self, task_id: int) -> Task:
        return self._get_or_raise(task_id)

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

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        deadline: Optional[date] = None,
    ) -> Task:
        task = self._get_or_raise(task_id)
        self._ensure_editable(task)
        if title is not None:
            task.title = self._validate_title(title)
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if deadline is not None:
            self._validate_deadline(deadline)
            task.deadline = deadline
        return self._repo.update(task)

    def complete_task(self, task_id: int) -> Task:
        task = self._get_or_raise(task_id)
        self._ensure_editable(task)
        task.status = Status.DONE
        return self._repo.update(task)

    def delete_task(self, task_id: int) -> None:
        self._get_or_raise(task_id)
        self._repo.delete(task_id)