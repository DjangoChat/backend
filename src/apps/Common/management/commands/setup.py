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

        for i, command in enumerate(commands, 1):
            self.stdout.write(f"\n[{i}/{len(commands)}] Running {command}...")
            try:
                call_command(command)
                self.stdout.write(self.style.SUCCESS(f"✓ {command} completed"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ {command} failed: {str(e)}"))
                raise

        self.stdout.write(
            self.style.SUCCESS("\nApplication setup completed successfully!")
        )
