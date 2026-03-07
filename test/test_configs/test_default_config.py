import os

import pytest

from src.configs.default_config import DefaultConfig


class TestDefaultConfigTimezone:
    def test_default_timezone(self) -> None:
        if "TZ" not in os.environ:
            assert DefaultConfig().TZ == "America/Argentina/Buenos_Aires"

    def test_timezone_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("TZ", "UTC")
        result = os.getenv("TZ", "America/Argentina/Buenos_Aires")
        assert result == "UTC"

    def test_timezone_is_string(self) -> None:
        assert isinstance(DefaultConfig().TZ, str)


class TestDefaultConfigFlags:
    def test_debug_is_false(self) -> None:
        assert DefaultConfig().DEBUG is False

    def test_testing_is_false(self) -> None:
        assert DefaultConfig().TESTING is False

    def test_debug_is_bool(self) -> None:
        assert isinstance(DefaultConfig().DEBUG, bool)

    def test_testing_is_bool(self) -> None:
        assert isinstance(DefaultConfig().TESTING, bool)


class TestDefaultConfigEnvName:
    def test_default_env_name(self) -> None:
        if "ENV_NAME" not in os.environ:
            assert DefaultConfig().ENV_NAME == "template tkinter python"

    def test_env_name_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENV_NAME", "my-custom-app")
        result = os.getenv("ENV_NAME", "template tkinter python")
        assert result == "my-custom-app"

    def test_env_name_is_string(self) -> None:
        assert isinstance(DefaultConfig().ENV_NAME, str)
