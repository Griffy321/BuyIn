from buyin.data import config
from buyin.features.players import player_repository
from buyin.features.players.player import Player
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from buyin.api import responses
from buyin.api import players

# config.create_table(player_repository.DB_NAME, player_repository.TABLE_NAME, Player, "player_id")

app = FastAPI()

app.add_exception_handler(HTTPException, handler=responses.handle_http_exception)
app.include_router(players.router)
