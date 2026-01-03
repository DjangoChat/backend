import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as PsycopgOperationalError


class Command(BaseCommand):

    def handle(self, *args, **options):

        self.stdout.write("Waiting for database readiness...")
        is_db_up = False

        while is_db_up is False:
            try:
                self.check(databases=["default"])  # type: ignore
                is_db_up = True
            except (PsycopgOperationalError, OperationalError):
                self.stdout.write("Database not ready yet...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database now ready!"))
