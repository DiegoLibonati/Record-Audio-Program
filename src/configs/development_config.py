from src.configs.default_config import DefaultConfig


class DevelopmentConfig(DefaultConfig):
    def __init__(self) -> None:
        super().__init__()
        self.DEBUG = True
        self.ENV = "development"
