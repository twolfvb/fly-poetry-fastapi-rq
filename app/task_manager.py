import os
from typing import Any, Protocol

from rq import Queue

from app.redis_client import get_client as get_redis_client


class TaskManager(Protocol):
    """TaskManager."""

    def enqueue(self, job: Any, *args: Any, **kwargs: Any) -> str:
        """Enqueue job."""
        raise NotImplementedError


class RQTaskManager:
    """RQTaskManager."""

    def __init__(self) -> None:
        """Initialize."""
        redis_instance = get_redis_client()
        self._q = Queue(connection=redis_instance)

    def enqueue(self, job: Any, *args: Any, **kwargs: Any) -> str:
        """Enqueue job."""
        return str(self._q.enqueue(job, *args, **kwargs).id)


def get_task_manager() -> TaskManager:
    """Get TaskManager instance."""
    manager = os.getenv("TASK_MANAGER", "RQ")
    match manager:
        case "RQ":
            return RQTaskManager()
        case _:
            raise ValueError(f"Unknown task manager: {manager}")
