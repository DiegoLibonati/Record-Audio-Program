from tkinter import DISABLED, NORMAL, StringVar
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.ui.components.record_controls import RecordControls


@pytest.fixture
def record_controls(mock_styles: MagicMock, mock_on_start: MagicMock, mock_on_stop: MagicMock) -> RecordControls:
    with (
        patch("src.ui.components.record_controls.Frame.__init__", return_value=None),
        patch("src.ui.components.record_controls.Entry"),
        patch("src.ui.components.record_controls.Button"),
        patch("src.ui.components.record_controls.StringVar"),
        patch.object(RecordControls, "columnconfigure"),
    ):
        instance: RecordControls = RecordControls.__new__(RecordControls)
        instance._styles = mock_styles
        instance._on_start = mock_on_start
        instance._on_stop = mock_on_stop
        instance._filename = MagicMock(spec=StringVar)
        instance._start_button = MagicMock()
        instance._stop_button = MagicMock()
        return instance


class TestRecordControlsInit:
    def test_stores_styles(self, record_controls: RecordControls, mock_styles: MagicMock) -> None:
        assert record_controls._styles == mock_styles

    def test_stores_on_start(self, record_controls: RecordControls, mock_on_start: MagicMock) -> None:
        assert record_controls._on_start == mock_on_start

    def test_stores_on_stop(self, record_controls: RecordControls, mock_on_stop: MagicMock) -> None:
        assert record_controls._on_stop == mock_on_stop

    def test_start_button_command_is_on_start(self, mock_styles: MagicMock, mock_on_start: MagicMock, mock_on_stop: MagicMock) -> None:
        with (
            patch("src.ui.components.record_controls.Frame.__init__", return_value=None),
            patch("src.ui.components.record_controls.Entry") as mock_entry,
            patch("src.ui.components.record_controls.Button") as mock_button,
            patch("src.ui.components.record_controls.StringVar"),
            patch.object(RecordControls, "columnconfigure"),
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: RecordControls = RecordControls.__new__(RecordControls)
            instance._styles = mock_styles
            RecordControls.__init__(
                instance,
                parent=MagicMock(),
                styles=mock_styles,
                on_start=mock_on_start,
                on_stop=mock_on_stop,
            )

        first_call_kwargs: dict[str, Any] = mock_button.call_args_list[0].kwargs
        assert first_call_kwargs.get("command") == mock_on_start

    def test_stop_button_command_is_on_stop(self, mock_styles: MagicMock, mock_on_start: MagicMock, mock_on_stop: MagicMock) -> None:
        with (
            patch("src.ui.components.record_controls.Frame.__init__", return_value=None),
            patch("src.ui.components.record_controls.Entry") as mock_entry,
            patch("src.ui.components.record_controls.Button") as mock_button,
            patch("src.ui.components.record_controls.StringVar"),
            patch.object(RecordControls, "columnconfigure"),
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: RecordControls = RecordControls.__new__(RecordControls)
            instance._styles = mock_styles
            RecordControls.__init__(
                instance,
                parent=MagicMock(),
                styles=mock_styles,
                on_start=mock_on_start,
                on_stop=mock_on_stop,
            )

        second_call_kwargs: dict[str, Any] = mock_button.call_args_list[1].kwargs
        assert second_call_kwargs.get("command") == mock_on_stop

    def test_start_button_initial_state_is_normal(self, mock_styles: MagicMock, mock_on_start: MagicMock, mock_on_stop: MagicMock) -> None:
        with (
            patch("src.ui.components.record_controls.Frame.__init__", return_value=None),
            patch("src.ui.components.record_controls.Entry") as mock_entry,
            patch("src.ui.components.record_controls.Button") as mock_button,
            patch("src.ui.components.record_controls.StringVar"),
            patch.object(RecordControls, "columnconfigure"),
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: RecordControls = RecordControls.__new__(RecordControls)
            instance._styles = mock_styles
            RecordControls.__init__(
                instance,
                parent=MagicMock(),
                styles=mock_styles,
                on_start=mock_on_start,
                on_stop=mock_on_stop,
            )

        first_call_kwargs: dict[str, Any] = mock_button.call_args_list[0].kwargs
        assert first_call_kwargs.get("state") == NORMAL

    def test_stop_button_initial_state_is_disabled(self, mock_styles: MagicMock, mock_on_start: MagicMock, mock_on_stop: MagicMock) -> None:
        with (
            patch("src.ui.components.record_controls.Frame.__init__", return_value=None),
            patch("src.ui.components.record_controls.Entry") as mock_entry,
            patch("src.ui.components.record_controls.Button") as mock_button,
            patch("src.ui.components.record_controls.StringVar"),
            patch.object(RecordControls, "columnconfigure"),
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: RecordControls = RecordControls.__new__(RecordControls)
            instance._styles = mock_styles
            RecordControls.__init__(
                instance,
                parent=MagicMock(),
                styles=mock_styles,
                on_start=mock_on_start,
                on_stop=mock_on_stop,
            )

        second_call_kwargs: dict[str, Any] = mock_button.call_args_list[1].kwargs
        assert second_call_kwargs.get("state") == DISABLED


class TestRecordControlsGetFilename:
    def test_returns_filename_value(self, record_controls: RecordControls) -> None:
        record_controls._filename.get.return_value = "my_audio"
        result: str = record_controls.get_filename()
        assert result == "my_audio"

    def test_returns_empty_string_when_empty(self, record_controls: RecordControls) -> None:
        record_controls._filename.get.return_value = ""
        result: str = record_controls.get_filename()
        assert result == ""

    def test_calls_filename_get(self, record_controls: RecordControls) -> None:
        record_controls._filename.get.return_value = "test"
        record_controls.get_filename()
        record_controls._filename.get.assert_called_once()


class TestRecordControlsSetFilename:
    def test_sets_filename_value(self, record_controls: RecordControls) -> None:
        record_controls.set_filename("new_name")
        record_controls._filename.set.assert_called_once_with("new_name")

    def test_sets_empty_string(self, record_controls: RecordControls) -> None:
        record_controls.set_filename("")
        record_controls._filename.set.assert_called_once_with("")


class TestRecordControlsSetRecordingState:
    def test_start_button_disabled_when_recording(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=True)
        record_controls._start_button.config.assert_called_once_with(state=DISABLED)

    def test_stop_button_enabled_when_recording(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=True)
        record_controls._stop_button.config.assert_called_once_with(state=NORMAL)

    def test_start_button_enabled_when_not_recording(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=False)
        record_controls._start_button.config.assert_called_once_with(state=NORMAL)

    def test_stop_button_disabled_when_not_recording(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=False)
        record_controls._stop_button.config.assert_called_once_with(state=DISABLED)


class TestRecordControlsIsRecording:
    def test_returns_true_when_stop_button_is_normal(self, record_controls: RecordControls) -> None:
        record_controls._stop_button.__getitem__ = MagicMock(return_value=NORMAL)
        result: bool = record_controls.is_recording()
        assert result is True

    def test_returns_false_when_stop_button_is_disabled(self, record_controls: RecordControls) -> None:
        record_controls._stop_button.__getitem__ = MagicMock(return_value=DISABLED)
        result: bool = record_controls.is_recording()
        assert result is False
