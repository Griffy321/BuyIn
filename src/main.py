import json
from dataclasses import dataclass

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.exceptions import HTTPException

from buyin.data import config, write
from buyin.features.players import player_repository
from buyin.features.players.player import Player

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, redirect_slashes=False)

config.create_table(player_repository.DB_NAME, player_repository.TABLE_NAME, Player, "player_id")


# --- request bodies (JSON property names are matched case-insensitively) ---

@dataclass
class CreatePlayerRequest:
    first_name: str | None
    last_name: str | None


async def read_create_player_request(request: Request) -> CreatePlayerRequest:
    data = await _read_json_object(request)
    values = []
    for name in ("firstName", "lastName"):
        value = data.get(name.lower())
        if value is not None and not isinstance(value, str):
            raise HTTPException(status_code=400)
        values.append(value)
    return CreatePlayerRequest(*values)


async def _read_json_object(request: Request) -> dict:
    media_type = request.headers.get("content-type", "").split(";")[0].strip().lower()
    if not (media_type == "application/json" or media_type.endswith("+json")):
        raise HTTPException(status_code=415)
    try:
        data = json.loads(await request.body())
    except ValueError:
        raise HTTPException(status_code=400)
    if not isinstance(data, dict):
        raise HTTPException(status_code=400)
    return {key.lower(): value for key, value in data.items()}


# --- responses ---

def json_response(content: dict, status_code: int = 200) -> Response:
    return Response(json.dumps(content, separators=(",", ":")), status_code=status_code, media_type="application/json; charset=utf-8")


_PROBLEM_TYPES = {
    404: "https://tools.ietf.org/html/rfc9110#section-15.5.5",
    500: "https://tools.ietf.org/html/rfc9110#section-15.6.1",
}


def problem(detail: str, status_code: int, title: str) -> Response:
    body = {"type": _PROBLEM_TYPES[status_code], "title": title, "status": status_code, "detail": detail}
    return Response(json.dumps(body, separators=(",", ":")), status_code=status_code, media_type="application/problem+json")


@app.exception_handler(HTTPException)
async def empty_error_response(request: Request, exc: HTTPException) -> Response:
    # bad bodies, unknown routes and wrong methods get a bare status code with no body
    return Response(status_code=exc.status_code, headers=exc.headers)


# --- endpoints ---

@app.post("/players")  # post has a body
async def create_player(request: Request):
    req = await read_create_player_request(request)
    player = Player(req.first_name, req.last_name)
    is_player_inserted = write.write_record(player_repository.DB_NAME, player_repository.TABLE_NAME, player)
    if is_player_inserted:
        return json_response({"playerId": player.player_id})
    else:
        return problem(detail="Failed to create the user.", status_code=500, title="Server error")


@app.get("/players/{player_id}")  # get has no body so just takes a player id from the path
def get_player(player_id: str):
    try:
        data = player_repository.get_player_info(player_id)
        if data is not None:
            return json_response({"playerId": data.player_id, "firstName": data.player_first_name, "lastName": data.player_last_name})
        else:
            # no player with that id: the app forgets its saved id when it gets a 404
            return problem(detail=f"No player with id {player_id}.", status_code=404, title="Player not found")
    except Exception:  # the repository already logged the exception, so it isn't needed here
        # something broke on our side: the app keeps its saved id and shows an error when it gets a 500
        return problem(detail="Failed to read the player.", status_code=500, title="Server error")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
