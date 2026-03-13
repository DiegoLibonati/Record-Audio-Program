import types
from unittest.mock import MagicMock, patch

from src.utils.dialogs import (
    BaseDialog,
    NotFoundDialogError,
    ValidationDialogError,
)
from src.utils.error_handler import error_handler


class TestHandleError:
    def test_calls_open_when_exc_is_base_dialog(self) -> None:
        exc: ValidationDialogError = ValidationDialogError(message="validation failed")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            error_handler(type(exc), exc, MagicMock(spec=types.TracebackType))
        mock_handler.assert_called_once()

    def test_calls_open_on_not_found_dialog(self) -> None:
        exc: NotFoundDialogError = NotFoundDialogError(message="not found")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            error_handler(type(exc), exc, MagicMock(spec=types.TracebackType))
        mock_handler.assert_called_once()

    def test_opens_internal_dialog_for_non_base_dialog_exception(self) -> None:
        exc: ValueError = ValueError("unexpected error")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            error_handler(type(exc), exc, MagicMock(spec=types.TracebackType))
        mock_handler.assert_called_once()

    def test_internal_dialog_message_is_exception_str(self) -> None:
        exc: RuntimeError = RuntimeError("something broke")
        with patch("src.utils.error_handler.InternalDialogError") as mock_internal_class:
            mock_internal: MagicMock = MagicMock()
            mock_internal_class.return_value = mock_internal
            error_handler(type(exc), exc, MagicMock(spec=types.TracebackType))

        mock_internal_class.assert_called_once_with(message="something broke")
        mock_internal.open.assert_called_once()

    def test_does_not_raise_for_base_dialog_exc(self) -> None:
        exc: ValidationDialogError = ValidationDialogError(message="err")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            error_handler(type(exc), exc, MagicMock(spec=types.TracebackType))

    def test_does_not_raise_for_unknown_exception(self) -> None:
        exc: Exception = Exception("generic")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            error_handler(type(exc), exc, MagicMock(spec=types.TracebackType))

    def test_returns_none(self) -> None:
        exc: ValidationDialogError = ValidationDialogError(message="err")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            result = error_handler(type(exc), exc, MagicMock(spec=types.TracebackType))
        assert result is None
