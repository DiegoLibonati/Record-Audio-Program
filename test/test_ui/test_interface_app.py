from unittest.mock import MagicMock, patch

import pytest

from src.ui.interface_app import InterfaceApp
from src.ui.styles import Styles


@pytest.fixture
def interface_app(mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock) -> InterfaceApp:
    with (
        patch("src.ui.interface_app.MainView") as mock_main_view_class,
        patch("src.ui.interface_app.PhotoImage"),
    ):
        mock_main_view: MagicMock = MagicMock()
        mock_main_view.grid = MagicMock()
        mock_main_view_class.return_value = mock_main_view
        instance: InterfaceApp = InterfaceApp.__new__(InterfaceApp)
        instance._styles = mock_styles
        instance._root = mock_root
        instance._config = MagicMock()
        instance._main_view = mock_main_view
        instance._InterfaceApp__audio = mock_audio
        return instance


class TestInterfaceAppInit:
    def test_stores_styles(self, interface_app: InterfaceApp, mock_styles: MagicMock) -> None:
        assert interface_app._styles == mock_styles

    def test_stores_root(self, interface_app: InterfaceApp, mock_root: MagicMock) -> None:
        assert interface_app._root == mock_root

    def test_audio_property_returns_audio(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        assert interface_app.audio == mock_audio

    def test_title_is_set(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)

        mock_root.title.assert_called_once_with("Record Program")

    def test_geometry_is_set(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)

        mock_root.geometry.assert_called_once_with("400x400")

    def test_is_not_resizable(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)

        mock_root.resizable.assert_called_once_with(False, False)

    def test_default_styles_is_styles_instance(self, mock_root: MagicMock, mock_audio: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock())

        assert isinstance(app._styles, Styles)


class TestInterfaceAppPerformStartRecord:
    def test_set_status_called_when_filename_is_empty(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = ""
        interface_app._perform_start_record()
        interface_app._main_view.set_status.assert_called_once_with("You must enter a valid filename.")

    def test_audio_start_record_not_called_when_filename_is_empty(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = ""
        interface_app._perform_start_record()
        interface_app.audio.start_record.assert_not_called()

    def test_set_recording_state_called_when_filename_is_valid(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_audio"

        with patch.object(interface_app, "_set_timer"):
            interface_app._perform_start_record()

        interface_app._main_view.set_recording_state.assert_called_once_with(recording=True)

    def test_audio_start_record_called_when_filename_is_valid(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_audio"

        with patch.object(interface_app, "_set_timer"):
            interface_app._perform_start_record()

        interface_app.audio.start_record.assert_called_once()

    def test_set_timer_called_when_filename_is_valid(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_audio"

        with patch.object(interface_app, "_set_timer") as mock_set_timer:
            interface_app._perform_start_record()

        mock_set_timer.assert_called_once()


class TestInterfaceAppPerformStopRecord:
    def test_set_recording_state_called_with_false(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_audio"
        interface_app.audio.seconds = 5
        interface_app.audio.minutes = 0

        interface_app._perform_stop_record()

        interface_app._main_view.set_recording_state.assert_called_once_with(recording=False)

    def test_audio_stop_record_called_with_filename(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_audio"
        interface_app.audio.seconds = 5
        interface_app.audio.minutes = 0

        interface_app._perform_stop_record()

        interface_app.audio.stop_record.assert_called_once_with(filename="my_audio")

    def test_set_filename_called_after_stop(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_audio"
        interface_app.audio.seconds = 5
        interface_app.audio.minutes = 0

        interface_app._perform_stop_record()

        interface_app._main_view.set_filename.assert_called_once_with("Insert a new one!.")

    def test_set_status_includes_filename(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_audio"
        interface_app.audio.seconds = 5
        interface_app.audio.minutes = 0

        interface_app._perform_stop_record()

        call_arg: str = interface_app._main_view.set_status.call_args[0][0]
        assert "my_audio" in call_arg


class TestInterfaceAppParseTimer:
    def test_both_below_ten(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=5, minutes=3)
        assert result == "03:05"

    def test_seconds_below_ten_minutes_above_ten(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=5, minutes=12)
        assert result == "12:05"

    def test_seconds_above_ten_minutes_below_ten(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=45, minutes=3)
        assert result == "03:45"

    def test_both_above_ten(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=45, minutes=12)
        assert result == "12:45"

    def test_zero_seconds_zero_minutes(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=0, minutes=0)
        assert result == "00:00"

    def test_exactly_ten_seconds(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=10, minutes=0)
        assert result == "00:10"

    def test_exactly_ten_minutes(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=0, minutes=10)
        assert result == "10:00"
