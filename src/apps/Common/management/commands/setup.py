from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Initialize application default data"

    def handle(self, *args, **options):
        commands = [
            "create_groups",
            "create_currency",
            "create_period",
            "create_plan",
            "create_price",
            "create_feature",
            "create_quota",
            "create_quota_plan",
            "create_nature",
            "create_policies_rules",
            "create_participant_agent",
        ]

        for command in commands:
            self.stdout.write(f"Running {command}...")
            call_command(command)

        self.stdout.write(self.style.SUCCESS("Application setup completed."))
