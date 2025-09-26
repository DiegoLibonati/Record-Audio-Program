import os
import sys
from pathlib import Path

import pytest

from src.core.config import resource_path


def test_resource_path_with_meipass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    fake_meipass = tmp_path / "fake_meipass"
    fake_meipass.mkdir()

    monkeypatch.setattr(sys, "_MEIPASS", str(fake_meipass), raising=False)

    rel_path = "assets/images/test.png"
    expected = os.path.join(str(fake_meipass), rel_path)

    assert resource_path(rel_path) == expected


def test_resource_path_without_meipass(monkeypatch: pytest.MonkeyPatch):
    if hasattr(sys, "_MEIPASS"):
        monkeypatch.delattr(sys, "_MEIPASS")

    rel_path = "assets/images/test.png"
    expected = os.path.join(os.path.abspath("."), rel_path)

    assert resource_path(rel_path) == expected
