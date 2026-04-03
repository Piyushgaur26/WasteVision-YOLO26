import sys
import traceback
from typing import Optional


def format_error_message(error: Exception) -> str:
    """
    Extracts detailed error information including file name and line number.
    """
    exc_type, exc_value, exc_tb = sys.exc_info()

    if exc_tb is None:
        return f"{type(error).__name__}: {error}"

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    return (
        f"Error in [{file_name}] "
        f"at line [{line_number}] "
        f"| {type(error).__name__}: {error}"
    )


class AppException(Exception):
    """
    Custom exception class with enriched error context.
    """

    def __init__(self, error: Exception, context: Optional[str] = None):
        self.original_error = error
        self.context = context
        self.detailed_message = format_error_message(error)

        if context:
            self.detailed_message = f"{context} -> {self.detailed_message}"

        super().__init__(self.detailed_message)

    def __str__(self) -> str:
        return self.detailed_message