from community_section import CommunitySection
from card import Card

class Game(): 
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        self.scores = []
        self.community_section = CommunitySection(self.num_players)

    # def initialize_game(self):
    #     self.community_section = 

    def set_member_variables(self, num_players):
        self.num_players = num_players
        self.players = [0] * num_players
        self.scores = [0] * num_players

    def start_game(self, num_players):
        Game.set_member_variables(num_players)
    
    def cp_move(self, card_name, pile_name):
        print(card_name)
        card = Card(card_name[-1].upper(), int(card_name[:-1]))
        return self.community_section.add_to_pile(card, pile_name)
    
    def get_board(self):
        return self.community_section.get_board()

