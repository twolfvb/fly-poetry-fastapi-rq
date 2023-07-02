import logging

import httpx

from app.environment import is_production
from app.factorial_service.factorial import calc_factorial

logger = logging.getLogger(__name__)

_TOO_BIG = "ran out of memory bro"
_NEGATIVE = "Number must be positive"


async def factorial_job(number: int, url: str | None = None) -> None:
    """Calculate factorial."""
    logger.info("Calculating factorial for %d", number)
    if number < 0:
        logger.warning("Result is '%s'", _NEGATIVE)
        return
    if number > 10:
        logger.warning("Result is '%s'", _TOO_BIG)
        return

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
