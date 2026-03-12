from unittest.mock import MagicMock, patch

from src.constants.messages import MESSAGE_ERROR_APP, MESSAGE_NOT_FOUND_DIALOG_TYPE
from src.utils.dialogs import (
    AuthenticationDialogError,
    BaseDialog,
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
        dialog: BaseDialog = BaseDialog()
        assert dialog.dialog_type == BaseDialog.ERROR


class TestBaseDialogTitleProperty:
    def test_title_for_error_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        dialog.dialog_type = BaseDialog.ERROR
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
        dialog: BaseDialog = BaseDialog()
        assert isinstance(dialog.to_dict(), dict)

    def test_dict_contains_dialog_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert "dialog_type" in dialog.to_dict()

    def test_dict_contains_title(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert "title" in dialog.to_dict()

    def test_dict_contains_message(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert "message" in dialog.to_dict()

    def test_dict_dialog_type_value(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.to_dict()["dialog_type"] == BaseDialog.ERROR

    def test_dict_title_value(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.to_dict()["title"] == "Error"

    def test_dict_message_value(self) -> None:
        dialog: BaseDialog = BaseDialog(message="test msg")
        assert dialog.to_dict()["message"] == "test msg"


class TestBaseDialogDialog:
    def test_calls_showerror_for_error_type(self) -> None:
        dialog: BaseDialog = BaseDialog(message="something went wrong")
        with patch.object(BaseDialog._HANDLERS[BaseDialog.ERROR], "__call__", return_value=None) as mock_handler:
            with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
                dialog.dialog()
        mock_handler.assert_called_once_with("Error", "something went wrong")

    def test_calls_showwarning_for_warning_type(self) -> None:
        dialog: BaseDialog = BaseDialog(message="heads up")
        dialog.dialog_type = BaseDialog.WARNING
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.WARNING: mock_handler}):
            dialog.dialog()
        mock_handler.assert_called_once_with("Warning", "heads up")

    def test_calls_showinfo_for_info_type(self) -> None:
        dialog: BaseDialog = BaseDialog(message="all good")
        dialog.dialog_type = BaseDialog.INFO
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.INFO: mock_handler}):
            dialog.dialog()
        mock_handler.assert_called_once_with("Information", "all good")

    def test_calls_showerror_for_error_type_with_correct_message(self) -> None:
        dialog: BaseDialog = BaseDialog(message="something went wrong")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            dialog.dialog()
        mock_handler.assert_called_once_with("Error", "something went wrong")

    def test_calls_showerror_with_not_found_message_for_unknown_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        dialog.dialog_type = "unknown_type"
        with patch("src.utils.dialogs.messagebox.showerror") as mock_showerror:
            dialog.dialog()
        mock_showerror.assert_called_once_with(BaseDialog.ERROR, MESSAGE_NOT_FOUND_DIALOG_TYPE)

    def test_returns_none_for_unknown_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        dialog.dialog_type = "unknown_type"
        with patch("src.utils.dialogs.messagebox.showerror"):
            result = dialog.dialog()
        assert result is None


class TestValidationDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert ValidationDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(ValidationDialogError, BaseDialog)

    def test_custom_message_is_set(self) -> None:
        dialog: ValidationDialogError = ValidationDialogError(message="invalid input")
        assert dialog.message == "invalid input"

    def test_calls_showerror_on_dialog(self) -> None:
        dialog: ValidationDialogError = ValidationDialogError(message="invalid")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            dialog.dialog()
        mock_handler.assert_called_once()


class TestAuthenticationDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert AuthenticationDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(AuthenticationDialogError, BaseDialog)

    def test_custom_message_is_set(self) -> None:
        dialog: AuthenticationDialogError = AuthenticationDialogError(message="auth failed")
        assert dialog.message == "auth failed"


class TestNotFoundDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert NotFoundDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(NotFoundDialogError, BaseDialog)

    def test_custom_message_is_set(self) -> None:
        dialog: NotFoundDialogError = NotFoundDialogError(message="not found")
        assert dialog.message == "not found"


class TestConflictDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert ConflictDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(ConflictDialogError, BaseDialog)

    def test_custom_message_is_set(self) -> None:
        dialog: ConflictDialogError = ConflictDialogError(message="already exists")
        assert dialog.message == "already exists"


class TestBusinessDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert BusinessDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(BusinessDialogError, BaseDialog)

    def test_custom_message_is_set(self) -> None:
        dialog: BusinessDialogError = BusinessDialogError(message="rule violated")
        assert dialog.message == "rule violated"


class TestInternalDialogError:
    def test_dialog_type_is_error(self) -> None:
        assert InternalDialogError.dialog_type == BaseDialog.ERROR

    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(InternalDialogError, BaseDialog)

    def test_custom_message_is_set(self) -> None:
        dialog: InternalDialogError = InternalDialogError(message="internal failure")
        assert dialog.message == "internal failure"


class TestDeprecatedDialogWarning:
    def test_dialog_type_is_warning(self) -> None:
        assert DeprecatedDialogWarning.dialog_type == BaseDialog.WARNING

    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(DeprecatedDialogWarning, BaseDialog)

    def test_title_is_warning(self) -> None:
        dialog: DeprecatedDialogWarning = DeprecatedDialogWarning()
        assert dialog.title == "Warning"

    def test_calls_showwarning_on_dialog(self) -> None:
        dialog: DeprecatedDialogWarning = DeprecatedDialogWarning(message="deprecated")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.WARNING: mock_handler}):
            dialog.dialog()
        mock_handler.assert_called_once()


class TestSuccessDialogInformation:
    def test_dialog_type_is_info(self) -> None:
        assert SuccessDialogInformation.dialog_type == BaseDialog.INFO

    def test_inherits_from_base_dialog(self) -> None:
        assert issubclass(SuccessDialogInformation, BaseDialog)

    def test_title_is_information(self) -> None:
        dialog: SuccessDialogInformation = SuccessDialogInformation()
        assert dialog.title == "Information"

    def test_custom_message_is_set(self) -> None:
        dialog: SuccessDialogInformation = SuccessDialogInformation(message="done")
        assert dialog.message == "done"

    def test_calls_showinfo_on_dialog(self) -> None:
        dialog: SuccessDialogInformation = SuccessDialogInformation(message="success")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.INFO: mock_handler}):
            dialog.dialog()
        mock_handler.assert_called_once()
