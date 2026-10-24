"""Layer HTTP: hanya menerima request, memanggil service, mengembalikan response."""
from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import get_task_service
from app.api.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.models.task import Priority, Status
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.create_task(**body.model_dump())


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    overdue: Optional[bool] = None,
    service: TaskService = Depends(get_task_service),
):
    return service.list_tasks(status=status, priority=priority, overdue=overdue)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return service.get_task(task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, body: TaskUpdate, service: TaskService = Depends(get_task_service)
):
    return service.update_task(task_id, **body.model_dump(exclude_unset=True))


@router.post("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return service.complete_task(task_id)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    service.delete_task(task_id)
    return Response(status_code=204)
