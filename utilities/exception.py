
import logging
from utilities. create_logger import create_logger
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


class PDFExtractionError(Exception):
    """
    Custom exception for errors that occur during PDF text extraction.

    Attributes:
        filepath (str): The path to the PDF file being processed.
        original_exception (Exception): The original exception that was raised.
    """
    def __init__(self, filepath: str, original_exception: Exception):
        self.filepath = filepath
        self.original_exception = original_exception
        message = f"Error extracting text from PDF: {filepath} -> {str(original_exception)}"
        super().__init__(message)
