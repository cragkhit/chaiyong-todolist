"""Unit tests for authentication functionality."""

import json
import tempfile
from pathlib import Path

import pytest

from auth import AuthManager


class TestAuthManager:
    """Tests for the AuthManager class."""

    @pytest.fixture
    def temp_users_file(self) -> Path:
        """Create a temporary file for user storage."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([], f)
            temp_path = Path(f.name)
        yield temp_path
        temp_path.unlink()

    @pytest.fixture
    def auth_manager(self, temp_users_file: Path) -> AuthManager:
        """Create an AuthManager with a temporary storage file."""
        return AuthManager(storage_path=temp_users_file)

    def test_auth_manager_initialization(self, temp_users_file: Path) -> None:
        """Test AuthManager initializes with correct storage path."""
        auth = AuthManager(storage_path=temp_users_file)
        assert auth.storage_path == temp_users_file

    def test_ensure_store_exists_creates_file(self) -> None:
        """Test that _ensure_store_exists creates a file if missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = Path(tmpdir) / "new_users.json"
            AuthManager(storage_path=storage_path)
            assert storage_path.exists()
            assert json.loads(storage_path.read_text()) == []

    def test_ensure_store_exists_with_empty_file(self) -> None:
        """Test that _ensure_store_exists initializes empty files."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("")
            temp_path = Path(f.name)

        try:
            AuthManager(storage_path=temp_path)
            content = json.loads(temp_path.read_text())
            assert content == []
        finally:
            temp_path.unlink()

    def test_register_new_user(self, auth_manager: AuthManager) -> None:
        """Test registering a new user successfully."""
        result = auth_manager.register("newuser", "password123")
        assert result is True

        users = auth_manager._load_users()
        assert len(users) == 1
        assert users[0]["username"] == "newuser"
        assert users[0]["password"] == "password123"

    def test_register_duplicate_username(self, auth_manager: AuthManager) -> None:
        """Test that registering duplicate username fails."""
        auth_manager.register("existinguser", "password123")
        result = auth_manager.register("existinguser", "differentpass")
        assert result is False

    def test_register_empty_username(self, auth_manager: AuthManager) -> None:
        """Test that registering with empty username fails."""
        result = auth_manager.register("", "password123")
        assert result is False

    def test_register_empty_password(self, auth_manager: AuthManager) -> None:
        """Test that registering with empty password fails."""
        result = auth_manager.register("username", "")
        assert result is False

    def test_register_empty_both(self, auth_manager: AuthManager) -> None:
        """Test that registering with both empty fails."""
        result = auth_manager.register("", "")
        assert result is False

    def test_authenticate_valid_credentials(self, auth_manager: AuthManager) -> None:
        """Test authenticating with valid credentials."""
        auth_manager.register("testuser", "testpass")
        result = auth_manager.authenticate("testuser", "testpass")
        assert result is True

    def test_authenticate_invalid_username(self, auth_manager: AuthManager) -> None:
        """Test authenticating with non-existent username."""
        auth_manager.register("testuser", "testpass")
        result = auth_manager.authenticate("wronguser", "testpass")
        assert result is False

    def test_authenticate_invalid_password(self, auth_manager: AuthManager) -> None:
        """Test authenticating with wrong password."""
        auth_manager.register("testuser", "testpass")
        result = auth_manager.authenticate("testuser", "wrongpass")
        assert result is False

    def test_authenticate_empty_credentials(self, auth_manager: AuthManager) -> None:
        """Test authenticating with empty credentials."""
        assert auth_manager.authenticate("", "password") is False
        assert auth_manager.authenticate("username", "") is False
        assert auth_manager.authenticate("", "") is False

    def test_authenticate_no_users(self, auth_manager: AuthManager) -> None:
        """Test authenticating when no users exist."""
        result = auth_manager.authenticate("anyuser", "anypass")
        assert result is False

    def test_multiple_users(self, auth_manager: AuthManager) -> None:
        """Test managing multiple users."""
        auth_manager.register("user1", "pass1")
        auth_manager.register("user2", "pass2")
        auth_manager.register("user3", "pass3")

        assert auth_manager.authenticate("user1", "pass1") is True
        assert auth_manager.authenticate("user2", "pass2") is True
        assert auth_manager.authenticate("user3", "pass3") is True
        assert auth_manager.authenticate("user1", "pass2") is False
