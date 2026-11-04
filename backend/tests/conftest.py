"""Shared pytest fixtures.

The DB engine is created at import time from settings, so the test database
URL must be set *before* any `app.*` module is imported.
"""
from __future__ import annotations

import os
import sys
import tempfile

_TMP_DIR = tempfile.mkdtemp(prefix="bkcourse-test-")
os.environ["DB_URL"] = f"sqlite:///{os.path.join(_TMP_DIR, 'test.db')}"
os.environ.setdefault("JWT_SECRET", "test-secret-key-that-is-long-enough-for-hs256")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

SAMPLE_PASTE = """CO3117 - Học máy
A01\t10/70\tV\tA01\t\t\t\t70\t
Thứ 6\t- - - - - - - 8 9 - - - - - - -\tB4-405\t1\t\t1234--789-12345678------------
L01\t80/80\tV\tL01\t\t\t\t80\t
Thứ 3\t- - - 4 5 - - - - - - - - - - -\tH3-402\t2\t\t1234--789-12345678------------
CO3001 - Công nghệ phần mềm
L01\t50/80\tV\tL01\t\t\t\t80\t
Thứ 2\t- - 3 4 5 - - - - - - - - - - -\tH6-101\t2\t\t1234--789-12345678------------
L02\t50/80\tV\tL02\t\t\t\t80\t
Thứ 6\t- - - - - - - 8 9 - - - - - - -\tB1-201\t1\t\t1234--789-12345678------------
"""


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def sample_paste() -> str:
    return SAMPLE_PASTE
