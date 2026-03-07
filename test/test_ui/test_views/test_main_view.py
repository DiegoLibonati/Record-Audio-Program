from tkinter import StringVar
from unittest.mock import MagicMock, patch

import pytest

from src.ui.views.main_view import MainView


@pytest.fixture
def main_view(mock_root: MagicMock, mock_styles: MagicMock, mock_on_start: MagicMock, mock_on_stop: MagicMock, mock_img: MagicMock) -> MainView:
    with (
        patch("src.ui.views.main_view.Frame.__init__", return_value=None),
        patch("src.ui.views.main_view.RecordControls"),
        patch("src.ui.views.main_view.Label"),
        patch("src.ui.views.main_view.StringVar"),
        patch.object(MainView, "columnconfigure"),
    ):
        instance: MainView = MainView.__new__(MainView)
        instance._styles = mock_styles
        instance._on_start = mock_on_start
        instance._on_stop = mock_on_stop
        instance._img_record_off = mock_img
        instance._img_record_on = mock_img
        instance._status_text = MagicMock(spec=StringVar)
        instance._label_image = MagicMock()
        instance._record_controls = MagicMock()
        return instance


class TestMainViewInit:
    def test_stores_styles(self, main_view: MainView, mock_styles: MagicMock) -> None:
        assert main_view._styles == mock_styles

    def test_stores_on_start(self, main_view: MainView, mock_on_start: MagicMock) -> None:
        assert main_view._on_start == mock_on_start

    def test_stores_on_stop(self, main_view: MainView, mock_on_stop: MagicMock) -> None:
        assert main_view._on_stop == mock_on_stop

    def test_stores_img_record_off(self, main_view: MainView, mock_img: MagicMock) -> None:
        assert main_view._img_record_off == mock_img

    def test_stores_img_record_on(self, main_view: MainView, mock_img: MagicMock) -> None:
        assert main_view._img_record_on == mock_img

    def test_status_text_initial_value(
        self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_start: MagicMock, mock_on_stop: MagicMock, mock_img: MagicMock
    ) -> None:
        with (
            patch("src.ui.views.main_view.Frame.__init__", return_value=None),
            patch("src.ui.views.main_view.RecordControls") as mock_record_controls,
            patch("src.ui.views.main_view.Label") as mock_label,
            patch("src.ui.views.main_view.StringVar") as mock_string_var,
            patch.object(MainView, "columnconfigure"),
        ):
            mock_record_controls.return_value.grid = MagicMock()
            mock_label.return_value.grid = MagicMock()
            instance: MainView = MainView.__new__(MainView)
            instance._styles = mock_styles
            MainView.__init__(
                instance,
                root=mock_root,
                styles=mock_styles,
                img_record_off=mock_img,
                img_record_on=mock_img,
                on_start=mock_on_start,
                on_stop=mock_on_stop,
            )

        mock_string_var.assert_called_once_with(value="Starts")

    def test_record_controls_receives_on_start(
        self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_start: MagicMock, mock_on_stop: MagicMock, mock_img: MagicMock
    ) -> None:
        with (
            patch("src.ui.views.main_view.Frame.__init__", return_value=None),
            patch("src.ui.views.main_view.RecordControls") as mock_record_controls,
            patch("src.ui.views.main_view.Label") as mock_label,
            patch("src.ui.views.main_view.StringVar"),
            patch.object(MainView, "columnconfigure"),
        ):
            mock_record_controls.return_value.grid = MagicMock()
            mock_label.return_value.grid = MagicMock()
            instance: MainView = MainView.__new__(MainView)
            instance._styles = mock_styles
            MainView.__init__(
                instance,
                root=mock_root,
                styles=mock_styles,
                img_record_off=mock_img,
                img_record_on=mock_img,
                on_start=mock_on_start,
                on_stop=mock_on_stop,
            )

        _, kwargs = mock_record_controls.call_args
        assert kwargs.get("on_start") == mock_on_start

    def test_record_controls_receives_on_stop(
        self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_start: MagicMock, mock_on_stop: MagicMock, mock_img: MagicMock
    ) -> None:
        with (
            patch("src.ui.views.main_view.Frame.__init__", return_value=None),
            patch("src.ui.views.main_view.RecordControls") as mock_record_controls,
            patch("src.ui.views.main_view.Label") as mock_label,
            patch("src.ui.views.main_view.StringVar"),
            patch.object(MainView, "columnconfigure"),
        ):
            mock_record_controls.return_value.grid = MagicMock()
            mock_label.return_value.grid = MagicMock()
            instance: MainView = MainView.__new__(MainView)
            instance._styles = mock_styles
            MainView.__init__(
                instance,
                root=mock_root,
                styles=mock_styles,
                img_record_off=mock_img,
                img_record_on=mock_img,
                on_start=mock_on_start,
                on_stop=mock_on_stop,
            )

        _, kwargs = mock_record_controls.call_args
        assert kwargs.get("on_stop") == mock_on_stop


class TestMainViewGetFilename:
    def test_delegates_to_record_controls(self, main_view: MainView) -> None:
        main_view._record_controls.get_filename.return_value = "my_audio"
        result: str = main_view.get_filename()
        assert result == "my_audio"

    def test_calls_record_controls_get_filename(self, main_view: MainView) -> None:
        main_view._record_controls.get_filename.return_value = "test"
        main_view.get_filename()
        main_view._record_controls.get_filename.assert_called_once()


class TestMainViewSetFilename:
    def test_delegates_to_record_controls(self, main_view: MainView) -> None:
        main_view.set_filename("new_name")
        main_view._record_controls.set_filename.assert_called_once_with("new_name")


class TestMainViewSetStatus:
    def test_sets_status_text(self, main_view: MainView) -> None:
        main_view.set_status("Recording...")
        main_view._status_text.set.assert_called_once_with("Recording...")

    def test_sets_empty_string(self, main_view: MainView) -> None:
        main_view.set_status("")
        main_view._status_text.set.assert_called_once_with("")


class TestMainViewSetRecordingState:
    def test_label_image_updated_to_record_on_when_recording(self, main_view: MainView) -> None:
        main_view.set_recording_state(recording=True)
        main_view._label_image.config.assert_called_once_with(image=main_view._img_record_on)

    def test_label_image_updated_to_record_off_when_not_recording(self, main_view: MainView) -> None:
        main_view.set_recording_state(recording=False)
        main_view._label_image.config.assert_called_once_with(image=main_view._img_record_off)

    def test_record_controls_set_recording_state_is_called(self, main_view: MainView) -> None:
        main_view.set_recording_state(recording=True)
        main_view._record_controls.set_recording_state.assert_called_once_with(recording=True)


class TestMainViewIsRecording:
    def test_delegates_to_record_controls(self, main_view: MainView) -> None:
        main_view._record_controls.is_recording.return_value = True
        result: bool = main_view.is_recording()
        assert result is True

    def test_returns_false_when_not_recording(self, main_view: MainView) -> None:
        main_view._record_controls.is_recording.return_value = False
        result: bool = main_view.is_recording()
        assert result is False
