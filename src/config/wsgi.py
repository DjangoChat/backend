from django.core.wsgi import get_wsgi_application

from config.telemetry import configure_opentelemetry

configure_opentelemetry(
    service_name="neuroconnect",
    otlp_endpoint="http://otel-collector:4317",
)

application = get_wsgi_application()
