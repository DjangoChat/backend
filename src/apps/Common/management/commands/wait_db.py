import time

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError

from psycopg2 import OperationalError as PsycopgOperationalError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=30,
            help="Timeout in seconds to wait for the secret (default: 30)",
        )

    def handle(self, *args, **options):
        timeout = options["timeout"]

        self.stdout.write("Waiting for database readiness...")
        start_time = time.time()
        is_db_up = False

        while not is_db_up and time.time() - start_time < timeout:
            try:
                self.check(databases=["default"])  # type: ignore
                is_db_up = True
            except (PsycopgOperationalError, OperationalError):
                self.stdout.write("Database not ready yet...")
                time.sleep(1)

        if is_db_up:
            self.stdout.write(self.style.SUCCESS("Database now ready!"))
        else:
            raise CommandError(f"Database not ready, timeout {timeout} reached")
