from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_ERROR_APP, MESSAGE_NOT_FOUND_DIALOG_TYPE
from src.utils.dialogs import (
    AuthenticationDialogError,
    BaseDialog,
    BaseDialogError,
    BaseDialogNotification,
    BusinessDialogError,
    ConflictDialogError,
    DeprecatedDialogWarning,
    InternalDialogError,
    NotFoundDialogError,
    SuccessDialogInformation,
    ValidationDialogError,
)


class TestBaseDialogInit:
    def test_default_message_is_error_app(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.message == MESSAGE_ERROR_APP

    def test_custom_message_overrides_default(self) -> None:
        dialog: BaseDialog = BaseDialog(message="Custom error")
        assert dialog.message == "Custom error"

    def test_none_message_keeps_class_default(self) -> None:
        dialog: BaseDialog = BaseDialog(message=None)
        assert dialog.message == MESSAGE_ERROR_APP

    def test_default_dialog_type_is_error(self) -> None:
        assert BaseDialog.dialog_type == BaseDialog.ERROR

    def test_is_not_exception(self) -> None:
        assert not issubclass(BaseDialog, Exception)


class TestBaseDialogTitleProperty:
    def test_title_for_error_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.title == "Error"

    def test_title_for_warning_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        dialog.dialog_type = BaseDialog.WARNING
        assert dialog.title == "Warning"

    def test_title_for_info_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        dialog.dialog_type = BaseDialog.INFO
        assert dialog.title == "Information"

    def test_title_falls_back_to_error_for_unknown_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        dialog.dialog_type = "unknown"
        assert dialog.title == "Error"


class TestBaseDialogToDict:
    def test_returns_dict(self) -> None:
        assert isinstance(BaseDialog().to_dict(), dict)

    def test_dict_contains_dialog_type(self) -> None:
        assert "dialog_type" in BaseDialog().to_dict()

    def test_dict_contains_title(self) -> None:
        assert "title" in BaseDialog().to_dict()

    def test_dict_contains_message(self) -> None:
        assert "message" in BaseDialog().to_dict()

    def test_dict_dialog_type_value(self) -> None:
        assert BaseDialog().to_dict()["dialog_type"] == BaseDialog.ERROR

    def test_dict_title_value(self) -> None:
        assert BaseDialog().to_dict()["title"] == "Error"

    def test_dict_message_value(self) -> None:
        assert BaseDialog(message="test msg").to_dict()["message"] == "test msg"


class TestBaseDialogOpen:
    def test_calls_showerror_for_error_type(self) -> None:
        dialog: BaseDialog = BaseDialog(message="something went wrong")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            dialog.open()
        mock_handler.assert_called_once_with("Error", "something went wrong")

    def test_calls_showwarning_for_warning_type(self) -> None:
        dialog: BaseDialog = BaseDialog(message="heads up")
        dialog.dialog_type = BaseDialog.WARNING
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.WARNING: mock_handler}):
            dialog.open()
        mock_handler.assert_called_once_with("Warning", "heads up")

    def test_calls_showinfo_for_info_type(self) -> None:
        dialog: BaseDialog = BaseDialog(message="all good")
        dialog.dialog_type = BaseDialog.INFO
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.INFO: mock_handler}):
            dialog.open()
        mock_handler.assert_called_once_with("Information", "all good")

    def test_calls_showerror_with_not_found_message_for_unknown_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        dialog.dialog_type = "unknown_type"
        with patch("src.utils.dialogs.messagebox.showerror") as mock_showerror:
            dialog.open()
        mock_showerror.assert_called_once_with(BaseDialog.ERROR, MESSAGE_NOT_FOUND_DIALOG_TYPE)

    def test_returns_none_for_unknown_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        dialog.dialog_type = "unknown_type"
        with patch("src.utils.dialogs.messagebox.showerror"):
            result = dialog.open()
        assert result is None

    def test_returns_none_on_success(self) -> None:
        dialog: BaseDialog = BaseDialog(message="ok")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            result = dialog.open()
        assert result is None


class TestBaseDialogError:
    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(BaseDialogError, BaseDialog)

    def test_inherits_from_exception(self) -> None:
        assert issubclass(BaseDialogError, Exception)

    def test_dialog_type_is_error(self) -> None:
        assert BaseDialogError.dialog_type == BaseDialog.ERROR

    def test_default_message_is_error_app(self) -> None:
        assert BaseDialogError().message == MESSAGE_ERROR_APP

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(BaseDialogError):
            raise BaseDialogError(message="error raised")

    def test_can_be_caught_as_exception(self) -> None:
        with pytest.raises(Exception):
            raise BaseDialogError(message="caught as exception")


