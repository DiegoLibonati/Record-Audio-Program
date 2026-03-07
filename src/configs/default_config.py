import os


class DefaultConfig:
    def __init__(self) -> None:
        # General
        self.TZ = os.getenv("TZ", "America/Argentina/Buenos_Aires")
        self.DEBUG = False
        self.TESTING = False

        # App
        self.ENV_NAME = os.getenv("ENV_NAME", "template tkinter python")
