# Building responses, shared by every endpoint.
#
# Look up: FastAPI "Custom Response" and "Handling Errors".
#
# TODO 1: a helper that returns a "problem" error response, the standard JSON shape for API errors:
#   {"type": "...", "title": "...", "status": 404, "detail": "..."}
#   with Content-Type: application/problem+json
#   Your endpoints use it for the 404 and 500 cases.
from fastapi import Request
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse
from http import HTTPStatus


def problem(status: int, detail: str, headers: dict[str, str] | None = None) -> JSONResponse:
    """for errors your endpoints return themselves, e.g. return problem(404, "No player with ID abc")"""
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        headers=headers,
        content={
            "type": "about:blank",
            "title": HTTPStatus(status).phrase,
            "status": status,
            "detail": detail,
        },
    )


async def handle_http_exception(request: Request, exception: HTTPException) -> JSONResponse:
    """for errors that get raised, this will send them to the client in a standard way"""
    return problem(exception.status_code, exception.detail, exception.headers)