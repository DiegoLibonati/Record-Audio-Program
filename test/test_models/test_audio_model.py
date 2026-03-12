from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_ERROR_AUDIO_NOT_STARTED, MESSAGE_NOT_VALID_FILENAME_SAVE
from src.models.audio_model import AudioModel


@pytest.fixture
def audio_model() -> AudioModel:
    with patch("src.models.audio_model.pyaudio.PyAudio"):
        return AudioModel(chunk=1024, sample_format=16, channels=1, fs=44100)


class TestAudioModelInit:
    def test_chunk_is_stored(self, audio_model: AudioModel) -> None:
        assert audio_model.chunk == 1024

    def test_sample_format_is_stored(self, audio_model: AudioModel) -> None:
        assert audio_model.sample_format == 16

    def test_channels_is_stored(self, audio_model: AudioModel) -> None:
        assert audio_model.channels == 1

    def test_fs_is_stored(self, audio_model: AudioModel) -> None:
        assert audio_model.fs == 44100

    def test_seconds_initial_value_is_zero(self, audio_model: AudioModel) -> None:
        assert audio_model.seconds == 0

    def test_minutes_initial_value_is_zero(self, audio_model: AudioModel) -> None:
        assert audio_model.minutes == 0

    def test_stream_initial_value_is_none(self, audio_model: AudioModel) -> None:
        assert audio_model.stream is None

    def test_frames_initial_value_is_empty_list(self, audio_model: AudioModel) -> None:
        assert audio_model.frames == []

    def test_end_audio_initial_value_is_false(self, audio_model: AudioModel) -> None:
        assert audio_model.end_audio is False

    def test_recording_thread_initial_value_is_none(self, audio_model: AudioModel) -> None:
        assert audio_model.recording_thread is None

    def test_timer_thread_initial_value_is_none(self, audio_model: AudioModel) -> None:
        assert audio_model.timer_thread is None


class TestAudioModelStartRecord:
    def test_stream_is_opened_with_correct_params(self, audio_model: AudioModel) -> None:
        mock_thread_instance: MagicMock = MagicMock()
        with patch("src.models.audio_model.threading.Thread", return_value=mock_thread_instance):
            audio_model.start_record()

        audio_model._AudioModel__py_audio.open.assert_called_once_with(
            format=16,
            channels=1,
            rate=44100,
            frames_per_buffer=1024,
            input=True,
        )

    def test_recording_thread_is_set_after_start(self, audio_model: AudioModel) -> None:
        mock_thread_instance: MagicMock = MagicMock()
        with patch("src.models.audio_model.threading.Thread", return_value=mock_thread_instance):
            audio_model.start_record()

        assert audio_model.recording_thread is not None

    def test_timer_thread_is_set_after_start(self, audio_model: AudioModel) -> None:
        mock_thread_instance: MagicMock = MagicMock()
        with patch("src.models.audio_model.threading.Thread", return_value=mock_thread_instance):
            audio_model.start_record()

        assert audio_model.timer_thread is not None

    def test_both_threads_are_started(self, audio_model: AudioModel) -> None:
        mock_thread_instance: MagicMock = MagicMock()
        with patch("src.models.audio_model.threading.Thread", return_value=mock_thread_instance):
            audio_model.start_record()

        assert mock_thread_instance.start.call_count == 2

    def test_stream_is_assigned(self, audio_model: AudioModel) -> None:
        mock_thread_instance: MagicMock = MagicMock()
        with patch("src.models.audio_model.threading.Thread", return_value=mock_thread_instance):
            audio_model.start_record()

        assert audio_model.stream is not None


