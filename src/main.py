# Entry point: creates the app and wires everything together. Keep this file small.
#
# Run from src/ with:  python -m uvicorn main:app --reload --port 5000
# (dev.ps1 runs the same thing, but on 0.0.0.0 so your phone can reach it)

from buyin.data import config
from buyin.features.players import player_repository
from buyin.features.players.player import Player

# Not FastAPI: makes sure the Players table exists before any request comes in.
config.create_table(player_repository.DB_NAME, player_repository.TABLE_NAME, Player, "player_id")

# TODO 1: create the FastAPI app and call it `app` (uvicorn looks for main:app).
#         Look up: FastAPI "First Steps".

# TODO 2: register the error handler from buyin/api/responses.py on the app.
#         Look up: FastAPI "Handling Errors" -> "Install custom exception handlers".

# TODO 3: plug in the players routes from buyin/api/players.py.
#         Look up: FastAPI "Bigger Applications - Multiple Files" -> include_router.

# TODO 4 (optional): let `python main.py` start the server on localhost:5000.
#         Look up: uvicorn.run.
