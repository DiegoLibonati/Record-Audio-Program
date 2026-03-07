import logging

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-instance")
        assert isinstance(logger, logging.Logger)

    def test_logger_has_correct_name(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-name")
        assert logger.name == "test-logger-name"

    def test_logger_default_name(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "tkinter-app"

    def test_logger_level_is_debug(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-level")
        assert logger.level == logging.DEBUG

    def test_logger_has_handlers(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-handlers")
        assert len(logger.handlers) > 0

    def test_logger_handler_is_stream_handler(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-stream")
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)

    def test_calling_twice_does_not_duplicate_handlers(self) -> None:
        logger_name: str = "test-logger-no-duplicate"
        setup_logger(logger_name)
        logger: logging.Logger = setup_logger(logger_name)
        assert len(logger.handlers) == 1
