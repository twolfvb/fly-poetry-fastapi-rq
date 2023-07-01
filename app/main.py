import logging
import os

from fastapi import FastAPI
from redis import Redis
from rq import Queue

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
# from env variable
# now I need redis hostname port password
redis_host  = os.getenv("REDIS_HOST", "localhost")
redis_port  = os.getenv("REDIS_PORT", "6379")
redis_pass  = os.getenv("REDIS_PASS", "")

logger.info("Connecting to redis at %s:%s", redis_host, redis_port)
r = Redis(host=redis_host, port=redis_port, password=redis_pass)  # type: ignore
logger.info("Connected to redis? %s", r.ping())
q = Queue(connection=r)

@app.get("/", tags=["health"], operation_id="check", response_model=str)
def index() -> str:
    """Health check endpoint."""
    return "ok"


@app.post("/factorial", tags=["factorial"], operation_id="factorial", response_model=str)
def factorial(number: int) -> str:
    """Factorial endpoint."""
    # sleep for 5 seconds
    job = q.enqueue(calc_factorial, number)
    return job.id


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
