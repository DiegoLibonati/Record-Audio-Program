from unittest.mock import MagicMock, patch

import pytest

from src.models.audio_model import AudioModel


@pytest.fixture
def audio_model() -> AudioModel:
    with patch("src.models.audio_model.pyaudio.PyAudio"):
        model: AudioModel = AudioModel(chunk=1024, sample_format=16, channels=1, fs=44100)
        return model


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

        with patch.object(audio_model, "_add_frame"), patch.object(audio_model, "_run_timer"):
            with patch("threading.Thread") as mock_thread:
                mock_thread.return_value.start = MagicMock()
                audio_model.start_record()

        audio_model._AudioModel__py_audio.open.assert_called_once_with(
            format=audio_model.sample_format,
            channels=audio_model.channels,
            rate=audio_model.fs,
            frames_per_buffer=audio_model.chunk,
            input=True,
        )

    def test_recording_thread_is_created(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__py_audio.open.return_value = MagicMock()

        with patch("threading.Thread") as mock_thread:
            mock_thread.return_value.start = MagicMock()
            audio_model.start_record()

        assert audio_model.recording_thread is not None

    def test_timer_thread_is_created(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__py_audio.open.return_value = MagicMock()

        with patch("threading.Thread") as mock_thread:
            mock_thread.return_value.start = MagicMock()
            audio_model.start_record()

        assert audio_model.timer_thread is not None

    def test_both_threads_are_started(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__py_audio.open.return_value = MagicMock()

        mock_thread_instance: MagicMock = MagicMock()
        with patch("threading.Thread", return_value=mock_thread_instance):
            audio_model.start_record()

        assert mock_thread_instance.start.call_count == 2


class TestAudioModelStopRecord:
    def test_raises_value_error_when_filename_is_empty(self, audio_model: AudioModel) -> None:
        with pytest.raises(ValueError, match="valid name"):
            audio_model.stop_record(filename="")

    def test_raises_value_error_when_filename_is_whitespace(self, audio_model: AudioModel) -> None:
        with pytest.raises(ValueError, match="valid name"):
            audio_model.stop_record(filename="   ")

    def test_raises_runtime_error_when_threads_are_none(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None

        with pytest.raises(RuntimeError, match="start an audio"):
            audio_model.stop_record(filename="test_file")

    def test_end_audio_is_set_to_true_before_joining(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()

        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream

        with (
            patch("wave.open") as mock_wave,
            patch.object(audio_model, "_reset_state"),
        ):
            mock_wave.return_value.__enter__ = MagicMock(return_value=mock_wave.return_value)
            mock_wave.return_value.__exit__ = MagicMock(return_value=False)
            audio_model.stop_record(filename="test_file")

        assert audio_model.end_audio is True

    def test_stream_is_stopped_and_closed(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()

        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream

        with (
            patch("wave.open") as mock_wave,
            patch.object(audio_model, "_reset_state"),
        ):
            mock_wave.return_value.__enter__ = MagicMock(return_value=mock_wave.return_value)
            mock_wave.return_value.__exit__ = MagicMock(return_value=False)
            audio_model.stop_record(filename="test_file")

        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()

    def test_wav_file_is_saved_with_correct_name(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()

        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream

        with (
            patch("wave.open") as mock_wave_open,
            patch.object(audio_model, "_reset_state"),
        ):
            mock_wave_file: MagicMock = MagicMock()
            mock_wave_open.return_value = mock_wave_file
            audio_model.stop_record(filename="my_recording")

        mock_wave_open.assert_called_once_with("my_recording.wav", "wb")

    def test_reset_state_is_called_after_saving(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()

        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream

        with (
            patch("wave.open") as mock_wave,
            patch.object(audio_model, "_reset_state") as mock_reset,
        ):
            mock_wave.return_value.__enter__ = MagicMock(return_value=mock_wave.return_value)
            mock_wave.return_value.__exit__ = MagicMock(return_value=False)
            audio_model.stop_record(filename="test_file")

        mock_reset.assert_called_once()


class TestAudioModelResetState:
    def test_seconds_reset_to_zero(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__seconds = 30
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None
        audio_model._AudioModel__stream = None

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.seconds == 0

    def test_minutes_reset_to_zero(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__minutes = 5
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None
        audio_model._AudioModel__stream = None

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.minutes == 0

    def test_frames_reset_to_empty_list(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__frames = [b"data"]
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None
        audio_model._AudioModel__stream = None

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.frames == []

    def test_end_audio_reset_to_false(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__end_audio = True
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None
        audio_model._AudioModel__stream = None

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.end_audio is False

    def test_stream_reset_to_none(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None
        audio_model._AudioModel__stream = None

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.stream is None

    def test_recording_thread_reset_to_none(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None
        audio_model._AudioModel__stream = None

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.recording_thread is None

    def test_timer_thread_reset_to_none(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None
        audio_model._AudioModel__stream = None

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert audio_model.timer_thread is None

    def test_stream_is_stopped_and_closed_when_present(self, audio_model: AudioModel) -> None:
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__stream = mock_stream
        audio_model._AudioModel__recording_thread = None
        audio_model._AudioModel__timer_thread = None

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()

    def test_threads_are_joined_when_present(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = None

        with patch("src.models.audio_model.pyaudio.PyAudio"):
            audio_model._reset_state()

        assert mock_thread.join.call_count == 2


class TestAudioModelStrMethod:
    def test_str_contains_chunk(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert "1024" in result

    def test_str_contains_channels(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert "1" in result

    def test_str_contains_fs(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert "44100" in result

    def test_str_returns_string(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert isinstance(result, str)
