from tkinter import Tk

from pyaudio import paInt16

from src.models.Audio import Audio
from src.models.InterfaceApp import InterfaceApp


def main():
    root = Tk()
    audio = Audio(chunk=1024, sample_format=paInt16, channels=1, fs=44100)
    app = InterfaceApp(root=root, audio=audio)

    root.mainloop()

    print(f"App: {app}")


if __name__ == "__main__":
    main()