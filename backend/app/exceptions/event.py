from fastapi import status

from app.exceptions.base import AppException

class EventNotFoundException(AppException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Event not found.",
            error_code="EVENT_NOT_FOUND"
        )