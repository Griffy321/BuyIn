from contextlib import closing

from buyin.data.config import create_connection
from buyin.features.players.player import Player
from buyin.tools import logger

_RESOURCE = "PlayerData"

# the one place the player db and table names live; main.py uses them too
DB_NAME = "BuyInPlayer.db"
TABLE_NAME = "Players"


def get_player_info(player_id: str) -> Player | None:
    try:
        with closing(create_connection(DB_NAME)) as connection:
            row = connection.execute(
                f"""
                select PlayerFirstName, PlayerLastName, PlayerId from {TABLE_NAME} where playerId = :playerId
                """,
                {"playerId": player_id},
            ).fetchone()

            if row is not None:
                first, last, id_ = row
                return Player(first, last, id_)
            else:
                logger.info(body="Player not found", resource=_RESOURCE, attributes={"playerId": player_id})
                return None
    except Exception as e:
        logger.error(body="Failed to read player", resource=_RESOURCE, attributes={"playerId": player_id, "tableName": TABLE_NAME}, exception=e)
        raise