class TestBaseDialogNotification:
    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(BaseDialogNotification, BaseDialog)

    def test_is_not_exception(self) -> None:
        assert not issubclass(BaseDialogNotification, Exception)


class TestValidationDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert ValidationDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog_error(self) -> None:
        assert issubclass(ValidationDialogError, BaseDialogError)

    def test_is_exception(self) -> None:
        assert issubclass(ValidationDialogError, Exception)

    def test_custom_message_is_set(self) -> None:
        assert ValidationDialogError(message="invalid input").message == "invalid input"

    def test_can_be_raised_and_caught_as_base_dialog_error(self) -> None:
        with pytest.raises(BaseDialogError):
            raise ValidationDialogError(message="err")

    def test_calls_showerror_on_open(self) -> None:
        dialog: ValidationDialogError = ValidationDialogError(message="invalid")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            dialog.open()
        mock_handler.assert_called_once()


class TestAuthenticationDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert AuthenticationDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog_error(self) -> None:
        assert issubclass(AuthenticationDialogError, BaseDialogError)

    def test_is_exception(self) -> None:
        assert issubclass(AuthenticationDialogError, Exception)

    def test_custom_message_is_set(self) -> None:
        assert AuthenticationDialogError(message="auth failed").message == "auth failed"


class TestNotFoundDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert NotFoundDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog_error(self) -> None:
        assert issubclass(NotFoundDialogError, BaseDialogError)

    def test_is_exception(self) -> None:
        assert issubclass(NotFoundDialogError, Exception)

    def test_custom_message_is_set(self) -> None:
        assert NotFoundDialogError(message="not found").message == "not found"


class TestConflictDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert ConflictDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog_error(self) -> None:
        assert issubclass(ConflictDialogError, BaseDialogError)

    def test_is_exception(self) -> None:
        assert issubclass(ConflictDialogError, Exception)

    def test_custom_message_is_set(self) -> None:
        assert ConflictDialogError(message="already exists").message == "already exists"


class TestBusinessDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert BusinessDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog_error(self) -> None:
        assert issubclass(BusinessDialogError, BaseDialogError)

    def test_is_exception(self) -> None:
        assert issubclass(BusinessDialogError, Exception)

    def test_custom_message_is_set(self) -> None:
        assert BusinessDialogError(message="rule violated").message == "rule violated"


class TestInternalDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert InternalDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog_error(self) -> None:
        assert issubclass(InternalDialogError, BaseDialogError)

    def test_is_exception(self) -> None:
        assert issubclass(InternalDialogError, Exception)

    def test_custom_message_is_set(self) -> None:
        assert InternalDialogError(message="internal failure").message == "internal failure"


class TestDeprecatedDialogWarning:
    def test_dialog_type_is_warning(self) -> None:
        assert DeprecatedDialogWarning.dialog_type == BaseDialog.WARNING

    def test_inherits_from_base_dialog_notification(self) -> None:
        assert issubclass(DeprecatedDialogWarning, BaseDialogNotification)

    def test_is_not_exception(self) -> None:
        assert not issubclass(DeprecatedDialogWarning, Exception)

    def test_title_is_warning(self) -> None:
        assert DeprecatedDialogWarning().title == "Warning"

    def test_custom_message_is_set(self) -> None:
        assert DeprecatedDialogWarning(message="deprecated feature").message == "deprecated feature"

    def test_calls_showwarning_on_open(self) -> None:
        dialog: DeprecatedDialogWarning = DeprecatedDialogWarning(message="deprecated")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.WARNING: mock_handler}):
            dialog.open()
        mock_handler.assert_called_once()


class TestSuccessDialogInformation:
    def test_dialog_type_is_info(self) -> None:
        assert SuccessDialogInformation.dialog_type == BaseDialog.INFO

    def test_inherits_from_base_dialog_notification(self) -> None:
        assert issubclass(SuccessDialogInformation, BaseDialogNotification)

    def test_is_not_exception(self) -> None:
        assert not issubclass(SuccessDialogInformation, Exception)

    def test_title_is_information(self) -> None:
        assert SuccessDialogInformation().title == "Information"

    def test_custom_message_is_set(self) -> None:
        assert SuccessDialogInformation(message="done").message == "done"

    def test_calls_showinfo_on_open(self) -> None:
        dialog: SuccessDialogInformation = SuccessDialogInformation(message="success")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.INFO: mock_handler}):
            dialog.open()
        mock_handler.assert_called_once()
