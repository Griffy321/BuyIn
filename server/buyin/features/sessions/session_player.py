from buyin.tools import random_string
from datetime import datetime, timezone
from typing import Dict, List
from buyin.tools.random_string import generate_uid

class SessionPlayer:
    """
    The perpose of this class is to hold the attributes of each player in the session, e.g. their buyins, when they joined (UTC), if they have cashed out etc.
    Each player when joining a session will have one of these instances created
    """

    def __init__(self, session_id, player_id, chips, buyin, session_player_id = None):
        self.session_player_id: str
        self.session_id:str = session_id
        self.player_id: str = player_id
        self.chips: Dict[str, List[int]] = chips
        self.buyin: int = buyin
        self.joined_at: datetime
        self.status: str # want to try and show this in the top corner of the app like an "On Air" sign but with the users game status
        self.is_settled: bool
        self.cash_out: int
        self.left_at: datetime

    def set_session_player_id(self):
        if self.session_player_id is None:
            self.session_player_id = generate_uid()
            return True
        else:
            return False

    def set_joined_at(self, player_id: str) -> bool:
        if self.joined_at is None: 
            self.joined_at = datetime.now(timezone.utc)
            return True
        else:
            return False 


    def update_status(self, player_id):
        """Updates the players status in the session"""
        pass


    def set_cashed_out(self, player_id: str, amount: int) -> bool:
        if self.cash_out is None: 
            self.cash_out = amount
            self.is_settled = True
            return True
        else:
            return False 


    def set_left_at(self, player_id: str) -> bool:
        if self.left_at is None: 
            self.left_at = datetime.now(timezone.utc)
            return True
        else:
            return False 
