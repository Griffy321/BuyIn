from contextlib import closing

from buyin.data.config import create_connection
from buyin.tools import logger
from buyin.features.sessions.session import Session
from buyin.features.sessions.session_player import SessionPlayer
from datetime import datetime


_RESOURCE = "SessionData"

# both tables live in one file so SessionPlayers.SessionId can reference Sessions. Schema: buyin/data/schemas/sessions.sql
DB_NAME = "BuyInSession.db"
SESSION_TABLE_NAME = "Sessions"
SESSION_PLAYER_TABLE_NAME = "SessionPlayers"


def session_exists(session_id: str) -> bool:
    """
    Checks if the session record has is_settled = false meaning there is still players in the session.
    Returns a bool.
    """
    with closing(create_connection(DB_NAME)) as connection:
        try:
            row = connection.execute(
                f"""
                select
                    SessionId
                from
                    {SESSION_TABLE_NAME}
                where
                    1 = 1
                    and IsSettled = False
                    and SessionId = :session_id
                """,
                {"session_id": session_id}
                ).fetchone()
            logger.info(body="Checked if session is active", resource=_RESOURCE, attributes={"sessionId": session_id, "found": row is not None})

            return row is not None
        except Exception as e:
            logger.error(body="Failed to read player", resource=_RESOURCE, attributes={"sessionId": session_id, "found": row is not None}, exception=e)
            raise


def session_player_exists(session_player_id: str) -> bool:
    """
    Checks if the session player record has is_settled = false meaning they are still in play and 'exist' in a session. 
    Returns a bool.
    """
    with closing(create_connection(DB_NAME)) as connection:
        try:
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
            logger.info(body="Checked if session player is active", resource=_RESOURCE, attributes={"sessionPlayerId": session_player_id, "found": row is not None})

            return row is not None
        except Exception as e:
            logger.error(body="Failed to read player", resource=_RESOURCE, attributes={"sessionPlayerId": session_player_id, "found": row is not None}, exception=e)
            raise


def get_session_info(session_id: str):
    """
    Gets all the info needed to build a session object.
    Returns the session object.
    """
    try:
        with closing(create_connection(DB_NAME)) as connection:
            row = connection.execute(
                f"""
                select 
                    SessionId,
                    HostPlayerId,
                    InitializedAt,
                    IsSettled,
                    EndedAt
                from 
                    {SESSION_TABLE_NAME}
                where 
                    1 = 1
                    and SessionId = :SessionId
                """, 
                {"SessionId": session_id}).fetchone()

            if row is not None:
                session = Session(row[0])
                session.host_player = str(row[1])
                session.initialized_at = datetime.fromisoformat(row[2])
                session.is_settled = bool(row[3])
                session.ended_at = datetime.fromisoformat(row[4])
                return session
            print("")
            return None
    except Exception as e:
        print("")
        raise


def get_session_player_info(session_player_id: str):
    """
    Gets all the info needed to build a session player object.
    Returns the session player object.
    """
    try:
        with closing(create_connection(DB_NAME)) as connection: 
            row = connection.execute(
                    f"""
                    select 
                        SessionPlayerId
                        SessionId
                        PlayerId
                        Buyin
                        JoinedAt
                        Status
                        IsSettled
                        CashOut
                        LeftAt
                    from 
                        {SESSION_TABLE_NAME}
                    where
                        1 = 1
                        and SessionPlayerId = :SessionPlayerId
                    """,
                    {"SessionPlayerId": session_player_id}
                    ).fetchone()
            if row is not None:
                session_player = SessionPlayer(row[2], row[1], row[3], int(row[0]))
                session_player.joined_at = datetime.fromisoformat(row[4])
                session_player.is_settled = bool(row[6])
                session_player.cash_out = int(row[7])
                session_player.left_at = datetime.fromisoformat(row[8])
                return session_player
            print("")
            return None
    except Exception as e:
        print("")
        raise


def make_session(player_id: str):
    """
    
    """
    pass


def make_session_player(session_id: str, player_id: str):
    """
    
    """
    pass