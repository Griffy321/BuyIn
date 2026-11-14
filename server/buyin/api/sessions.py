from fastapi import APIRouter
from buyin.features.players.player_repository import player_exists
from buyin.api.responses import problem
from buyin.api.requests import CreateSessionRequest, CreateSessionPlayerRequest
from buyin.features.sessions.session_repository import session_player_exists, session_exists
from buyin.features.sessions.session import Session
from buyin.features.sessions.session_player import SessionPlayer

router = APIRouter()


@router.post("/sessions") # endpoint to make a session
async def make_new_session(body: CreateSessionRequest):
    try:
        exists = player_exists(body.player_id)
        if not exists:
            problem()
        session = Session(host_player_id=body.player_id)

    except Exception:
        return problem(status=500, detail="Internal server error")



@router.post("sessions/{session_id}/players")
async def make_new_session_player(body: CreateSessionPlayerRequest):
    pass
