from community_section import CommunitySection

class Game(): 
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        self.scores = []

    def initialize_game(self):
        community_section = CommunitySection(self.num_players)

    def set_member_variables(self, num_players):
        self.num_players = num_players
        self.players = [0] * num_players
        self.scores = [0] * num_players

    def start_game(self, num_players):
        Game.set_member_variables(num_players)

