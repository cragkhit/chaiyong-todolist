"""Authentication helpers for the CLI to-do application."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


class AuthManager:
    """Manages user authentication against a local JSON file."""

    def __init__(self, storage_path: str | Path = "users.json") -> None:
        self.storage_path = Path(storage_path)
        self._ensure_store_exists()

    def authenticate(self, username: str, password: str) -> bool:
        """Return True if the given credentials match a stored user."""

        if not username or not password:
            return False

        users = self._load_users()
        return any(
            user.get("username") == username and user.get("password") == password
            for user in users
        )

    def register(self, username: str, password: str) -> bool:
        """Register a new user. Return True if successful, False if user already exists."""

        if not username or not password:
            return False

        users = self._load_users()

        # Check if username already exists
        if any(user.get("username") == username for user in users):
            return False

        # Add the new user
        users.append({"username": username, "password": password})
        self._save_users(users)
        return True

    def _ensure_store_exists(self) -> None:
        """Create the storage file if missing or empty."""

        if not self.storage_path.exists():
            self.storage_path.write_text("[]", encoding="utf-8")
            return

        if not self.storage_path.read_text(encoding="utf-8").strip():
            self.storage_path.write_text("[]", encoding="utf-8")

    def _load_users(self) -> List[Dict[str, str]]:
        """Load user records from disk."""

        try:
            raw = self.storage_path.read_text(encoding="utf-8")
            return json.loads(raw)
        except (OSError, json.JSONDecodeError):
            return []

    def _save_users(self, users: List[Dict[str, str]]) -> None:
        """Save user records to disk."""

        try:
            self.storage_path.write_text(
                json.dumps(users, indent=4), encoding="utf-8"
            )
        except OSError:
            pass
