from tkinter import PhotoImage, StringVar
from unittest.mock import MagicMock

import pytest

from src.ui.styles import Styles


@pytest.fixture
def mock_root() -> MagicMock:
    root: MagicMock = MagicMock()
    root.title = MagicMock()
    root.geometry = MagicMock()
    root.resizable = MagicMock()
    root.config = MagicMock()
    root.columnconfigure = MagicMock()
    root.rowconfigure = MagicMock()
    root.after = MagicMock()
    return root


@pytest.fixture
def mock_styles() -> MagicMock:
    styles: MagicMock = MagicMock()
    styles.PRIMARY_COLOR = "#0099FF"
    styles.SECONDARY_COLOR = "#E43A3A"
    styles.WHITE_COLOR = "#FFFFFF"
    styles.BLACK_COLOR = "#000000"
    styles.FONT_ROBOTO_12 = "Roboto 12"
    styles.FONT_ROBOTO_15 = "Roboto 15"
    return styles


@pytest.fixture
def real_styles() -> Styles:
    return Styles()


@pytest.fixture
def mock_on_start() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_on_stop() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_img() -> MagicMock:
    return MagicMock(spec=PhotoImage)


@pytest.fixture
def variable() -> MagicMock:
    return MagicMock(spec=StringVar)


@pytest.fixture
def mock_audio() -> MagicMock:
    audio: MagicMock = MagicMock()
    audio.seconds = 0
    audio.minutes = 0
    audio.end_audio = False
    return audio
