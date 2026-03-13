# import traceback
import types

from src.utils.dialogs import BaseDialog, InternalDialogError


def error_handler(
    _exc_type: type[BaseException],
    exc_value: BaseException,
    _exc_tb: types.TracebackType,
) -> None:
    # error_detail: str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    # logger.error("Unhandled exception:\n%s", error_detail)

    if isinstance(exc_value, BaseDialog):
        exc_value.open()
    else:
        InternalDialogError(message=str(exc_value)).open()
