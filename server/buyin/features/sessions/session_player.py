from datetime import datetime, timezone

from buyin.tools.helpers import is_blank
from buyin.tools.random_string import generate_uid


class SessionPlayer:
    """
    The purpose of this class is to hold the attributes of each player in the session, e.g. their buyins, when they joined (UTC), if they have cashed out etc.
    Each player when joining a session will have one of these instances created
    """

    def __init__(self, session_id: str, player_id: str, chips: dict[str, list[int]], buyin: int, session_player_id: str | None = None):
        if is_blank(session_player_id):
            self.session_player_id: str = generate_uid()
        else:
            self.session_player_id = session_player_id
        self.session_id: str = session_id
        self.player_id: str = player_id
        self.chips: dict[str, list[int]] = chips
        self.buyin: int = buyin
        self.joined_at: datetime | None = None
        self.status: str | None = None # want to try and show this in the top corner of the app like an "On Air" sign but with the users game status
        self.is_settled: bool = False
        self.cash_out: int | None = None
        self.left_at: datetime | None = None


    def set_joined_at(self) -> bool:
        if self.joined_at is None:
            self.joined_at = datetime.now(timezone.utc)
            return True
        return False


    def update_status(self):
        """Updates the players status in the session"""
        pass


    def set_cashed_out(self, amount: int) -> bool:
        if self.cash_out is None and not self.is_settled and self.left_at is None:
            self.cash_out = amount
            self.is_settled = True
            self.left_at = datetime.now(timezone.utc)
            return True
        return False
