"""Unit tests for the CLI application and menu interface."""

from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from auth import AuthManager
from main import App


class TestApp:
    """Tests for the App class."""

    @pytest.fixture
    def mock_auth_manager(self) -> MagicMock:
        """Create a mock AuthManager for testing."""
        return MagicMock(spec=AuthManager)

    @pytest.fixture
    def app(self, mock_auth_manager: MagicMock) -> App:
        """Create an App instance with mocked AuthManager."""
        return App(auth_manager=mock_auth_manager)

    def test_app_initialization(self, mock_auth_manager: MagicMock) -> None:
        """Test App initializes with correct default state."""
        app = App(auth_manager=mock_auth_manager)
        assert app._running is True
        assert app._current_user is None
        assert app._auth == mock_auth_manager

    def test_app_initialization_without_auth_manager(self) -> None:
        """Test App creates default AuthManager if none provided."""
        app = App()
        assert app._auth is not None
        assert isinstance(app._auth, AuthManager)

    def test_app_actions_mapping(self, app: App) -> None:
        """Test App has correct action mappings."""
        assert "1" in app._actions
        assert "2" in app._actions
        assert "3" in app._actions

    def test_print_pre_login_menu(self, app: App, capsys: object) -> None:
        """Test pre-login menu is printed correctly."""
        app._print_pre_login_menu()
        captured = capsys.readouterr()

        assert "Please choose an action:" in captured.out
        assert "[1] Login" in captured.out
        assert "[2] Sign Up" in captured.out
        assert "[3] Exit" in captured.out

    def test_dispatch_login_action(self, app: App) -> None:
        """Test dispatch routes to login handler."""
        mock_login = MagicMock()
        app._actions["1"] = mock_login
        app._dispatch("1")
        mock_login.assert_called_once()

    def test_dispatch_signup_action(self, app: App) -> None:
        """Test dispatch routes to sign up handler."""
        mock_signup = MagicMock()
        app._actions["2"] = mock_signup
        app._dispatch("2")
        mock_signup.assert_called_once()

    def test_dispatch_exit_action(self, app: App) -> None:
        """Test dispatch routes to exit handler."""
        mock_exit = MagicMock()
        app._actions["3"] = mock_exit
        app._dispatch("3")
        mock_exit.assert_called_once()

    def test_dispatch_invalid_action(self, app: App, capsys: object) -> None:
        """Test dispatch handles invalid choice gracefully."""
        app._dispatch("4")
        captured = capsys.readouterr()
        assert "Invalid selection" in captured.out

    def test_dispatch_empty_choice(self, app: App, capsys: object) -> None:
        """Test dispatch handles empty choice."""
        app._dispatch("")
        captured = capsys.readouterr()
        assert "Invalid selection" in captured.out


class TestAppLoginFlow:
    """Tests for the login flow."""

    @pytest.fixture
    def app(self) -> App:
        """Create an App with mocked AuthManager."""
        mock_auth = MagicMock(spec=AuthManager)
        return App(auth_manager=mock_auth)

    def test_handle_login_success(self, app: App, capsys: object) -> None:
        """Test successful login flow."""
        app._auth.authenticate.return_value = True

        with patch("builtins.input", side_effect=["testuser", "password123"]):
            app._handle_login()

        assert app._current_user == "testuser"
        app._auth.authenticate.assert_called_once_with("testuser", "password123")
        captured = capsys.readouterr()
        assert "Welcome back, testuser!" in captured.out

    def test_handle_login_failure(self, app: App, capsys: object) -> None:
        """Test failed login attempt."""
        app._auth.authenticate.return_value = False

        with patch("builtins.input", side_effect=["wronguser", "wrongpass"]):
            app._handle_login()

        assert app._current_user is None
        captured = capsys.readouterr()
        assert "Invalid username or password" in captured.out

    def test_handle_login_with_whitespace(self, app: App) -> None:
        """Test login strips whitespace from inputs."""
        app._auth.authenticate.return_value = True

        with patch("builtins.input", side_effect=["  testuser  ", "  password  "]):
            app._handle_login()

        app._auth.authenticate.assert_called_once_with("testuser", "password")


