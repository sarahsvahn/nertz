from community_section import CommunitySection
from card import Card
import threading

class Game(): 
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        # self.scores = []
        self.scores = {}
        self.community_section = CommunitySection(self.num_players)
        self.scores_count = 0
        self.mutex = threading.Lock()

    def start_game(self, num_players):
        Game.set_member_variables(num_players)
    
    def cp_move(self, card_name, pile_name):
        card = Card(card_name[-1].upper(), int(card_name[:-1]))
        return self.community_section.add_to_pile(card, pile_name)
    
    def get_board(self, name, card, pile):
        return self.community_section.get_board(name, card, pile)
    
    def set_score(self, name, score):
        with self.mutex: 
            if name not in self.scores: 
                self.scores[name] = 0
            self.scores[name] += score
            self.scores_count += 1
            if self.scores_count == self.num_players:
                self.scores_count = 0
                return True
            return False
    
    def get_scores(self):
        return self.scores
    
    def reset(self): 
        self.community_section.reset()

