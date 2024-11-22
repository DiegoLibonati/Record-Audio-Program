from tkinter import Tk
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import PhotoImage
from tkinter import NORMAL
from tkinter import CENTER
from tkinter import DISABLED

from src.models.Audio import Audio
from src.utils.constants import WHITE
from src.utils.constants import PRIMARY
from src.utils.constants import SECONDARY
from src.utils.constants import ROBOTO_12
from src.utils.constants import ROBOTO_15


class InterfaceApp:
    def __init__(self, root: Tk, audio: Audio, bg: str = PRIMARY) -> None:
        self.root = root
        self.root.title("Record Audio APP")
        self.root.geometry('400x400')
        self.root.resizable(False, False)
        self.root.config(bg=bg)

        self.img_record_off = PhotoImage(file="./src/assets/mic.png", master=self.root)
        self.img_record_on = PhotoImage(file="./src/assets/micon.png", master=self.root)

        self.__audio = audio

        self._create_widgets()

    @property
    def audio(self) -> Audio:
        return self.__audio 
        
    def _create_widgets(self) -> None:
        self.filename = StringVar()

        self.label_image = Label(self.root, image=self.img_record_off, border = 0)
        self.label_image.place(x=200, y = 100, anchor=CENTER)

        self.entry_name_audio = Entry(width = 15, font=(ROBOTO_15), textvariable=self.filename)
        self.entry_name_audio.place(x = 200, y = 200, anchor=CENTER)

        self.start_button = Button(self.root, width=15, text="Start Record", font=(ROBOTO_15), bg=SECONDARY, fg=WHITE, border=0, command=lambda:self._perform_start_record(), state=NORMAL)
        self.start_button.place(x = 200, y = 250, anchor=CENTER)

        self.stop_button = Button(self.root, width=15, text="Stop Record", font=(ROBOTO_15), bg=SECONDARY, fg=WHITE, border=0, state=DISABLED, command=lambda:self._perform_stop_record())
        self.stop_button.place(x = 200, y = 300, anchor=CENTER)

        self.crono_label = Label(self.root, width = 25, bg=PRIMARY, fg=WHITE, font=(ROBOTO_12))
        self.crono_label.place(x = 200, y = 350, anchor=CENTER)
        self.crono_label.config(text="Starts")


    def _perform_start_record(self) -> None:
        self.stop_button['state'] = NORMAL 
        self.start_button['state'] = DISABLED 
        self.label_image['image'] = self.img_record_on

        self.audio.start_record()
        self._set_timer()


    def _perform_stop_record(self) -> None:
        filename = self.filename.get()

        self.stop_button['state'] = DISABLED
        self.start_button['state'] = NORMAL 
        self.label_image['image'] = self.img_record_off
        self.crono_label["text"] = f"Finished in: {self._parse_timer(seconds=self.audio.seconds, minutes=self.audio.minutes)}. {filename} saved."

        self.audio.stop_record(filename=filename)

        self.filename.set("Insert a new one!.")


    def _set_timer(self) -> None:
        if not self.audio.end_audio and self.stop_button['state'] == NORMAL:
            self.crono_label["text"] = self._parse_timer(seconds=self.audio.seconds, minutes=self.audio.minutes)
            self.root.after(1000, self._set_timer)


    @staticmethod
    def _parse_timer(seconds: int, minutes: int) -> str:
        if seconds < 10 and minutes < 10:
            return f"0{minutes}:0{seconds}"
        
        if seconds < 10 and minutes >= 10:
            return f"{minutes}:0{seconds}"
        
        if seconds >= 10 and minutes < 10:
            return f"0{minutes}:{seconds}"
       
        return f"{minutes}:{seconds}"