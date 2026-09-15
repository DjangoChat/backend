from __future__ import absolute_import, unicode_literals

import logging

import structlog
from celery import Celery
from celery.signals import setup_logging
from django_structlog.celery.steps import DjangoStructLogInitStep

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.steps["worker"].add(DjangoStructLogInitStep)  # type: ignore
app.autodiscover_tasks()


@setup_logging.connect
def receiver_setup_logging(
    loglevel,
    logfile,
    format,
    colorize,
    **kwargs,
):
    logging.config.dictConfig(  # type: ignore
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json_formatter": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(),
                },
                "plain_console": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(),
                },
                "key_value": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.KeyValueRenderer(
                        key_order=["timestamp", "level", "event", "logger"]
                    ),
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "plain_console",
                },
                "json_file": {
                    "class": "logging.handlers.WatchedFileHandler",
                    "filename": "logs/json.log",
                    "formatter": "json_formatter",
                },
                "flat_line_file": {
                    "class": "logging.handlers.WatchedFileHandler",
                    "filename": "logs/flat_line.log",
                    "formatter": "key_value",
                },
            },
            "loggers": {
                "django_structlog": {
                    "handlers": ["console", "flat_line_file", "json_file"],
                    "level": "INFO",
                },
                "django_structlog_demo_project": {
                    "handlers": ["console", "flat_line_file", "json_file"],
                    "level": "INFO",
                },
            },
        }
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
