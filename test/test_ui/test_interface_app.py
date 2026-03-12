from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_NOT_VALID_FILENAME
from src.ui.interface_app import InterfaceApp
from src.ui.styles import Styles


@pytest.fixture
def interface_app(mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock) -> InterfaceApp:
    with (
        patch("src.ui.interface_app.MainView") as mock_main_view_class,
        patch("src.ui.interface_app.PhotoImage"),
        patch("src.ui.interface_app.PATH_MIC", "mic.png"),
        patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
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

    def test_audio_property_returns_stored_audio(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        assert interface_app.audio is mock_audio

    def test_title_is_set(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage"),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)

        mock_root.title.assert_called_once_with("Record Program")

    def test_geometry_is_set(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage"),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)

        mock_root.geometry.assert_called_once_with("400x400")

    def test_is_not_resizable(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage"),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)

        mock_root.resizable.assert_called_once_with(False, False)

    def test_default_styles_is_styles_instance(self, mock_root: MagicMock, mock_audio: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage"),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock())

        assert isinstance(app._styles, Styles)

    def test_main_view_receives_on_start_and_on_stop(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage"),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)

        _, kwargs = mock_main_view_class.call_args
        assert callable(kwargs.get("on_start"))
        assert callable(kwargs.get("on_stop"))


class TestInterfaceAppPerformStartRecord:
    def test_validation_dialog_called_when_filename_is_empty(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = ""

        with patch("src.ui.interface_app.ValidationDialogError") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._perform_start_record()

        mock_dialog_class.assert_called_once_with(message=MESSAGE_NOT_VALID_FILENAME)
        mock_dialog_class.return_value.dialog.assert_called_once()

    def test_audio_start_not_called_when_filename_is_empty(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.get_filename.return_value = ""

        with patch("src.ui.interface_app.ValidationDialogError") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._perform_start_record()

        mock_audio.start_record.assert_not_called()

    def test_set_recording_state_called_with_true(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        interface_app._main_view.is_recording.return_value = False

        with patch.object(interface_app, "_set_timer"):
            interface_app._perform_start_record()

        interface_app._main_view.set_recording_state.assert_called_once_with(recording=True)

    def test_audio_start_record_called(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        interface_app._main_view.is_recording.return_value = False

        with patch.object(interface_app, "_set_timer"):
            interface_app._perform_start_record()

        mock_audio.start_record.assert_called_once()

    def test_set_timer_called_when_filename_is_valid(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        interface_app._main_view.is_recording.return_value = False

        with patch.object(interface_app, "_set_timer") as mock_set_timer:
            interface_app._perform_start_record()

        mock_set_timer.assert_called_once()


class TestInterfaceAppPerformStopRecord:
    def test_set_recording_state_called_with_false(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        mock_audio.seconds = 5
        mock_audio.minutes = 0

        interface_app._perform_stop_record()

        interface_app._main_view.set_recording_state.assert_called_once_with(recording=False)

    def test_set_status_called_with_formatted_message(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        mock_audio.seconds = 5
        mock_audio.minutes = 0

        interface_app._perform_stop_record()

        call_arg: str = interface_app._main_view.set_status.call_args[0][0]
        assert "my_recording" in call_arg
        assert "Finished in:" in call_arg

    def test_audio_stop_record_called_with_filename(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        mock_audio.seconds = 5
        mock_audio.minutes = 0

        interface_app._perform_stop_record()

        mock_audio.stop_record.assert_called_once_with(filename="my_recording")

    def test_set_filename_reset_after_stop(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        mock_audio.seconds = 5
        mock_audio.minutes = 0

        interface_app._perform_stop_record()

        interface_app._main_view.set_filename.assert_called_once_with("Insert a new one!.")


class TestInterfaceAppSetTimer:
    def test_set_status_called_when_recording(self, interface_app: InterfaceApp, mock_audio: MagicMock, mock_root: MagicMock) -> None:
        mock_audio.end_audio = False
        mock_audio.seconds = 5
        mock_audio.minutes = 0
        interface_app._main_view.is_recording.return_value = True

        interface_app._set_timer()

        interface_app._main_view.set_status.assert_called_once()

    def test_root_after_called_when_recording(self, interface_app: InterfaceApp, mock_audio: MagicMock, mock_root: MagicMock) -> None:
        mock_audio.end_audio = False
        mock_audio.seconds = 5
        mock_audio.minutes = 0
        interface_app._main_view.is_recording.return_value = True

        interface_app._set_timer()

        args, _ = mock_root.after.call_args
        assert args[0] == 1000
        assert args[1] == interface_app._set_timer

    def test_set_status_not_called_when_end_audio_is_true(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        mock_audio.end_audio = True
        interface_app._main_view.is_recording.return_value = True

        interface_app._set_timer()

        interface_app._main_view.set_status.assert_not_called()

    def test_set_status_not_called_when_not_recording(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        mock_audio.end_audio = False
        interface_app._main_view.is_recording.return_value = False

        interface_app._set_timer()

        interface_app._main_view.set_status.assert_not_called()


class TestInterfaceAppParseTimer:
    def test_both_under_ten_adds_leading_zeros(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=5, minutes=3)
        assert result == "03:05"

    def test_seconds_under_ten_minutes_ten_or_more(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=5, minutes=10)
        assert result == "10:05"

    def test_seconds_ten_or_more_minutes_under_ten(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=15, minutes=3)
        assert result == "03:15"

    def test_both_ten_or_more_no_leading_zeros(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=45, minutes=12)
        assert result == "12:45"

    def test_seconds_zero_minutes_zero(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=0, minutes=0)
        assert result == "00:00"

    def test_seconds_exactly_ten(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=10, minutes=0)
        assert result == "00:10"

    def test_minutes_exactly_ten(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=5, minutes=10)
        assert result == "10:05"

    def test_returns_string(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=5, minutes=3)
        assert isinstance(result, str)

    def test_result_contains_colon(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=5, minutes=3)
        assert ":" in result
