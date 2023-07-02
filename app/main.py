import logging
import os

import httpx
from fastapi import FastAPI
from rq import Queue

from app.redis_client import get_client as get_redis_client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

redis_instance = get_redis_client()
q = Queue(connection=redis_instance)


@app.get("/", tags=["health"], operation_id="check", response_model=str)
def index() -> str:
    """Health check endpoint."""
    return "ok"


@app.post(
    "/factorial",
    tags=["factorial"],
    operation_id="factorial",
    response_model=str,
)
def factorial(number: int, endpoint: str | None) -> str:
    """Factorial endpoint."""
    job = q.enqueue(factorial_job, number, endpoint)
    return str(job.id)


@app.post("/webhook", tags=["webhook"], operation_id="webhook")
async def webhook(result: int) -> None:
    """Webhook endpoint."""
    logger.info("The webhook was hit, result was: %d", result)


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
    if url is None:
        url = "http://localhost:3000/webhook"
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        await client.post(url, data={"result": str(result)}, headers=headers)
        logger.info("Webhook sent to %s", url)


def calc_factorial(number: int) -> int:
    """Calculate factorial."""
    result = 1
    for i in range(1, number + 1):
        result *= i
    logger.warning("Result is '%d'", result)
    return result


def is_production() -> bool:
    """Check if we are in production."""
    return os.getenv("APP_ENV", "development") == "production"
