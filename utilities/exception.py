
import logging
from create_logger import create_logger
def custom_exception_handler(exception: Exception) -> None:
    """
    Custom exception handler that logs the exception details.
    
    Args:
        exception (Exception): The exception to handle.
    """
    logger=create_logger(name=__name__, level=logging.ERROR)
    logger.error("An error occurred", exc_info=exception)


if __name__ == "__main__":
    try:
        result = 1 / 0  # Example to raise an exception
    except Exception as e:
        custom_exception_handler(e)