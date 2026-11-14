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
    try:
        with closing(create_connection(DB_NAME)) as connection:
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
    except Exception as exception:
        logger.error(body="Failed to check if session is active", resource=_RESOURCE, attributes={"sessionId": session_id}, exception=exception)
        raise


def session_player_exists(session_player_id: str) -> bool:
    """
    Checks if the session player record has is_settled = false meaning they are still in play and 'exist' in a session. 
    Returns a bool.
    """
    try:
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
            logger.info(body="Checked if session player is active", resource=_RESOURCE, attributes={"sessionPlayerId": session_player_id, "found": row is not None})

            return row is not None
    except Exception as exception:
        logger.error(body="Failed to check if session player is active", resource=_RESOURCE, attributes={"sessionPlayerId": session_player_id}, exception=exception)
        raise


def get_session_info(session_id: str) -> Session | None:
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
                session = Session(host_player_id=row[1], session_id=row[0])
                session.initialized_at = datetime.fromisoformat(row[2])
                session.is_settled = bool(row[3])
                # EndedAt is null until the session is settled, so only convert it when there's a value
                session.ended_at = datetime.fromisoformat(row[4]) if row[4] is not None else None
                logger.info(body="Session loaded", resource=_RESOURCE, attributes={"sessionId": session_id})
                return session
            logger.info(body="Session not found", resource=_RESOURCE, attributes={"sessionId": session_id})
            return None
    except Exception as exception:
        logger.error(body="Failed to load session", resource=_RESOURCE, attributes={"sessionId": session_id}, exception=exception)
        raise


def get_session_player_info(session_player_id: str) -> SessionPlayer | None:
    """
    Gets all the info needed to build a session player object.
    Returns the session player object.
    """
    try:
        with closing(create_connection(DB_NAME)) as connection: 
            row = connection.execute(
                    f"""
                    select
                        SessionPlayerId,
                        SessionId,
                        PlayerId,
                        Buyin,
                        JoinedAt,
                        Status,
                        IsSettled,
                        CashOut,
                        LeftAt
                    from
                        {SESSION_PLAYER_TABLE_NAME}
                    where
                        1 = 1
                        and SessionPlayerId = :SessionPlayerId
                    """,
                    {"SessionPlayerId": session_player_id}
                    ).fetchone()
            if row is not None:
                session_player = SessionPlayer(player_id=row[2], session_id=row[1], buyin=row[3], session_player_id=row[0])
                # JoinedAt, Status, CashOut and LeftAt can all be null, so only convert them when there's a value
                session_player.joined_at = datetime.fromisoformat(row[4]) if row[4] is not None else None
                session_player.status = row[5]
                session_player.is_settled = bool(row[6])
                session_player.cash_out = row[7]
                session_player.left_at = datetime.fromisoformat(row[8]) if row[8] is not None else None
                logger.info(body="Session player loaded", resource=_RESOURCE, attributes={"sessionPlayerId": session_player_id})
                return session_player
            logger.info(body="Session player not found", resource=_RESOURCE, attributes={"sessionPlayerId": session_player_id})
            return None
    except Exception as exception:
        logger.error(body="Failed to load session player", resource=_RESOURCE, attributes={"sessionPlayerId": session_player_id}, exception=exception)
        raise


def player_currently_in_session(player_id: str) -> bool:
    """
    Checks if the provided player_id is currently in a session.
    Returns a bool.
    """
    try:
        with closing(create_connection(DB_NAME)) as connection:
            row = connection.execute(
                f"""
                select 
                    PlayerId
                from 
                    {SESSION_PLAYER_TABLE_NAME}
                where 
                    1 = 1
                    and (LeftAt is null or IsSettled = 0)
                    and PlayerId = :PlayerId
                """,
                {"PlayerId": player_id}
                ).fetchone()
            logger.info(body="Checked if player is in an active session", resource=_RESOURCE, attributes={"playerId": player_id, "found": row is not None})
            if row is not None:
                return True
            return False
    except Exception as exception:
        logger.error(body="Failed to check if player is in an active session", resource=_RESOURCE, attributes={"playerId": player_id}, exception=exception)
        raise


def save_session(session: Session) -> Session | None:
    """
    Writes the session object built by the endpoint to the DB.
    Returns the session object.
    """
    try:
        with closing(create_connection(DB_NAME)) as connection:
            result = connection.execute(
                f"""
                insert into {SESSION_TABLE_NAME}(SessionId, HostPlayerId, InitializedAt)
                values(:SessionId, :HostPlayerId, :InitializedAt)
                """,
                {"SessionId": session.session_id, "HostPlayerId": session.host_player_id, "InitializedAt": session.initialized_at.isoformat()}
                )

            if result.rowcount == 1:
                logger.info(body="Session saved", resource=_RESOURCE, attributes={"sessionId": session.session_id, "hostPlayerId": session.host_player_id})
                return session
            logger.warn(body="Session insert didn't write a row", resource=_RESOURCE, attributes={"sessionId": session.session_id, "hostPlayerId": session.host_player_id, "rowCount": result.rowcount})
            return None

    except Exception as exception:
        logger.error(body="Failed to save session", resource=_RESOURCE, attributes={"sessionId": session.session_id, "hostPlayerId": session.host_player_id}, exception=exception)
        raise


