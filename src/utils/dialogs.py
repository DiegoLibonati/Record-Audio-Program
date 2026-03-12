from tkinter import messagebox
from typing import Any

from src.constants.messages import MESSAGE_ERROR_APP, MESSAGE_NOT_FOUND_DIALOG_TYPE


class BaseDialog:
    ERROR = "Error"
    WARNING = "Warning"
    INFO = "Info"

    _TITLES = {
        ERROR: "Error",
        WARNING: "Warning",
        INFO: "Information",
    }

    _HANDLERS = {
        ERROR: messagebox.showerror,
        WARNING: messagebox.showwarning,
        INFO: messagebox.showinfo,
    }

    dialog_type: str = ERROR
    message: str = MESSAGE_ERROR_APP

    def __init__(self, message: str | None = None):
        if message is not None:
            self.message = message

    @property
    def title(self) -> str:
        return self._TITLES.get(self.dialog_type, self._TITLES[self.ERROR])

    def to_dict(self) -> dict[str, Any]:
        return {
            "dialog_type": self.dialog_type,
            "title": self.title,
            "message": self.message,
        }

    def dialog(self):
        handler = self._HANDLERS.get(self.dialog_type)
        if handler is None:
            messagebox.showerror(self.ERROR, MESSAGE_NOT_FOUND_DIALOG_TYPE)
            return None
        return handler(self.title, self.message)


class ValidationDialogError(BaseDialog):
    dialog_type = BaseDialog.ERROR
    message = "Validation error"


class AuthenticationDialogError(BaseDialog):
    dialog_type = BaseDialog.ERROR
    message = "Authentication error"


class NotFoundDialogError(BaseDialog):
    dialog_type = BaseDialog.ERROR
    message = "Resource not found"


class ConflictDialogError(BaseDialog):
    dialog_type = BaseDialog.ERROR
    message = "Conflict error"


class BusinessDialogError(BaseDialog):
    dialog_type = BaseDialog.ERROR
    message = "Business rule violated"


class InternalDialogError(BaseDialog):
    dialog_type = BaseDialog.ERROR
    message = "Internal error"


class DeprecatedDialogWarning(BaseDialog):
    dialog_type = BaseDialog.WARNING
    message = "This feature is deprecated"


class SuccessDialogInformation(BaseDialog):
    dialog_type = BaseDialog.INFO
    message = "Operation completed successfully"
