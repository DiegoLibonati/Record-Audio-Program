from src.constants.messages import (
    MESSAGE_ERROR_APP,
    MESSAGE_ERROR_AUDIO_NOT_STARTED,
    MESSAGE_NOT_FOUND_DIALOG_TYPE,
    MESSAGE_NOT_VALID_FILENAME,
    MESSAGE_NOT_VALID_FILENAME_SAVE,
)


class TestMessages:
    def test_error_app_is_string(self) -> None:
        assert isinstance(MESSAGE_ERROR_APP, str)

    def test_error_app_is_not_empty(self) -> None:
        assert len(MESSAGE_ERROR_APP) > 0

    def test_error_audio_not_started_is_string(self) -> None:
        assert isinstance(MESSAGE_ERROR_AUDIO_NOT_STARTED, str)

    def test_error_audio_not_started_is_not_empty(self) -> None:
        assert len(MESSAGE_ERROR_AUDIO_NOT_STARTED) > 0

    def test_not_valid_filename_save_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_VALID_FILENAME_SAVE, str)

    def test_not_valid_filename_save_is_not_empty(self) -> None:
        assert len(MESSAGE_NOT_VALID_FILENAME_SAVE) > 0

    def test_not_valid_filename_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_VALID_FILENAME, str)

    def test_not_valid_filename_is_not_empty(self) -> None:
        assert len(MESSAGE_NOT_VALID_FILENAME) > 0

    def test_not_found_dialog_type_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_DIALOG_TYPE, str)

    def test_not_found_dialog_type_is_not_empty(self) -> None:
        assert len(MESSAGE_NOT_FOUND_DIALOG_TYPE) > 0

    def test_all_messages_are_unique(self) -> None:
        all_messages: list[str] = [
            MESSAGE_ERROR_APP,
            MESSAGE_ERROR_AUDIO_NOT_STARTED,
            MESSAGE_NOT_VALID_FILENAME_SAVE,
            MESSAGE_NOT_VALID_FILENAME,
            MESSAGE_NOT_FOUND_DIALOG_TYPE,
        ]
        assert len(all_messages) == len(set(all_messages))
