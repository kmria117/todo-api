from datetime import date

import pytest

from app.core.exceptions import (
    InvalidTaskError,
    TaskAlreadyDoneError,
    TaskNotFoundError,
)
from app.models.task import Priority, Status
from app.repositories.in_memory import InMemoryTaskRepository
from app.services.task_service import TaskService

TODAY = date(2026, 10, 24)


@pytest.fixture
def service():
    # Tanggal dibekukan supaya test deadline selalu konsisten.
    return TaskService(InMemoryTaskRepository(), today=lambda: TODAY)


# ---------- create ----------
def test_create_task_success(service):
    task = service.create_task("Belajar SOLID", priority=Priority.HIGH)
    assert task.id == 1
    assert task.title == "Belajar SOLID"
    assert task.status == Status.PENDING


def test_create_task_strips_title(service):
    assert service.create_task("  Tugas  ").title == "Tugas"


@pytest.mark.parametrize("title", ["", "   "])
def test_create_task_empty_title_rejected(service, title):
    with pytest.raises(InvalidTaskError):
        service.create_task(title)


def test_create_task_past_deadline_rejected(service):
    with pytest.raises(InvalidTaskError):
        service.create_task("Tugas", deadline=date(2026, 10, 23))


def test_create_task_deadline_today_allowed(service):
    assert service.create_task("Tugas", deadline=TODAY).deadline == TODAY


# ---------- read ----------
def test_get_task_not_found(service):
    with pytest.raises(TaskNotFoundError):
        service.get_task(99)


def test_list_tasks_filter_by_priority_and_status(service):
    service.create_task("A", priority=Priority.HIGH)
    b = service.create_task("B", priority=Priority.LOW)
    service.complete_task(b.id)

    assert len(service.list_tasks()) == 2
    assert [t.title for t in service.list_tasks(priority=Priority.HIGH)] == ["A"]
    assert [t.title for t in service.list_tasks(status=Status.DONE)] == ["B"]


# ---------- update ----------
def test_update_task_changes_only_given_fields(service):
    t = service.create_task("Lama", description="desc")
    updated = service.update_task(t.id, title="Baru")
    assert updated.title == "Baru"
    assert updated.description == "desc"


def test_update_task_invalid_title_rejected(service):
    t = service.create_task("Lama")
    with pytest.raises(InvalidTaskError):
        service.update_task(t.id, title=" ")


def test_update_done_task_rejected(service):
    t = service.create_task("Tugas")
    service.complete_task(t.id)
    with pytest.raises(TaskAlreadyDoneError):
        service.update_task(t.id, title="Ubah")


# ---------- complete ----------
def test_complete_task_sets_done(service):
    t = service.create_task("Tugas")
    assert service.complete_task(t.id).status == Status.DONE


def test_complete_task_twice_rejected(service):
    t = service.create_task("Tugas")
    service.complete_task(t.id)
    with pytest.raises(TaskAlreadyDoneError):
        service.complete_task(t.id)


# ---------- delete ----------
def test_delete_task(service):
    t = service.create_task("Tugas")
    service.delete_task(t.id)
    with pytest.raises(TaskNotFoundError):
        service.get_task(t.id)


def test_delete_missing_task(service):
    with pytest.raises(TaskNotFoundError):
        service.delete_task(1)
def test_list_tasks_overdue_filter():
    current = {"today": TODAY}
    service = TaskService(InMemoryTaskRepository(), today=lambda: current["today"])
    service.create_task("Telat", deadline=TODAY)
    service.create_task("Aman", deadline=date(2026, 11, 30))
    service.create_task("Tanpa deadline")

    current["today"] = date(2026, 10, 25)  # satu hari berlalu

    assert [t.title for t in service.list_tasks(overdue=True)] == ["Telat"]