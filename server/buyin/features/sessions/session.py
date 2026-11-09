from datetime import datetime, timezone

from buyin.features.sessions.session_player import SessionPlayer
from buyin.tools import logger
from buyin.tools.helpers import is_blank
from buyin.tools.random_string import generate_secure_uid

_RESOURCE = "Session"


class Session:
    """The object that all the players join to play a game"""

    def __init__(self, session_id: str | None = None):
        if is_blank(session_id):
            self.session_id: str = generate_secure_uid()
        else:
            self.session_id = session_id
        self.host_player: SessionPlayer | None = None
        self.session_players: list[SessionPlayer] = []
        self.cash_in_play: int = 0
        self.initialized_at: datetime = datetime.now(timezone.utc)
        self.ended_at: datetime | None = None
        logger.info(body="Session created", resource=_RESOURCE, attributes={"sessionId": self.session_id})


    def find_player(self, player_id: str) -> SessionPlayer | None:
        for player in self.session_players:
            if player.player_id == player_id:
                return player
        return None


    def add_host(self, player: SessionPlayer) -> bool:
        if self.host_player is not None:
            logger.warn(body="Session already has a host", resource=_RESOURCE, attributes={"sessionId": self.session_id, "playerId": player.player_id})
            return False
        added = self.add_player(player)
        if added:
            self.host_player = player
            logger.info(body="Host added to session", resource=_RESOURCE, attributes={"sessionId": self.session_id, "playerId": player.player_id})
        return added


    def add_player(self, player: SessionPlayer) -> bool:
        if self.find_player(player.player_id) is not None:
            logger.warn(body="Player is already in the session", resource=_RESOURCE, attributes={"sessionId": self.session_id, "playerId": player.player_id})
            return False
        self.session_players.append(player)
        self.cash_in_play += player.buyin
        player.set_joined_at()
        logger.info(body="Player joined session", resource=_RESOURCE, attributes={"sessionId": self.session_id, "playerId": player.player_id, "buyin": player.buyin})
        return True


    def remove_player(self, player_id: str, cashout: int) -> bool:
        player = self.find_player(player_id)
        if player is None:
            logger.warn(body="Tried to remove a player who isn't in the session", resource=_RESOURCE, attributes={"sessionId": self.session_id, "playerId": player_id})
            return False
        if not player.set_cashed_out(cashout):
            logger.warn(body="Player has already cashed out", resource=_RESOURCE, attributes={"sessionId": self.session_id, "playerId": player_id})
            return False
        self.cash_in_play -= cashout
        self.session_players.remove(player)
        logger.info(body="Player cashed out of session", resource=_RESOURCE, attributes={"sessionId": self.session_id, "playerId": player_id, "cashout": cashout})
        return True


    def settle_session(self, player_cashouts: dict[str, int]) -> bool:
        """player_cashouts maps each player_id still in the session to the amount they're cashing out"""
        player_ids_in_session = {player.player_id for player in self.session_players}
        if player_ids_in_session != set(player_cashouts.keys()):
            logger.warn(body="Cashouts don't match the players in the session", resource=_RESOURCE, attributes={"sessionId": self.session_id})
            return False

        total_cashout = sum(player_cashouts.values())
        if total_cashout != self.cash_in_play:
            raise ValueError(f"Cashouts total {total_cashout} but there is {self.cash_in_play} in play")

        for player_id, cashout in player_cashouts.items():
            self.remove_player(player_id, cashout)
        self.ended_at = datetime.now(timezone.utc)
        logger.info(body="Session settled", resource=_RESOURCE, attributes={"sessionId": self.session_id, "totalCashout": total_cashout})
        return True
