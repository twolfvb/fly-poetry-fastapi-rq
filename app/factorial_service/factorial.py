""" factorial calculation implementation """
import logging

logger = logging.getLogger(__name__)


def calc_factorial(number: int) -> int:
    """Calculate factorial."""
    result = 1
    for i in range(1, number + 1):
        result *= i
    logger.warning("Result is'%s'", result)
    return result
