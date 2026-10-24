"""Entity domain: hanya data dan enum, tanpa logika HTTP atau penyimpanan."""
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(str, Enum):
    PENDING = "pending"
    DONE = "done"


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    deadline: Optional[date] = None
    status: Status = Status.PENDING
