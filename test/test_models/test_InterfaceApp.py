import os
import logging
import time
from tkinter import NORMAL
from tkinter import DISABLED

from src.models.Audio import Audio
from src.models.InterfaceApp import InterfaceApp
from src.utils.constants import PRIMARY


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CUSTOM_BG = "" or PRIMARY
AUDIO_NAMES = ["test_call_perform_start_record", "test_call_perform_stop_record", "test_set_timer"]


def test_initial_config_tk_app(interface_app: InterfaceApp) -> None:
    root = interface_app.root
    root.update()

    title = root.title()
    geometry = root.geometry().split("+")[0]
    resizable = root.resizable()
    config_bg = root.cget("bg")

    audio = interface_app.audio

    assert title == "Record Audio APP"
    assert geometry == "400x400"
    assert resizable == (False, False)
    assert config_bg == CUSTOM_BG

    assert audio
    assert isinstance(audio, Audio)

def test_call_perform_start_record(interface_app: InterfaceApp) -> None:
    interface_app._perform_start_record()

    assert interface_app.stop_button["state"] == NORMAL
    assert interface_app.start_button["state"] == DISABLED

    interface_app.audio.stop_record(filename="test_call_perform_start_record")

    interface_app.root.destroy()

def test_call_perform_stop_record(interface_app: InterfaceApp) -> None:
    interface_app._perform_start_record()

    assert interface_app.stop_button["state"] == NORMAL
    assert interface_app.start_button["state"] == DISABLED

    filename = "test_call_perform_stop_record"
    interface_app.filename.set(filename)
    interface_app._perform_stop_record()

    assert interface_app.stop_button["state"] == DISABLED
    assert interface_app.start_button["state"] == NORMAL
    assert interface_app.crono_label["text"] == f"Finished in: 00:00. {filename} saved."
    assert interface_app.filename.get() == "Insert a new one!."

    interface_app.root.destroy()

def test_set_timer(interface_app: InterfaceApp) -> None:
    interface_app._perform_start_record()

    assert interface_app.crono_label["text"] == "00:00"

    interface_app.filename.set("test_set_timer")
    interface_app._perform_stop_record()
    interface_app.root.destroy()

def test_parse_timer(interface_app: InterfaceApp) -> None:
    time = interface_app._parse_timer(seconds=1, minutes=2)

    assert time == "02:01"

    time = interface_app._parse_timer(seconds=10, minutes=2)

    assert time == "02:10"

    time = interface_app._parse_timer(seconds=2, minutes=10)

    assert time == "10:02"

    time = interface_app._parse_timer(seconds=20, minutes=10)

    assert time == "10:20"

def test_remove_audios() -> None:
    for audio_name in AUDIO_NAMES:
        audio_folder = os.getcwd()
        audio_name = f"{audio_name}.wav"
        
        file = os.path.join(audio_folder, audio_name)
        os.remove(path=file)

        assert not audio_name in os.listdir(os.getcwd())