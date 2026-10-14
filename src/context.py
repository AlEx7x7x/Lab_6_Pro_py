from contextlib import contextmanager
import logging
from time import perf_counter

logger = logging.getLogger(__name__)


@contextmanager
def logged_operation(name: str):
    """Власний context manager: реєструє початок, помилку або тривалість операції."""
    start = perf_counter()
    logger.info("%s: початок", name)
    try:
        yield
    except Exception:
        logger.exception("%s: помилка", name)
        raise
    else:
        logger.info("%s: завершено за %.4f с", name, perf_counter() - start)
