import logging

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
    "/factorial", tags=["factorial"], operation_id="factorial", response_model=str
)
def factorial(number: int) -> str:
    """Factorial endpoint."""
    # sleep for 5 seconds
    job = q.enqueue(calc_factorial, number)
    return str(job.id)


_TOO_BIG = "ran out of memory bro"
_NEGATIVE = "Number must be positive"


def calc_factorial(number: int) -> str:
    """Calculate factorial."""
    logger.info("Calculating factorial for %d", number)
    if number < 0:
        logger.warning("Result is '%s'", _NEGATIVE)
        return _NEGATIVE
    if number > 10:
        logger.warning("Result is '%s'", _TOO_BIG)
        return _TOO_BIG
    result = 1
    for i in range(1, number + 1):
        result *= i
    logger.warning("Result is '%d'", result)
    return str(result)
