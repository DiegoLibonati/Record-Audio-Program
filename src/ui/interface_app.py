from tkinter import PhotoImage, Tk

from src.configs.default_config import DefaultConfig
from src.constants.paths import PATH_MIC, PATH_MIC_ON
from src.models.audio_model import AudioModel
from src.ui.styles import Styles
from src.ui.views.main_view import MainView


class InterfaceApp:
    def __init__(self, root: Tk, audio: AudioModel, config: DefaultConfig, styles: Styles = Styles()) -> None:
        self._styles = styles
        self._config = config
        self._root = root
        self._root.title("Record Program")
        self._root.geometry("400x400")
        self._root.resizable(False, False)
        self._root.config(background=self._styles.PRIMARY_COLOR)

        self._img_record_off = PhotoImage(file=PATH_MIC, master=self._root)
        self._img_record_on = PhotoImage(file=PATH_MIC_ON, master=self._root)

        self.__audio = audio

        self._main_view = MainView(
            root=self._root,
            styles=self._styles,
            img_record_off=self._img_record_off,
            img_record_on=self._img_record_on,
            on_start=self._perform_start_record,
            on_stop=self._perform_stop_record,
        )
        self._main_view.grid(row=0, column=0, sticky="nsew")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

    @property
    def audio(self) -> AudioModel:
        return self.__audio

    def _perform_start_record(self) -> None:
        filename = self._main_view.get_filename()

        if not filename:
            self._main_view.set_status("You must enter a valid filename.")
            return

        self._main_view.set_recording_state(recording=True)
        self.audio.start_record()
        self._set_timer()

    def _perform_stop_record(self) -> None:
        filename = self._main_view.get_filename()

        self._main_view.set_recording_state(recording=False)
        self._main_view.set_status(f"Finished in: {self._parse_timer(seconds=self.audio.seconds, minutes=self.audio.minutes)}. {filename} saved.")

        self.audio.stop_record(filename=filename)
        self._main_view.set_filename("Insert a new one!.")

    def _set_timer(self) -> None:
        if not self.audio.end_audio and self._main_view.is_recording():
            self._main_view.set_status(self._parse_timer(seconds=self.audio.seconds, minutes=self.audio.minutes))
            self._root.after(1000, self._set_timer)

    @staticmethod
    def _parse_timer(seconds: int, minutes: int) -> str:
        if seconds < 10 and minutes < 10:
            return f"0{minutes}:0{seconds}"

        if seconds < 10 and minutes >= 10:
            return f"{minutes}:0{seconds}"

        if seconds >= 10 and minutes < 10:
            return f"0{minutes}:{seconds}"

        return f"{minutes}:{seconds}"
