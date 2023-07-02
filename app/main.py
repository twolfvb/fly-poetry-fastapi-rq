import logging
from typing import Optional

from fastapi import FastAPI
from rq import Queue

from app.factorial_service.jobs import factorial_job
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
def factorial(number: int, endpoint: Optional[str] = None) -> str:
    """Factorial endpoint."""
    job = q.enqueue(factorial_job, number, endpoint)
    return str(job.id)


@app.post("/webhook", tags=["webhook"], operation_id="webhook")
async def webhook(result: int) -> None:
    """Webhook endpoint."""
    logger.info("The webhook was hit, result was: %d", result)
