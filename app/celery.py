"""Celery client to be used by the application."""
import os
from typing import Any

from celery import current_app


def _get_broker_url() -> str:
    """Get broker url."""
    return os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")


class CeleryConfig:
    """Celery configuration."""

    broker_url = _get_broker_url()
    task_time_limit = 600


def create_celery() -> Any:
    """Create celery app."""
    celery_app = current_app
    celery_app.config_from_object(CeleryConfig)
    print(CeleryConfig.broker_url)

    # If tasks are created in other modules, they should be included here
    celery_app.autodiscover_tasks(
        [
            "app.factorial_service.jobs",
        ]
    )

    return celery_app


celery = create_celery()
print("celery", celery)
