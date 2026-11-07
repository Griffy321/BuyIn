from dataclasses import dataclass
from buyin.tools import logger
from buyin.tools.random_string import generate_uid
from buyin.tools.helpers import is_blank

_RESOURCE = "Player"


@dataclass(init=False)
class Player:
    # field order is the column order in the database
    player_first_name: str
    player_last_name: str
    player_id: str

    def __init__(self, first_name: str | None, last_name: str | None, player_id: str | None = None):
        if is_blank(player_id):
            self.player_id = generate_uid()
            logger.info(body="Player created", resource=_RESOURCE, attributes={"playerId": self.player_id})
        else:
            self.player_id = player_id
            logger.info(body="Player created", resource=_RESOURCE, attributes={"playerId": self.player_id})
        if is_blank(first_name):
            self.player_first_name = ""
            logger.warn(body="Player created with a blank first name", resource=_RESOURCE, attributes={"playerId": self.player_id})
        else:
            self.player_first_name = first_name
        if is_blank(last_name):
            self.player_last_name = ""
            logger.warn(body="Player created with a blank last name", resource=_RESOURCE, attributes={"playerId": self.player_id})
        else:
            self.player_last_name = last_name
        logger.info(body="Player created", resource=_RESOURCE, attributes={"playerId": self.player_id})
