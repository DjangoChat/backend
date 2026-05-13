import time
from socket import gaierror

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError
from django.db import connections

from psycopg2 import OperationalError as PsycopgOperationalError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=60,
            help="Timeout in seconds to wait for the database (default: 60)",
        )

    def handle(self, *args, **options):
        timeout = options["timeout"]

        self.stdout.write("Waiting for database readiness...")
        start_time = time.time()
        is_db_up = False
        last_error = None
        attempt = 0

        while not is_db_up and time.time() - start_time < timeout:
            attempt += 1
            try:
                # Try to close any stale connections first
                connections.close_all()
                # Then check the connection
                self.check(databases=["default"])  # type: ignore
                is_db_up = True
            except (PsycopgOperationalError, OperationalError, gaierror) as e:
                last_error = e
                elapsed = time.time() - start_time
                error_type = type(e).__name__
                error_msg = str(e)[:80]
                self.stdout.write(
                    f"[{elapsed:.1f}s] Attempt {attempt}: {error_type}: {error_msg}"
                )
                # Increase sleep to give DNS more time to recover
                sleep_time = min(3, 1 + (attempt * 0.5))
                self.stdout.write(f"Retrying in {sleep_time:.1f}s...")
                time.sleep(sleep_time)

        if is_db_up:
            self.stdout.write(self.style.SUCCESS("✓ Database now ready!"))
        else:
            error_msg = f"Database not ready after {timeout}s ({attempt} attempts)"
            if last_error:
                error_msg += f": {type(last_error).__name__}"
            raise CommandError(error_msg)
