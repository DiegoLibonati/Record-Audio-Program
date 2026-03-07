from src.configs.default_config import DefaultConfig


class TestingConfig(DefaultConfig):
    def __init__(self) -> None:
        super().__init__()
        self.TESTING = True
        self.DEBUG = True
        self.ENV = "testing"
