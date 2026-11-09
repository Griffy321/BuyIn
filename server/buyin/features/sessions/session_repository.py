from contextlib import closing

from buyin.data.config import create_connection
from buyin.features.players.player import Player
from buyin.tools import logger
from buyin.features.players import player_repository


_RESOURCE = "SessionPlayerData"

DB_NAME = "BuyInPlayerSession.db"
TABLE_NAME = "SessionPlayers"

