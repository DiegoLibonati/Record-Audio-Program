from tkinter import CENTER, FLAT

from src.ui.styles import Styles


class TestStyles:
    def test_primary_color(self) -> None:
        assert Styles.PRIMARY_COLOR == "#0099FF"

    def test_secondary_color(self) -> None:
        assert Styles.SECONDARY_COLOR == "#E43A3A"

    def test_white_color(self) -> None:
        assert Styles.WHITE_COLOR == "#FFFFFF"

    def test_black_color(self) -> None:
        assert Styles.BLACK_COLOR == "#000000"

    def test_font_roboto_base(self) -> None:
        assert Styles.FONT_ROBOTO == "Roboto"

    def test_font_roboto_12(self) -> None:
        assert Styles.FONT_ROBOTO_12 == "Roboto 12"

    def test_font_roboto_13(self) -> None:
        assert Styles.FONT_ROBOTO_13 == "Roboto 13"

    def test_font_roboto_14(self) -> None:
        assert Styles.FONT_ROBOTO_14 == "Roboto 14"

    def test_font_roboto_15(self) -> None:
        assert Styles.FONT_ROBOTO_15 == "Roboto 15"

    def test_font_roboto_20(self) -> None:
        assert Styles.FONT_ROBOTO_20 == "Roboto 20"

    def test_center(self) -> None:
        assert Styles.CENTER == CENTER

    def test_anchor_center(self) -> None:
        assert Styles.ANCHOR_CENTER == CENTER

    def test_relief_flat(self) -> None:
        assert Styles.RELIEF_FLAT == FLAT

    def test_instantiation(self) -> None:
        styles: Styles = Styles()
        assert styles.PRIMARY_COLOR == "#0099FF"
