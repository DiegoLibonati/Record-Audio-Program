from tkinter import Tk

from pytest import fixture

from src.models.Audio import Audio
from src.models.InterfaceApp import InterfaceApp

from test.constants import CHUNK
from test.constants import SAMPLE_FORMAT
from test.constants import CHANNELS
from test.constants import FS

@fixture
def audio() -> Audio:
    return Audio(chunk=CHUNK, sample_format=SAMPLE_FORMAT, channels=CHANNELS, fs=FS)

@fixture
def interface_app(audio: Audio) -> InterfaceApp:
    root = Tk()

    return InterfaceApp(root=root, audio=audio)