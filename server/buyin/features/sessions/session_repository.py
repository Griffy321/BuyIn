from contextlib import closing

from buyin.data.config import create_connection
from buyin.features.players.player import Player
from buyin.tools import logger
from buyin.features.players import player_repository


_RESOURCE = "SessionPlayerData"

# both tables live in one file so SessionPlayers.SessionId can reference Sessions. Schema: buyin/data/schemas/sessions.sql
DB_NAME = "BuyInSession.db"
SESSION_TABLE_NAME = "Sessions"
SESSION_PLAYER_TABLE_NAME = "SessionPlayers"


def session_player_exists(session_player_id: str):
    """
    Checks if the session player record has is_settled = false meaning they are still in play and 'exist' in a session. 
    Returns a bool.
    """
    with closing(create_connection(DB_NAME)) as connection:
        row = connection.execute(
            f"""
            select
                SessionPlayerId
            from
                {SESSION_PLAYER_TABLE_NAME}
            where
                1 = 1
                and IsSettled = 0
                and SessionPlayerId = :session_player_id
            """,
            {"session_player_id": session_player_id}
        ).fetchone()
        print("") # add logging

        if row is not None:
            return True
        return False


def session_exists(session_id: str):
    """
    Checks if the session record has is_settled = false meaning there is still players in the session.
    Returns a bool.
    """
    with closing(create_connection(DB_NAME)) as connection:
        row = connection.execute(
            f"""
            select
                SessionId
            from
                {SESSION_TABLE_NAME}
            where
                1 = 1
                and IsSettled = 0
                and SessionId = :session_id
            """,
            {"session_id": session_id}
            ).fetchone()
        print("") # add logging
        
        if row is not None:
            return True
        return False


def get_session_info(host_player_id: str): # i think this should be done by the api file
    """
    """
    pass


def get_session_player_info(player_id: str, session_id: str): # i think this should be done by the api file
    """
    """
    pass