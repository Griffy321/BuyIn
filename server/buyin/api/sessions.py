from fastapi import APIRouter
from buyin.features.players import player_repository
from buyin.api.responses import problem
from buyin.api.requests import CreateSessionRequest, CreateSessionPlayerRequest


router = APIRouter()


@router.post("/sessions")
async def make_new_session(body: CreateSessionRequest):
    try:
        exists = player_repository.player_exists(body.player_id)

        #~#~ `exists` gets set but never checked, and the function never returns anything, so every call currently answers 200 with `null`.
        #~#~ Still to do: if not exists -> problem(404, ...); build the Session; save it; save the host as a SessionPlayer too; return {"sessionId": ...}.
        #~#~ write_record won't work here: it uses dataclasses.fields(), and Session / SessionPlayer aren't dataclasses, so it raises a TypeError.
        #~#~ Session also has fields that aren't columns (session_players, cash_in_play, host_player). Write the INSERTs in session_repository.

    except Exception:
        return problem(status=500, detail="Internal server error")



#~#~ and the body only needs playerId and buyin (see the comment on CreateSessionPlayerRequest).
#~#~ Checks worth doing before you insert: the session exists and isn't settled (session_exists), the player exists (player_exists),
#~#~ buyin > 0, and the player isn't already in this session. Otherwise the same person can join twice.
@router.post("sessions/{session_id}/players")
async def make_new_session_player(body: CreateSessionPlayerRequest):
    pass
