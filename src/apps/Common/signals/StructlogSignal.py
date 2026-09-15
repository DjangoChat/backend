from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import receiver

import structlog
from django_structlog import signals
from django_structlog.celery import signals as celery_signals


@receiver(signals.update_failure_response)
@receiver(signals.bind_extra_request_finished_metadata)
def add_request_id_to_response(response, logger, **kwargs):
    context = structlog.contextvars.get_merged_contextvars(logger)
    response["X-Request-ID"] = context["request_id"]


@receiver(signals.bind_extra_request_failed_metadata)
def bind_domain_request_failed(request, logger, exception, log_kwargs, **kwargs):
    current_site = get_current_site(request)
    structlog.contextvars.bind_contextvars(domain=current_site.domain)


@receiver(signals.bind_extra_request_finished_metadata)
def bind_domain_request_finished(request, logger, response, log_kwargs, **kwargs):
    current_site = get_current_site(request)
    structlog.contextvars.bind_contextvars(domain=current_site.domain)


@receiver(signals.bind_extra_request_metadata)
def bind_domain_request_metadata(request, logger, log_kwargs, **kwargs):
    current_site = get_current_site(request)
    structlog.contextvars.bind_contextvars(domain=current_site.domain)


@receiver(celery_signals.bind_extra_task_metadata)
def receiver_bind_extra_task_metadata(sender, signal, task=None, logger=None, **kwargs):
    assert task is not None
    structlog.contextvars.bind_contextvars(correlation_id=task.request.correlation_id)


@receiver(celery_signals.pre_task_succeeded)
def receiver_pre_task_succeeded(sender, signal, logger=None, result=None, **kwargs):
    structlog.contextvars.bind_contextvars(result=str(result))


# TODO: add id token from user
"""
@receiver(bind_extra_request_metadata)
def bind_token_user_id(request, logger, **kwargs):
    try:
        header = request.META.get("HTTP_AUTHORIZATION")
        if header:
            raw_token = header.split()[1]
            token = UntypedToken(raw_token)
            user_id = token["user_id"]
            structlog.contextvars.bind_contextvars(user_id=user_id)
    except Exception:
        pass
"""
