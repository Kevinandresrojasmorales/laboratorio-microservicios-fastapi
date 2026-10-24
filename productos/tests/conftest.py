import os
from contextlib import contextmanager
from unittest.mock import Mock

import pytest

os.environ.setdefault(
    "DATABASE_URL",
    "sqlite:///./test.db",
)


@contextmanager
def fake_connection():
    yield Mock()


@pytest.fixture(autouse=True)
def fake_database(monkeypatch):
    from app import main

    fake_engine = Mock()
    fake_engine.begin.return_value = fake_connection()
    fake_engine.connect.return_value = fake_connection()
    monkeypatch.setattr(main, "engine", fake_engine)
