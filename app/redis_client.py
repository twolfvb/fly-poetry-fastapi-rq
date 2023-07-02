"""Redis client module"""
from __future__ import annotations

import logging
import os

from redis import Redis

logger = logging.getLogger(__name__)


def get_client() -> Redis[bytes]:
    """Get Redis client using environment variables."""
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_pass = os.getenv("REDIS_PASS", "")

    logger.info("Connecting to redis at %s:%s", redis_host, redis_port)
    redis_client = Redis(host=redis_host, port=redis_port, password=redis_pass)
    if not redis_client.ping():
        raise RuntimeError("Cannot connect to Redis")
    return redis_client
