import tempfile
from unittest import mock

import pytest

from termometro import create_app
import termometro.db as tdb


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "test.db"
    with mock.patch.object(tdb, "DB_PATH", str(path)):
        yield str(path)


@pytest.fixture
def app(db_path):
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()