class TestAudioModelStopRecord:
    def test_validation_dialog_called_when_filename_is_empty(self, audio_model: AudioModel) -> None:
        with (
            patch("src.models.audio_model.ValidationDialogError") as mock_dialog_class,
            patch("src.models.audio_model.pyaudio.PyAudio"),
        ):
            mock_dialog_class.return_value = MagicMock()
            audio_model.stop_record(filename="")

        mock_dialog_class.assert_called_once_with(message=MESSAGE_NOT_VALID_FILENAME_SAVE)
        mock_dialog_class.return_value.dialog.assert_called_once()

    def test_validation_dialog_called_when_filename_is_whitespace(self, audio_model: AudioModel) -> None:
        with (
            patch("src.models.audio_model.ValidationDialogError") as mock_dialog_class,
            patch("src.models.audio_model.pyaudio.PyAudio"),
        ):
            mock_dialog_class.return_value = MagicMock()
            audio_model.stop_record(filename="   ")

        mock_dialog_class.assert_called_once_with(message=MESSAGE_NOT_VALID_FILENAME_SAVE)
        mock_dialog_class.return_value.dialog.assert_called_once()

    def test_reset_state_called_when_filename_is_empty(self, audio_model: AudioModel) -> None:
        with (
            patch("src.models.audio_model.ValidationDialogError") as mock_dialog_class,
            patch("src.models.audio_model.pyaudio.PyAudio"),
            patch.object(audio_model, "_reset_state") as mock_reset,
        ):
            mock_dialog_class.return_value = MagicMock()
            audio_model.stop_record(filename="")

        mock_reset.assert_called_once()

    def test_internal_dialog_called_when_threads_are_none(self, audio_model: AudioModel) -> None:
        with (
            patch("src.models.audio_model.InternalDialogError") as mock_dialog_class,
            patch("src.models.audio_model.pyaudio.PyAudio"),
            patch.object(audio_model, "_reset_state"),
        ):
            mock_dialog_class.return_value = MagicMock()
            audio_model.stop_record(filename="test_file")

        mock_dialog_class.assert_called_once_with(message=MESSAGE_ERROR_AUDIO_NOT_STARTED)
        mock_dialog_class.return_value.dialog.assert_called_once()

    def test_end_audio_is_set_to_true_when_threads_exist(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream

        with (
            patch("wave.open"),
            patch("src.models.audio_model.pyaudio.PyAudio"),
            patch.object(audio_model, "_reset_state"),
        ):
            audio_model.stop_record(filename="test_file")

        assert audio_model.end_audio is True

    def test_stream_stopped_and_closed_when_threads_exist(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream

        with (
            patch("wave.open"),
            patch("src.models.audio_model.pyaudio.PyAudio"),
            patch.object(audio_model, "_reset_state"),
        ):
            audio_model.stop_record(filename="test_file")

        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()

    def test_wav_file_saved_with_correct_name(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream

        with (
            patch("wave.open") as mock_wave_open,
            patch("src.models.audio_model.pyaudio.PyAudio"),
            patch.object(audio_model, "_reset_state"),
        ):
            mock_wave_file: MagicMock = MagicMock()
            mock_wave_open.return_value = mock_wave_file
            audio_model.stop_record(filename="my_recording")

        mock_wave_open.assert_called_once_with("my_recording.wav", "wb")

    def test_reset_state_called_after_saving(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream

        with (
            patch("wave.open"),
            patch("src.models.audio_model.pyaudio.PyAudio"),
            patch.object(audio_model, "_reset_state") as mock_reset,
        ):
            audio_model.stop_record(filename="test_file")

        mock_reset.assert_called_once()

    def test_threads_joined_when_they_exist(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream

        with (
            patch("wave.open"),
            patch("src.models.audio_model.pyaudio.PyAudio"),
            patch.object(audio_model, "_reset_state"),
        ):
            audio_model.stop_record(filename="test_file")

        assert mock_thread.join.call_count == 2


class TestAudioModelResetState:
    def test_seconds_reset_to_zero(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__seconds = 30

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.seconds == 0

    def test_minutes_reset_to_zero(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__minutes = 5

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.minutes == 0

    def test_frames_reset_to_empty_list(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__frames = [b"data"]

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.frames == []

    def test_end_audio_reset_to_false(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__end_audio = True

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.end_audio is False

    def test_stream_reset_to_none(self, audio_model: AudioModel) -> None:
        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.stream is None

    def test_recording_thread_reset_to_none(self, audio_model: AudioModel) -> None:
        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.recording_thread is None

    def test_timer_thread_reset_to_none(self, audio_model: AudioModel) -> None:
        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.timer_thread is None

    def test_stream_stopped_and_closed_when_present(self, audio_model: AudioModel) -> None:
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__stream = mock_stream

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()

    def test_threads_joined_when_present(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert mock_thread.join.call_count == 2

    def test_py_audio_reinitialised(self, audio_model: AudioModel) -> None:
        with patch("src.models.audio_model.pyaudio.PyAudio") as mock_pyaudio:
            audio_model._reset_state()

        mock_pyaudio.assert_called_once()


class TestAudioModelStr:
    def test_str_contains_chunk(self, audio_model: AudioModel) -> None:
        assert "1024" in str(audio_model)

    def test_str_contains_channels(self, audio_model: AudioModel) -> None:
        assert "1" in str(audio_model)

    def test_str_contains_fs(self, audio_model: AudioModel) -> None:
        assert "44100" in str(audio_model)

    def test_str_returns_string(self, audio_model: AudioModel) -> None:
        assert isinstance(str(audio_model), str)
