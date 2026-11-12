from fastapi import APIRouter
from buyin.features.players.player import Player
from buyin.features.players import player_repository
from buyin.tools.helpers import is_blank
from buyin.api.responses import problem
from buyin.data.write import write_record
from buyin.api.requests import CreateSessionRequest, CreateSessionPlayerRequest


router = APIRouter()


@router.post("/session/{player_id}")
async def make_new_session(body: CreateSessionRequest):
    try:
        exists = player_repository.player_exists(body.player_id)

    except Exception:
        return problem(status=500, detail="Internal server error")



async def make_new_session_player(body: CreateSessionPlayerRequest):
    pass