class TestAppSignupFlow:
    """Tests for the sign up flow."""

    @pytest.fixture
    def app(self) -> App:
        """Create an App with mocked AuthManager."""
        mock_auth = MagicMock(spec=AuthManager)
        return App(auth_manager=mock_auth)

    def test_handle_sign_up_success(self, app: App, capsys: object) -> None:
        """Test successful sign up flow."""
        app._auth.register.return_value = True

        with patch(
            "builtins.input",
            side_effect=["newuser", "password123", "password123"],
        ):
            app._handle_sign_up()

        app._auth.register.assert_called_once_with("newuser", "password123")
        captured = capsys.readouterr()
        assert "Account created successfully" in captured.out

    def test_handle_sign_up_passwords_mismatch(self, app: App, capsys: object) -> None:
        """Test sign up fails when passwords don't match."""
        with patch(
            "builtins.input",
            side_effect=["newuser", "password123", "different123"],
        ):
            app._handle_sign_up()

        app._auth.register.assert_not_called()
        captured = capsys.readouterr()
        assert "Passwords do not match" in captured.out

    def test_handle_sign_up_empty_username(self, app: App, capsys: object) -> None:
        """Test sign up fails with empty username."""
        with patch("builtins.input", side_effect=["", "password123", "password123"]):
            app._handle_sign_up()

        app._auth.register.assert_not_called()
        captured = capsys.readouterr()
        assert "Username and password cannot be empty" in captured.out

    def test_handle_sign_up_empty_password(self, app: App, capsys: object) -> None:
        """Test sign up fails with empty password."""
        with patch("builtins.input", side_effect=["newuser", "", ""]):
            app._handle_sign_up()

        app._auth.register.assert_not_called()
        captured = capsys.readouterr()
        assert "Username and password cannot be empty" in captured.out

    def test_handle_sign_up_username_exists(self, app: App, capsys: object) -> None:
        """Test sign up fails when username already exists."""
        app._auth.register.return_value = False

        with patch(
            "builtins.input",
            side_effect=["existinguser", "password123", "password123"],
        ):
            app._handle_sign_up()

        captured = capsys.readouterr()
        assert "Username already exists" in captured.out

    def test_handle_sign_up_with_whitespace(self, app: App) -> None:
        """Test sign up strips whitespace from inputs."""
        app._auth.register.return_value = True

        with patch(
            "builtins.input",
            side_effect=["  newuser  ", "  password123  ", "  password123  "],
        ):
            app._handle_sign_up()

        app._auth.register.assert_called_once_with("newuser", "password123")


class TestAppExitFlow:
    """Tests for the exit flow."""

    @pytest.fixture
    def app(self) -> App:
        """Create an App with mocked AuthManager."""
        mock_auth = MagicMock(spec=AuthManager)
        return App(auth_manager=mock_auth)

    def test_exit_application(self, app: App, capsys: object) -> None:
        """Test exit application stops the loop."""
        assert app._running is True
        app._exit_application()
        assert app._running is False
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out


class TestAppMainLoop:
    """Tests for the main application loop."""

    @pytest.fixture
    def app(self) -> App:
        """Create an App with mocked AuthManager."""
        mock_auth = MagicMock(spec=AuthManager)
        return App(auth_manager=mock_auth)

    def test_run_exits_on_keyboard_interrupt(self, app: App, capsys: object) -> None:
        """Test that KeyboardInterrupt is handled gracefully."""
        with patch("builtins.input", side_effect=KeyboardInterrupt()):
            from main import main

            with patch("builtins.print"):
                with patch("sys.exit"):
                    try:
                        app.run()
                    except KeyboardInterrupt:
                        pass

    def test_run_with_exit_command(self, app: App, capsys: object) -> None:
        """Test run loop exits when user selects exit."""
        with patch("builtins.input", side_effect=["3"]):
            app.run()

        assert app._running is False
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_run_multiple_invalid_choices(self, app: App, capsys: object) -> None:
        """Test run loop handles multiple invalid choices before exit."""
        with patch("builtins.input", side_effect=["9", "invalid", "3"]):
            app.run()

        assert app._running is False
        captured = capsys.readouterr()
        assert "Invalid selection" in captured.out
        assert "Goodbye!" in captured.out
