from tkinter import Frame, Label, PhotoImage, StringVar, Tk

from src.ui.components.record_controls import RecordControls
from src.ui.styles import Styles


class MainView(Frame):
    def __init__(
        self,
        root: Tk,
        styles: Styles,
        img_record_off: PhotoImage,
        img_record_on: PhotoImage,
        on_start: callable,
        on_stop: callable,
    ) -> None:
        super().__init__(root, bg=styles.PRIMARY_COLOR)
        self._styles = styles
        self._img_record_off = img_record_off
        self._img_record_on = img_record_on
        self._on_start = on_start
        self._on_stop = on_stop

        self._status_text = StringVar(value="Starts")

        self._create_widgets()

    def _create_widgets(self) -> None:
        self.columnconfigure(0, weight=1)

        self._label_image = Label(
            self,
            image=self._img_record_off,
            border=0,
            bg=self._styles.PRIMARY_COLOR,
        )
        self._label_image.grid(row=0, column=0, pady=(40, 10))

        self._record_controls = RecordControls(
            parent=self,
            styles=self._styles,
            on_start=self._on_start,
            on_stop=self._on_stop,
        )
        self._record_controls.grid(row=1, column=0, pady=10)

        Label(
            self,
            width=25,
            bg=self._styles.PRIMARY_COLOR,
            fg=self._styles.WHITE_COLOR,
            font=self._styles.FONT_ROBOTO_12,
            textvariable=self._status_text,
        ).grid(row=2, column=0, pady=10)

    def get_filename(self) -> str:
        return self._record_controls.get_filename()

    def set_filename(self, value: str) -> None:
        self._record_controls.set_filename(value)

    def set_status(self, text: str) -> None:
        self._status_text.set(text)

    def set_recording_state(self, recording: bool) -> None:
        self._label_image.config(image=self._img_record_on if recording else self._img_record_off)
        self._record_controls.set_recording_state(recording=recording)

    def is_recording(self) -> bool:
        return self._record_controls.is_recording()
