from test.constants import CHANNELS, CHUNK, FS, SAMPLE_FORMAT
from tkinter import Tk

from pytest import fixture

from src.models.audio import Audio
from src.ui.interface_app import InterfaceApp


@fixture
def audio() -> Audio:
    return Audio(chunk=CHUNK, sample_format=SAMPLE_FORMAT, channels=CHANNELS, fs=FS)


@fixture
def interface_app(audio: Audio) -> InterfaceApp:
    root = Tk()

    return InterfaceApp(root=root, audio=audio)
