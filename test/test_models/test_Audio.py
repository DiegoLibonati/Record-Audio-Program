import logging
import os
import time
from test.constants import CHANNELS, CHUNK, FS, SAMPLE_FORMAT

import pyaudio
import pytest

from src.models.Audio import Audio

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


AUDIO_NAMES = [
    "test_add_frame_to_frames",
    "test_run_timer",
    "test_start_record",
    "test_stop_record",
]


def test_init_audio(audio: Audio) -> None:
    assert audio.chunk == CHUNK
    assert audio.sample_format == SAMPLE_FORMAT
    assert audio.channels == CHANNELS
    assert audio.fs == FS

    assert audio.seconds == 0
    assert audio.minutes == 0

    assert audio.stream is None
    assert isinstance(audio.py_audio, pyaudio.PyAudio)
    assert not audio.frames
    assert isinstance(audio.frames, list)

    assert isinstance(audio.end_audio, bool)
    assert not audio.end_audio
    assert not audio.recording_thread
    assert not audio.timer_thread


def test_start_record(audio: Audio) -> None:
    audio.start_record()

    assert audio.stream
    assert isinstance(audio.stream, pyaudio.Stream)
    assert audio.recording_thread.is_alive()
    assert audio.timer_thread.is_alive()

    audio.stop_record(filename="test_start_record")


def test_add_frame_to_frames(audio: Audio) -> None:
    audio.start_record()
    time.sleep(1)

    assert audio.frames

    for frame in audio.frames:
        assert frame
        assert isinstance(frame, bytes)

    audio.stop_record(filename="test_add_frame_to_frames")


def test_stop_record(audio: Audio) -> None:
    audio_name = "test_stop_record"

    audio.start_record()
    time.sleep(1)
    audio.stop_record(filename=audio_name)

    assert f"{audio_name}.wav" in os.listdir(os.getcwd())

    # Reseted
    assert audio.seconds == 0
    assert audio.minutes == 0
    assert audio.stream is None
    assert isinstance(audio.py_audio, pyaudio.PyAudio)
    assert not audio.frames
    assert isinstance(audio.frames, list)
    assert isinstance(audio.end_audio, bool)
    assert not audio.end_audio
    assert not audio.recording_thread
    assert not audio.timer_thread


def test_stop_record_not_filename(audio: Audio) -> None:
    with pytest.raises(ValueError) as exc_info:
        audio.stop_record(filename="  ")

    assert str(exc_info.value) == "You must enter a valid name to save the file."


def test_stop_record_not_started(audio: Audio) -> None:
    with pytest.raises(RuntimeError) as exc_info:
        audio.stop_record(filename="test_stop_record_not_started")

    assert str(exc_info.value) == "You must start an audio to be able to stop it."


def test_run_timer(audio: Audio) -> None:
    audio.start_record()
    time.sleep(2)

    assert audio.seconds == 1 or 2
    assert audio.minutes == 0

    audio.stop_record(filename="test_run_timer")


def test_reset_state(audio: Audio) -> None:
    audio._reset_state()

    assert audio.chunk == CHUNK
    assert audio.sample_format == SAMPLE_FORMAT
    assert audio.channels == CHANNELS
    assert audio.fs == FS

    assert audio.seconds == 0
    assert audio.minutes == 0

    assert audio.stream is None
    assert isinstance(audio.py_audio, pyaudio.PyAudio)
    assert not audio.frames
    assert isinstance(audio.frames, list)

    assert isinstance(audio.end_audio, bool)
    assert not audio.end_audio
    assert not audio.recording_thread
    assert not audio.timer_thread

    # Remove all audios
    for audio_name in AUDIO_NAMES:
        audio_folder = os.getcwd()
        audio_name = f"{audio_name}.wav"

        file = os.path.join(audio_folder, audio_name)
        os.remove(path=file)

        assert audio_name not in os.listdir(os.getcwd())
