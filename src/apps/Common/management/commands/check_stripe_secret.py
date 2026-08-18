import os
import time
import structlog

from django.core.management.base import BaseCommand

logger = structlog.get_logger(__name__)


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

        logger.info("Running command check_stripe_secret")
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Check if secret file exists
            if os.path.exists(secret_file):
                try:
                    with open(secret_file, "r") as f:
                        secret = f.read().strip()

                    if secret and secret.startswith("whsec_"):
                        logger.info(
                            "Stipe webhook secret loaded sucessfully",
                            secret=secret,
                        )

                        os.environ["STRIPE_WEBHOOK_SECRET"] = secret
                        return
                    else:
                        logger.info("Secret already exist")
                except IOError as e:
                    logger.error(
                        "check_stripe_secret_failed",
                        reason=e,
                    )
            time.sleep(1)

        # Timeout reached
        logger.error(
            "check_stripe_secret_failed",
            reason="Time out reached",
        )
