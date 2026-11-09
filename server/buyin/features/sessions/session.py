from buyin.features.sessions.session_player import SessionPlayer
from buyin.tools.random_string import generate_secure_uid
from datetime import datetime

class Session:
    """The object that all the players join to play a game"""

    def __init__(self, host_player, cash_in_play):
        self.session_id: str
        self.host_player: SessionPlayer = host_player
        self.session_players: list[SessionPlayer]
        self.cash_in_play: int = cash_in_play
        self.initialized_at: datetime
        self.ended_at: datetime


    def set_session_id(self):
        if self.session_id is None:
            self.session_id = generate_secure_uid()
            return True
        else:
            return False

    
    def add_player(self, player: SessionPlayer, buyin: int):
        self.session_players.append(player)
        self.cash_in_play += buyin
        joined = player.set_joined_at()
        if joined == True:
            print("") # add a log
        else:
            print("") # add a log


    def remove_player(self, session_player: SessionPlayer, cashout: int):
        index = 0
        for player in self.session_players:
            if player.player_id == session_player.player_id:
                self.cash_in_play -= cashout
                cashed_out = session_player.set_cashed_out(cashout)
                print("") # add a log
                self.session_players.pop(index)
                print("") # add a log
                if cashed_out == True:
                    return True
            else:
                index += 1
        return False


    def settle_session(self, player_cashouts: dict[SessionPlayer, int]):
        total_cashout = 0
        for cashout in player_cashouts.values():
            cashout += total_cashout
        if self.cash_in_play - total_cashout != 0:
            raise ValueError()

        if len(self.session_players) == len(player_cashouts):
            for player, out in player_cashouts.items():
                self.remove_player(player, out)
                print("") # add a log
            self.cash_in_play = 0
            print("") # add a log
            return True
        return False