from unittest import mock

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

import pytest
from psycopg2 import OperationalError as PsycopgOperationalError


@mock.patch("time.sleep", return_value=None)
def test_wait_db_command_success(mock_sleep, capsys):
    with mock.patch.object(BaseCommand, "check") as mock_check:
        # Simulate OperationalError for first 2 calls, then success
        mock_check.side_effect = [PsycopgOperationalError(), OperationalError(), None]
        call_command("wait_db")
    out = capsys.readouterr().out
    assert "Waiting for database readiness..." in out
    assert out.count("Database not ready yet...") == 2
    assert "Database now ready!" in out
