# The /players endpoints. The app in mobile/src/api/players.js calls these.
#
# Look up: FastAPI "Bigger Applications - Multiple Files" (APIRouter) and "Path Parameters".
#
# TODO 1: create an APIRouter called `router`. main.py will plug it into the app.


# TODO 2: POST /players
#   - Body: JSON with firstName and lastName, e.g. {"firstName": "James", "lastName": "G"}
#     (use your helper in requests.py to read it)
#   - Make a Player and save it with write.write_record(...)
#   - Saved:      200  {"playerId": "..."}
#   - Not saved:  500  problem response (see responses.py)


# TODO 3: GET /players/{player_id}
#   - Look the player up with player_repository.get_player_info(...)
#   - Found:              200  {"playerId": "...", "firstName": "...", "lastName": "..."}
#   - Not found (None):   404  problem response. The app relies on this 404 to forget a stale saved ID.
#   - Exception raised:   500  problem response. The app keeps its saved ID and offers a retry.
#   (Note: JSON keys are camelCase even though the Python fields are snake_case.)
