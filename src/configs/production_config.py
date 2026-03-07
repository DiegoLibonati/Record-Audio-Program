from src.configs.default_config import DefaultConfig


class ProductionConfig(DefaultConfig):
    def __init__(self) -> None:
        super().__init__()
        self.DEBUG = False
        self.ENV = "production"
