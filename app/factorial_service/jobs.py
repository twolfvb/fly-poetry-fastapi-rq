""" Can be both used as rq jobs or celery tasks. """
import logging

import httpx
from celery import shared_task

from app.environment import is_production
from app.factorial_service.factorial import calc_factorial

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@shared_task()
async def factorial_job(number: int, url: str | None = None) -> None:
    """Calculate factorial."""
    logger.info("Calculating factorial for %d", number)

    result = calc_factorial(number)

    if url is None and is_production():
        logger.info("No webhook url provided")
        return
    if url is None or url == "":
        logger.info("No webhook url provided")
        return

    headers = {"Content-Type": "application/json"}

    logger.info("Sending webhook to %s", url)

    async with httpx.AsyncClient() as client:
        await client.post(url, params={"result": str(result)}, headers=headers)
        logger.info("Webhook sent to %s", url)
