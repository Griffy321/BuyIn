# Reading request bodies, shared by every endpoint that takes JSON.
#
# Look up: FastAPI "Using the Request Directly" and "Request Body".
# FastAPI's usual approach is a Pydantic model as the endpoint parameter. That's
# fine to use instead of this file, but note it returns 422 (not 400) for bad bodies
# and matches JSON keys case-sensitively.
#
# TODO: write the helper(s) your endpoints use to turn a request body into data.
#   Things worth handling:
#   - Content-Type isn't JSON          -> 415
#   - Body is empty or not valid JSON  -> 400
#   - A field has the wrong type       -> 400
