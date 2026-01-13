"""Entry point for the CLI to-do list application."""

from __future__ import annotations

from typing import Callable, Dict

from auth import AuthManager


class App:
    """A simple REPL-like CLI shell."""

    def __init__(self, auth_manager: AuthManager | None = None) -> None:
        self._running = True
        self._current_user: str | None = None
        self._auth = auth_manager or AuthManager()
        self._actions: Dict[str, Callable[[], None]] = {
            "1": self._handle_login,
            "2": self._handle_sign_up,
            "3": self._exit_application,
        }

    def run(self) -> None:
        """Start the main application loop."""

        print("Welcome to the CLI To-Do List App!")
        while self._running:
            self._print_pre_login_menu()
            choice = input("Select an option: ").strip()
            self._dispatch(choice)

    def _print_pre_login_menu(self) -> None:
        """Display the pre-login menu options."""

        print("\nPlease choose an action:")
        print("[1] Login")
        print("[2] Sign Up")
        print("[3] Exit")

    def _dispatch(self, choice: str) -> None:
        """Execute the action mapped to the provided menu choice."""

        action = self._actions.get(choice)
        if action is None:
            print("Invalid selection. Please enter 1, 2, or 3.")
            return

        action()

    def _handle_login(self) -> None:
        """Authenticate a user against the stored credentials."""

        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if self._auth.authenticate(username, password):
            self._current_user = username
            print(f"Welcome back, {username}!")
            return

        print("Invalid username or password. Please try again.")

    def _handle_sign_up(self) -> None:
        """Placeholder for sign-up flow until user registration is implemented."""

        print("Sign up is not implemented yet. Please check back soon.")

    def _exit_application(self) -> None:
        """Stop the application loop and exit."""

        print("Goodbye!")
        self._running = False


def main() -> None:
    """Entrypoint for launching the CLI application."""

    app = App()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting application.")


if __name__ == "__main__":
    main()
