# Building responses, shared by every endpoint.
#
# Look up: FastAPI "Custom Response" and "Handling Errors".
#
# TODO 1: a helper that returns a "problem" error response, the standard JSON shape for API errors:
#   {"type": "...", "title": "...", "status": 404, "detail": "..."}
#   with Content-Type: application/problem+json
#   Your endpoints use it for the 404 and 500 cases.


# TODO 2: an exception handler that main.py registers on the app.
#   Decide what errors like 400 / 404 (unknown route) / 405 (wrong method) should look like.
#   FastAPI's default is {"detail": "..."}. The old server sent the status code with an empty body.
