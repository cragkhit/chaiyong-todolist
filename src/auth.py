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
