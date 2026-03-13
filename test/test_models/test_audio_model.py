import threading
from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_ERROR_AUDIO_NOT_STARTED, MESSAGE_NOT_VALID_FILENAME_SAVE
from src.models.audio_model import AudioModel
from src.utils.dialogs import InternalDialogError, ValidationDialogError


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
    def test_stream_is_opened(self, audio_model: AudioModel) -> None:
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__py_audio.open.return_value = mock_stream

        with patch.object(threading.Thread, "start"):
            audio_model.start_record()

        audio_model._AudioModel__py_audio.open.assert_called_once_with(
            format=16,
            channels=1,
            rate=44100,
            frames_per_buffer=1024,
            input=True,
        )

    def test_stream_is_assigned(self, audio_model: AudioModel) -> None:
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__py_audio.open.return_value = mock_stream

        with patch.object(threading.Thread, "start"):
            audio_model.start_record()

        assert audio_model.stream is mock_stream

    def test_recording_thread_is_created(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__py_audio.open.return_value = MagicMock()

        with patch.object(threading.Thread, "start"):
            audio_model.start_record()

        assert audio_model.recording_thread is not None

    def test_timer_thread_is_created(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__py_audio.open.return_value = MagicMock()

        with patch.object(threading.Thread, "start"):
            audio_model.start_record()

        assert audio_model.timer_thread is not None

    def test_both_threads_are_started(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__py_audio.open.return_value = MagicMock()

        with patch("threading.Thread") as mock_thread_class:
            mock_thread: MagicMock = MagicMock()
            mock_thread_class.return_value = mock_thread
            audio_model.start_record()

        assert mock_thread.start.call_count == 2


class TestAudioModelStopRecord:
    def test_raises_validation_error_when_filename_is_empty(self, audio_model: AudioModel) -> None:
        with (
            patch.object(audio_model, "_reset_state"),
            pytest.raises(ValidationDialogError) as exc_info,
        ):
            audio_model.stop_record(filename="")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FILENAME_SAVE

    def test_raises_validation_error_when_filename_is_whitespace(self, audio_model: AudioModel) -> None:
        with (
            patch.object(audio_model, "_reset_state"),
            pytest.raises(ValidationDialogError) as exc_info,
        ):
            audio_model.stop_record(filename="   ")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FILENAME_SAVE

    def test_reset_state_called_when_filename_is_empty(self, audio_model: AudioModel) -> None:
        with (
            patch.object(audio_model, "_reset_state") as mock_reset,
            pytest.raises(ValidationDialogError),
        ):
            audio_model.stop_record(filename="")
        mock_reset.assert_called_once()

    def test_raises_internal_error_when_threads_are_none(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None

        with (
            patch.object(audio_model, "_reset_state"),
            pytest.raises(InternalDialogError) as exc_info,
        ):
            audio_model.stop_record(filename="recording")
        assert exc_info.value.message == MESSAGE_ERROR_AUDIO_NOT_STARTED

    def test_reset_state_called_when_threads_are_none(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None

        with (
            patch.object(audio_model, "_reset_state") as mock_reset,
            pytest.raises(InternalDialogError),
        ):
            audio_model.stop_record(filename="recording")
        mock_reset.assert_called()

    def test_returns_true_on_success(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock(spec=threading.Thread)
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = MagicMock()

        with (
            patch("wave.open") as mock_wave,
            patch.object(audio_model, "_reset_state"),
        ):
            mock_wave.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_wave.return_value.__exit__ = MagicMock(return_value=False)
            result: bool = audio_model.stop_record(filename="recording")

        assert result is True

    def test_stream_is_stopped_and_closed(self, audio_model: AudioModel) -> None:
        mock_stream: MagicMock = MagicMock()
        mock_thread: MagicMock = MagicMock(spec=threading.Thread)
        audio_model._AudioModel__stream = mock_stream
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread

        with (
            patch("wave.open"),
            patch.object(audio_model, "_reset_state"),
        ):
            audio_model.stop_record(filename="recording")

        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()

    def test_py_audio_is_terminated(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock(spec=threading.Thread)
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = MagicMock()

        with (
            patch("wave.open"),
            patch.object(audio_model, "_reset_state"),
        ):
            audio_model.stop_record(filename="recording")

        audio_model._AudioModel__py_audio.terminate.assert_called_once()

    def test_wave_file_written_with_correct_filename(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock(spec=threading.Thread)
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = MagicMock()

        with (
            patch("wave.open") as mock_wave_open,
            patch.object(audio_model, "_reset_state"),
        ):
            mock_wave_obj: MagicMock = MagicMock()
            mock_wave_open.return_value = mock_wave_obj
            audio_model.stop_record(filename="my_recording")

        mock_wave_open.assert_called_once_with("my_recording.wav", "wb")

    def test_end_audio_is_set_to_true(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock(spec=threading.Thread)
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = MagicMock()

        with (
            patch("wave.open"),
            patch.object(audio_model, "_reset_state"),
        ):
            audio_model.stop_record(filename="recording")

        assert audio_model._AudioModel__end_audio is True


class TestAudioModelResetState:
    def test_seconds_reset_to_zero(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__seconds = 45

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.seconds == 0

    def test_minutes_reset_to_zero(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__minutes = 3

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.minutes == 0

    def test_stream_reset_to_none(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__stream = MagicMock()

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.stream is None

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

    def test_recording_thread_reset_to_none(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__recording_thread = MagicMock()

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.recording_thread is None

    def test_timer_thread_reset_to_none(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__timer_thread = MagicMock()

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.timer_thread is None

    def test_stream_is_stopped_and_closed_if_set(self, audio_model: AudioModel) -> None:
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__stream = mock_stream

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()

    def test_py_audio_terminated_if_set(self, audio_model: AudioModel) -> None:
        mock_py_audio: MagicMock = MagicMock()
        audio_model._AudioModel__py_audio = mock_py_audio

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        mock_py_audio.terminate.assert_called_once()

    def test_threads_are_joined_if_set(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock(spec=threading.Thread)
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert mock_thread.join.call_count == 2
