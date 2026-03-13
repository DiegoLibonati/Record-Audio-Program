from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_NOT_VALID_FILENAME
from src.ui.interface_app import InterfaceApp
from src.ui.styles import Styles
from src.utils.dialogs import ValidationDialogError


@pytest.fixture
def interface_app(mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> InterfaceApp:
    with (
        patch("src.ui.interface_app.MainView") as mock_main_view_class,
        patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
        patch("src.ui.interface_app.PATH_MIC", "mic.png"),
        patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
    ):
        mock_main_view_class.return_value = MagicMock()
        instance: InterfaceApp = InterfaceApp.__new__(InterfaceApp)
        instance._styles = mock_styles
        instance._config = MagicMock()
        instance._root = mock_root
        instance._main_view = mock_main_view_class.return_value
        instance._InterfaceApp__audio = mock_audio
        return instance


class TestInterfaceAppInit:
    def test_stores_styles(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        assert app._styles is mock_styles

    def test_stores_root(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        assert app._root is mock_root

    def test_audio_property_returns_audio(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        assert interface_app.audio is mock_audio

    def test_title_is_set(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        mock_root.title.assert_called_once_with("Record Program")

    def test_geometry_is_set(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        mock_root.geometry.assert_called_once_with("400x400")

    def test_is_not_resizable(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        mock_root.resizable.assert_called_once_with(False, False)

    def test_background_uses_primary_color(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        mock_root.config.assert_called_once_with(background=mock_styles.PRIMARY_COLOR)

    def test_default_styles_is_styles_instance(self, mock_root: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock())
        assert isinstance(app._styles, Styles)

    def test_main_view_receives_callbacks(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        _, kwargs = mock_main_view_class.call_args
        assert callable(kwargs.get("on_start"))
        assert callable(kwargs.get("on_stop"))

    def test_main_view_grid_called(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view: MagicMock = MagicMock()
            mock_main_view_class.return_value = mock_main_view
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        mock_main_view.grid.assert_called_once_with(row=0, column=0, sticky="nsew")

    def test_columnconfigure_called_on_root(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        mock_root.columnconfigure.assert_called_once_with(0, weight=1)

    def test_rowconfigure_called_on_root(self, mock_root: MagicMock, mock_styles: MagicMock, mock_audio: MagicMock, mock_img: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.PhotoImage", return_value=mock_img),
            patch("src.ui.interface_app.PATH_MIC", "mic.png"),
            patch("src.ui.interface_app.PATH_MIC_ON", "mic_on.png"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, audio=mock_audio, config=MagicMock(), styles=mock_styles)
        mock_root.rowconfigure.assert_called_once_with(0, weight=1)


class TestInterfaceAppPerformStartRecord:
    def test_raises_validation_error_when_filename_is_empty(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = ""
        with pytest.raises(ValidationDialogError) as exc_info:
            interface_app._perform_start_record()
        assert exc_info.value.message == MESSAGE_NOT_VALID_FILENAME

    def test_set_recording_state_not_called_when_filename_is_empty(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = ""
        with pytest.raises(ValidationDialogError):
            interface_app._perform_start_record()
        interface_app._main_view.set_recording_state.assert_not_called()

    def test_set_recording_state_called_with_true(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        with patch.object(interface_app, "_set_timer"):
            interface_app._perform_start_record()
        interface_app._main_view.set_recording_state.assert_called_once_with(recording=True)

    def test_audio_start_record_called(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        with patch.object(interface_app, "_set_timer"):
            interface_app._perform_start_record()
        interface_app.audio.start_record.assert_called_once()

    def test_set_timer_called(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        with patch.object(interface_app, "_set_timer") as mock_set_timer:
            interface_app._perform_start_record()
        mock_set_timer.assert_called_once()

    def test_audio_start_record_not_called_when_filename_is_empty(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = ""
        with pytest.raises(ValidationDialogError):
            interface_app._perform_start_record()
        interface_app.audio.start_record.assert_not_called()


class TestInterfaceAppPerformStopRecord:
    def test_set_recording_state_called_with_false(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        interface_app.audio.seconds = 5
        interface_app.audio.minutes = 0
        interface_app.audio.stop_record.return_value = True

        interface_app._perform_stop_record()

        interface_app._main_view.set_recording_state.assert_called_once_with(recording=False)

    def test_set_status_called_with_finished_message(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        interface_app.audio.seconds = 5
        interface_app.audio.minutes = 0
        interface_app.audio.stop_record.return_value = True

        interface_app._perform_stop_record()

        call_args: str = interface_app._main_view.set_status.call_args[0][0]
        assert "my_recording" in call_args
        assert "00:05" in call_args

    def test_stop_record_called_with_filename(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        interface_app.audio.seconds = 0
        interface_app.audio.minutes = 0
        interface_app.audio.stop_record.return_value = True

        interface_app._perform_stop_record()

        interface_app.audio.stop_record.assert_called_once_with(filename="my_recording")

    def test_set_filename_called_when_stop_record_returns_true(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        interface_app.audio.seconds = 0
        interface_app.audio.minutes = 0
        interface_app.audio.stop_record.return_value = True

        interface_app._perform_stop_record()

        interface_app._main_view.set_filename.assert_called_once_with("Insert a new one!.")

    def test_set_filename_not_called_when_stop_record_returns_false(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_filename.return_value = "my_recording"
        interface_app.audio.seconds = 0
        interface_app.audio.minutes = 0
        interface_app.audio.stop_record.return_value = False

        interface_app._perform_stop_record()

        interface_app._main_view.set_filename.assert_not_called()


class TestInterfaceAppSetTimer:
    def test_set_status_called_when_recording(self, interface_app: InterfaceApp, mock_root: MagicMock) -> None:
        interface_app.audio.end_audio = False
        interface_app.audio.seconds = 3
        interface_app.audio.minutes = 0
        interface_app._main_view.is_recording.return_value = True

        interface_app._set_timer()

        interface_app._main_view.set_status.assert_called_once_with("00:03")

    def test_root_after_called_when_recording(self, interface_app: InterfaceApp, mock_root: MagicMock) -> None:
        interface_app.audio.end_audio = False
        interface_app._main_view.is_recording.return_value = True
        interface_app.audio.seconds = 0
        interface_app.audio.minutes = 0

        interface_app._set_timer()

        args, _ = mock_root.after.call_args
        assert args[0] == 1000
        assert args[1] == interface_app._set_timer

    def test_set_status_not_called_when_end_audio_is_true(self, interface_app: InterfaceApp) -> None:
        interface_app.audio.end_audio = True
        interface_app._main_view.is_recording.return_value = True

        interface_app._set_timer()

        interface_app._main_view.set_status.assert_not_called()

    def test_root_after_not_called_when_not_recording(self, interface_app: InterfaceApp, mock_root: MagicMock) -> None:
        interface_app.audio.end_audio = False
        interface_app._main_view.is_recording.return_value = False

        interface_app._set_timer()

        mock_root.after.assert_not_called()


class TestInterfaceAppParseTimer:
    def test_both_under_10(self) -> None:
        assert InterfaceApp._parse_timer(seconds=5, minutes=3) == "03:05"

    def test_seconds_under_10_minutes_over_10(self) -> None:
        assert InterfaceApp._parse_timer(seconds=5, minutes=12) == "12:05"

    def test_seconds_over_10_minutes_under_10(self) -> None:
        assert InterfaceApp._parse_timer(seconds=45, minutes=3) == "03:45"

    def test_both_over_10(self) -> None:
        assert InterfaceApp._parse_timer(seconds=30, minutes=15) == "15:30"

    def test_both_exactly_10(self) -> None:
        assert InterfaceApp._parse_timer(seconds=10, minutes=10) == "10:10"

    def test_seconds_zero_minutes_zero(self) -> None:
        assert InterfaceApp._parse_timer(seconds=0, minutes=0) == "00:00"

    def test_seconds_59_minutes_9(self) -> None:
        assert InterfaceApp._parse_timer(seconds=59, minutes=9) == "09:59"