def save_session_player(session_player: SessionPlayer) -> SessionPlayer | None:
    """
    Writes the session player object built by the endpoint to the DB.
    Returns the session player object.
    """
    try:
        with closing(create_connection(DB_NAME)) as connection:
            # IsSettled defaults to 0, and Status, CashOut and LeftAt stay null until the player's status changes or they cash out
            result = connection.execute(
                f"""
                insert into {SESSION_PLAYER_TABLE_NAME}(SessionPlayerId, SessionId, PlayerId, Buyin, JoinedAt)
                values(:SessionPlayerId, :SessionId, :PlayerId, :Buyin, :JoinedAt)
                """,
                {
                    "SessionPlayerId": session_player.session_player_id,
                    "SessionId": session_player.session_id,
                    "PlayerId": session_player.player_id,
                    "Buyin": session_player.buyin,
                    "JoinedAt": session_player.joined_at.isoformat(),
                }
                )

            if result.rowcount == 1:
                logger.info(body="Session player saved", resource=_RESOURCE, attributes={"sessionPlayerId": session_player.session_player_id, "sessionId": session_player.session_id, "playerId": session_player.player_id, "buyin": session_player.buyin})
                return session_player
            logger.warn(body="Session player insert didn't write a row", resource=_RESOURCE, attributes={"sessionId": session_player.session_id, "playerId": session_player.player_id, "rowCount": result.rowcount})
            return None

    except Exception as exception:
        logger.error(body="Failed to save session player", resource=_RESOURCE, attributes={"sessionId": session_player.session_id, "playerId": session_player.player_id}, exception=exception)
        raise


def end_session(session: Session) -> Session | None:
    """
    Marks the session as ended in the DB, using the ended_at set on the object by session.settle_session(...).
    Returns the session object, or None if it hasn't been settled in the call.
    """
    if session.ended_at is None:
        logger.warn(body="Tried to end a session that hasn't been settled", resource=_RESOURCE, attributes={"sessionId": session.session_id})
        return None

    try:
        with closing(create_connection(DB_NAME)) as connection:
            result = connection.execute(
                f"""
                update {SESSION_TABLE_NAME}
                set
                    IsSettled = 1,
                    EndedAt = :EndedAt
                where
                    1 = 1
                    and IsSettled = 0
                    and SessionId = :SessionId
                """,
                {"SessionId": session.session_id, "EndedAt": session.ended_at.isoformat()}
                )

            if result.rowcount == 1:
                logger.info(body="Session ended", resource=_RESOURCE, attributes={"sessionId": session.session_id})
                return session
            logger.warn(body="No active session to end", resource=_RESOURCE, attributes={"sessionId": session.session_id, "rowCount": result.rowcount})
            return None

    except Exception as exception:
        logger.error(body="Failed to end session", resource=_RESOURCE, attributes={"sessionId": session.session_id}, exception=exception)
        raise


def end_session_player(session_player: SessionPlayer) -> SessionPlayer | None:
    """
    Marks the session player as cashed out in the DB, using the cash_out and left_at set on the object by session_player.set_cashed_out(...).
    Returns the session player object, or None if they haven't cashed out in this call.
    """
    if session_player.left_at is None:
        logger.warn(body="Tried to end a session player who hasn't cashed out", resource=_RESOURCE, attributes={"sessionPlayerId": session_player.session_player_id})
        return None

    try:
        with closing(create_connection(DB_NAME)) as connection:
            result = connection.execute(
                f"""
                update {SESSION_PLAYER_TABLE_NAME}
                set
                    IsSettled = 1,
                    CashOut = :CashOut,
                    LeftAt = :LeftAt
                where
                    1 = 1
                    and IsSettled = 0
                    and SessionPlayerId = :SessionPlayerId
                """,
                {
                    "SessionPlayerId": session_player.session_player_id,
                    "CashOut": session_player.cash_out,
                    "LeftAt": session_player.left_at.isoformat(),
                }
                )

            if result.rowcount == 1:
                logger.info(body="Session player ended", resource=_RESOURCE, attributes={"sessionPlayerId": session_player.session_player_id, "sessionId": session_player.session_id, "cashOut": session_player.cash_out})
                return session_player
            logger.warn(body="No active session player to end", resource=_RESOURCE, attributes={"sessionPlayerId": session_player.session_player_id, "rowCount": result.rowcount})
            return None

    except Exception as exception:
        logger.error(body="Failed to end session player", resource=_RESOURCE, attributes={"sessionPlayerId": session_player.session_player_id}, exception=exception)
        raise