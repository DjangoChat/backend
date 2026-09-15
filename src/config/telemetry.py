import logging
import os

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib import URLLibInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_ALREADY = False


def configure_opentelemetry(
    service_name: str,
    otlp_endpoint: str,
):
    # Create resource
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": "1.0.0",
            "deployment.environment": "production",
        }
    )

    # Create tracer
    tp = TracerProvider(resource=resource)

    # Set global tracer provider
    trace.set_tracer_provider(tp)

    # Configure OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
    )
    tp.add_span_processor(BatchSpanProcessor(otlp_exporter))

    lp = LoggerProvider(resource=resource)
    set_logger_provider(lp)
    lp.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    handler = LoggingHandler(level=logging.INFO, logger_provider=lp)
    logging.getLogger().addHandler(handler)

    # Instrument libraries
    Psycopg2Instrumentor().instrument(
        tracer_provider=tp,
        skip_dep_check=True,
        enable_commenter=True,
        enable_attribute_commenter=True,
        capture_parameters=False,
    )
    LoggingInstrumentor().instrument(
        tracer_provider=tp,
        set_logging_format=True,
    )
    URLLibInstrumentor().instrument(
        tracer_provider=tp,
    )
    URLLib3Instrumentor().instrument(
        tracer_provider=tp,
    )
    RequestsInstrumentor().instrument(
        tracer_provider=tp,
    )
    DjangoInstrumentor().instrument(
        tracer_provider=tp,
        is_sql_commentor_enabled=True,
    )
    RedisInstrumentor().instrument(
        tracer_provider=tp,
    )
