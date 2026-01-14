"""Unit tests for data models and enums."""

from datetime import datetime

import pytest

from models import Priority, Status, TodoItem


class TestPriority:
    """Tests for the Priority enum."""

    def test_priority_high_value(self) -> None:
        """Test HIGH priority has correct value."""
        assert Priority.HIGH.value == "HIGH"

    def test_priority_mid_value(self) -> None:
        """Test MID priority has correct value."""
        assert Priority.MID.value == "MID"

    def test_priority_low_value(self) -> None:
        """Test LOW priority has correct value."""
        assert Priority.LOW.value == "LOW"

    def test_priority_all_members(self) -> None:
        """Test all priority members exist."""
        priorities = [p.value for p in Priority]
        assert "HIGH" in priorities
        assert "MID" in priorities
        assert "LOW" in priorities


class TestStatus:
    """Tests for the Status enum."""

    def test_status_pending_value(self) -> None:
        """Test PENDING status has correct value."""
        assert Status.PENDING.value == "PENDING"

    def test_status_completed_value(self) -> None:
        """Test COMPLETED status has correct value."""
        assert Status.COMPLETED.value == "COMPLETED"

    def test_status_all_members(self) -> None:
        """Test all status members exist."""
        statuses = [s.value for s in Status]
        assert "PENDING" in statuses
        assert "COMPLETED" in statuses


class TestTodoItem:
    """Tests for the TodoItem dataclass."""

    @pytest.fixture
    def sample_todo(self) -> TodoItem:
        """Create a sample TodoItem for testing."""
        return TodoItem(
            id="uuid-1",
            title="Test Task",
            details="This is a test task",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at=datetime(2026, 1, 13, 10, 0, 0),
            updated_at=datetime(2026, 1, 13, 10, 0, 0),
        )

    def test_todoitem_creation(self, sample_todo: TodoItem) -> None:
        """Test creating a TodoItem with all fields."""
        assert sample_todo.id == "uuid-1"
        assert sample_todo.title == "Test Task"
        assert sample_todo.details == "This is a test task"
        assert sample_todo.priority == Priority.HIGH
        assert sample_todo.status == Status.PENDING
        assert sample_todo.owner == "testuser"

    def test_todoitem_to_dict(self, sample_todo: TodoItem) -> None:
        """Test serialization to dictionary."""
        todo_dict = sample_todo.to_dict()
        assert todo_dict["id"] == "uuid-1"
        assert todo_dict["title"] == "Test Task"
        assert todo_dict["details"] == "This is a test task"
        assert todo_dict["priority"] == "HIGH"
        assert todo_dict["status"] == "PENDING"
        assert todo_dict["owner"] == "testuser"
        assert todo_dict["created_at"] == "2026-01-13T10:00:00"
        assert todo_dict["updated_at"] == "2026-01-13T10:00:00"

    def test_todoitem_from_dict(self, sample_todo: TodoItem) -> None:
        """Test deserialization from dictionary."""
        todo_dict = sample_todo.to_dict()
        restored = TodoItem.from_dict(todo_dict)

        assert restored.id == sample_todo.id
        assert restored.title == sample_todo.title
        assert restored.details == sample_todo.details
        assert restored.priority == sample_todo.priority
        assert restored.status == sample_todo.status
        assert restored.owner == sample_todo.owner
        assert restored.created_at == sample_todo.created_at
        assert restored.updated_at == sample_todo.updated_at

    def test_todoitem_from_dict_with_missing_details(self) -> None:
        """Test creating TodoItem from dict with missing optional details field."""
        data = {
            "id": "uuid-2",
            "title": "Task without details",
            "priority": "MID",
            "status": "COMPLETED",
            "owner": "anotheruser",
            "created_at": "2026-01-13T12:00:00",
            "updated_at": "2026-01-13T12:00:00",
        }
        todo = TodoItem.from_dict(data)
        assert todo.details == ""
        assert todo.title == "Task without details"

    def test_todoitem_round_trip(self, sample_todo: TodoItem) -> None:
        """Test that to_dict and from_dict preserve all data."""
        original_dict = sample_todo.to_dict()
        restored = TodoItem.from_dict(original_dict)
        restored_dict = restored.to_dict()

        assert original_dict == restored_dict
