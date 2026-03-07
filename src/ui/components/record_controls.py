from tkinter import DISABLED, NORMAL, Button, Entry, Frame, Misc, StringVar

from src.ui.styles import Styles


class RecordControls(Frame):
    def __init__(
        self,
        parent: Misc,
        styles: Styles,
        on_start: callable,
        on_stop: callable,
    ) -> None:
        super().__init__(parent, bg=styles.PRIMARY_COLOR)
        self._styles = styles
        self._on_start = on_start
        self._on_stop = on_stop

        self._filename = StringVar()

        self.columnconfigure(0, weight=1)

        Entry(
            self,
            width=15,
            font=self._styles.FONT_ROBOTO_15,
            textvariable=self._filename,
        ).grid(row=0, column=0, pady=(0, 10))

        self._start_button = Button(
            self,
            width=15,
            text="Start Record",
            font=self._styles.FONT_ROBOTO_15,
            bg=self._styles.SECONDARY_COLOR,
            fg=self._styles.WHITE_COLOR,
            border=0,
            state=NORMAL,
            command=self._on_start,
        )
        self._start_button.grid(row=1, column=0, pady=5)

        self._stop_button = Button(
            self,
            width=15,
            text="Stop Record",
            font=self._styles.FONT_ROBOTO_15,
            bg=self._styles.SECONDARY_COLOR,
            fg=self._styles.WHITE_COLOR,
            border=0,
            state=DISABLED,
            command=self._on_stop,
        )
        self._stop_button.grid(row=2, column=0, pady=5)

    def get_filename(self) -> str:
        return self._filename.get()

    def set_filename(self, value: str) -> None:
        self._filename.set(value)

    def set_recording_state(self, recording: bool) -> None:
        self._start_button.config(state=DISABLED if recording else NORMAL)
        self._stop_button.config(state=NORMAL if recording else DISABLED)

    def is_recording(self) -> bool:
        return self._stop_button["state"] == NORMAL
