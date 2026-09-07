"""Shared error types and helpers."""

from fastapi import HTTPException, status


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, code: str = "APP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


def http_error(status_code: int, code: str, message: str, details: list | None = None) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
            "error": {
                "code": code,
                "message": message,
                "details": details or [],
            }
        },
    )


def not_found(resource: str = "Resource") -> HTTPException:
    return http_error(status.HTTP_404_NOT_FOUND, "NOT_FOUND", f"{resource} not found.")


def validation_error(message: str, details: list | None = None) -> HTTPException:
    return http_error(status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR", message, details)
