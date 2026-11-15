from fastapi import APIRouter
from buyin.features.players.player_repository import player_exists
from buyin.api.responses import problem
from buyin.api.requests import CreateSessionRequest, CreateSessionPlayerRequest
from buyin.features.sessions.session_repository import (
    session_exists, session_player_exists, get_session_info, get_session_player_info, 
    player_currently_in_session, save_session, save_session_player, end_session, end_session_player
    )
from buyin.features.sessions.session import Session
from buyin.features.sessions.session_player import SessionPlayer

router = APIRouter()


@router.post("/sessions") # endpoint to make a session
async def make_session(body: CreateSessionRequest):
    """
    Makes the new session and saves it to the db.
    Returns the session id.
    """
    try:
        exists = player_exists(body.player_id)
        if not exists:
            return problem(status=404, detail=f"No player with ID {body.player_id}")
        in_session = player_currently_in_session(body.player_id)
        if in_session:
            return problem(status=409, detail=f"Player {body.player_id} is already in an active session")

        session = Session(host_player_id=body.player_id)
        session_player = SessionPlayer(player_id=body.player_id, session_id=session.session_id, buyin=body.buyin)
        host_added = session.add_host(session_player)

        if not host_added:
            return problem(status=500, detail="Couldn't add the host")

        saved_session = save_session(session)

        if saved_session is not None:
            saved_session_player = save_session_player(session_player)
            if saved_session_player is not None:
                return {"sessionId": session.session_id, "sessionPlayerId": session_player.session_player_id}
        return problem(status=500, detail="Couldn't save the session")

    except Exception:
        return problem(status=500, detail="Internal server error")



@router.post("/sessions/{session_id}/players")
async def make_session_player(session_id: str, body: CreateSessionPlayerRequest):
    try:
        exists = player_exists(body.player_id)
        if not exists:
            return problem(status=404, detail=f"No player with ID {body.player_id}")
        in_session = player_currently_in_session(body.player_id)
        if in_session:
            return problem(status=409, detail=f"Player {body.player_id} is already in an active session")
        session_is_active = session_exists(session_id)
        if not session_is_active:
            return problem(status=404, detail=f"No active session with ID {session_id}")

        session_player = SessionPlayer(player_id=body.player_id, session_id=session_id, buyin=body.buyin)

        saved_session_player = save_session_player(session_player)
        if saved_session_player is not None:
            return {"sessionId": session_id, "sessionPlayerId": saved_session_player.session_player_id}
        return problem(status=500, detail="Couldn't save the session player")

    except Exception:
        return problem(status=500, detail="Couldn't save the session player")