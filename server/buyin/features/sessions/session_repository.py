from contextlib import closing

from buyin.data.config import create_connection
from buyin.features.players.player import Player
from buyin.tools import logger
from buyin.features.players import player_repository


_RESOURCE = "SessionPlayerData"

DB_NAME = "BuyInPlayerSession.db"
TABLE_NAME = "SessionPlayers"


def session_player_exists(session_player_id: str):
    """
    Checks if the session player record has is_settled = false meaning they are still in play and 'exist' in a session. 
    Returns a bool.
    """
    pass


def session_exists(session_id: str):
    """
    Checks if the session record has is_settled = false meaning there is still players in the session.
    Returns a bool.
    """
    pass


def make_new_session(host_player_id: str):
    """
    Creates a new session for session players to join. 
    Returns the session ID.
    """
    pass


def make_session_player(player_id: str, session_id: str, buyin: int):
    """
    Creates a new session player to be added to a session. 
    Returns the session player ID.
    """
    pass


def end_session_player(session_player_id: str):
    """
    Ends the session for the session player.
    Returns a bool.
    """
    pass


def end_session(session_id: str):
    """
    Ends the session.
    Returns a bool.
    """
    pass