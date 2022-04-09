import logging
from functools import wraps
from typing import Optional


class UserError(Exception):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)


def user_error_handler(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UserError as error:
            logging.error(str(error))
            raise SystemExit

    return inner
