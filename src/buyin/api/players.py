from fastapi import APIRouter
from buyin.features.players.player import Player
from buyin.features.players import player_repository
from buyin.tools.helpers import is_blank
from buyin.api.responses import problem
from buyin.data.write import write_record
from buyin.api.requests import CreatePlayerRequest

ENDPOINT = "/players"

router = APIRouter()


@router.post("/players") # make new player # add checks on the values that come in
async def make_player(body: CreatePlayerRequest):
    if is_blank(body.first_name) or is_blank(body.last_name):
        return problem(400, "Please provide both first and last name")
    player = Player(first_name=body.first_name, last_name=body.last_name)
    saved = write_record(player_repository.DB_NAME, player_repository.TABLE_NAME, player)
    if not saved:
        return problem(500, "Couldn't save the player")
    return {"playerId": player.player_id}


@router.get("/players/{player_id}") # player details
async def get_player_info(player_id: str):
    try: 
        player_details = player_repository.get_player_info(player_id=player_id)
        if player_details is None:
            return problem(status=404, detail=f"No player with ID {player_id}")
        else:
            return {
                    "playerId": player_details.player_id, 
                    "firstName": player_details.player_first_name, 
                    "lastName": player_details.player_last_name
                    }
    except Exception:
        return problem(status=500, detail="Internal server error")