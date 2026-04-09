import os
import time

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Wait for Stripe webhook secret to be available"

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=30,
            help="Timeout in seconds to wait for the secret (default: 30)",
        )

    def handle(self, *args, **options):
        timeout = options["timeout"]
        secret_file = "/stripe-secrets/webhook_secret"

        self.stdout.write("Waiting for Stripe webhook secret...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Check if secret file exists
            if os.path.exists(secret_file):
                try:
                    with open(secret_file, "r") as f:
                        secret = f.read().strip()

                    if secret and secret.startswith("whsec_"):
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✓ Stripe webhook secret loaded successfully: {secret[:20]}..."
                            )
                        )
                        # Set it as environment variable for this process
                        os.environ["STRIPE_WEBHOOK_SECRET"] = secret
                        return
                    else:
                        self.stdout.write("Secret file exists but content is invalid")
                except IOError as e:
                    self.stdout.write(f"Error reading secret file: {e}")

            elapsed = time.time() - start_time
            remaining = timeout - elapsed
            self.stdout.write(
                f"Secret not ready yet... ({elapsed:.0f}s/{timeout}s, {remaining:.0f}s remaining)"
            )
            time.sleep(1)

        # Timeout reached
        self.stdout.write(
            self.style.WARNING(
                f"⚠ Stripe webhook secret not found after {timeout} seconds"
            )
        )

        # Check if there's a fallback secret in environment
        if os.environ.get("STRIPE_WEBHOOK_SECRET"):
            self.stdout.write(
                self.style.WARNING("Using fallback secret from environment")
            )
        else:
            raise CommandError(
                "STRIPE_WEBHOOK_SECRET is not set and no secret file was generated. "
                "Make sure stripe-cli container is running."
            )
