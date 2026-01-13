"""Data models and enums for the to-do list application."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict


class Priority(Enum):
    """Represents the urgency of a to-do item."""

    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(Enum):
    """Represents the completion status of a to-do item."""

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class TodoItem:
    """A single to-do item owned by a user."""

    id: str
    title: str
    details: str
    priority: Priority
    status: Status
    owner: str
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the item into a JSON-friendly dictionary."""

        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "priority": self.priority.value,
            "status": self.status.value,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TodoItem":
        """Create a ``TodoItem`` from a dictionary representation."""

        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            details=str(data.get("details", "")),
            priority=Priority(str(data["priority"])),
            status=Status(str(data["status"])),
            owner=str(data["owner"]),
            created_at=datetime.fromisoformat(str(data["created_at"])),
            updated_at=datetime.fromisoformat(str(data["updated_at"])),
        )
