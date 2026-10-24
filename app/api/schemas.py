"""Schema request/response (kontrak HTTP), terpisah dari entity domain."""
from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.models.task import Priority, Status


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    deadline: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    deadline: Optional[date] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: Priority
    deadline: Optional[date]
    status: Status
