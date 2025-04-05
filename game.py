from community_section import CommunitySection

class Game(): 
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = [0] * num_players
        self.scores = [0] * num_players

    def initialize_game(self):
        community_section = CommunitySection(self.num_players)
