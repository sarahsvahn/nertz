from community_section import CommunitySection
from card import Card
import threading

class Game(): 
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        self.scores = {} # dictionary of names to lists of size 2 [previous score, new score]
        self.community_section = CommunitySection(self.num_players)
        self.scores_count = 0
        self.mutex = threading.Lock()
        self.nertz_counts = {} # dictionary of names to nertz counts
    
    def cp_move(self, card_name, pile_name):
        card = Card(card_name[-1].upper(), int(card_name[:-1]))
        return self.community_section.add_to_pile(card, pile_name)
    
    def get_board(self, name = "", card = "", pile = ""):
        return self.community_section.get_board(name, card, self.nertz_counts, pile)
    
    def set_score(self, name, score):
        with self.mutex: 
            if name not in self.scores: 
                self.scores[name] = [0, 0]
            self.scores[name][0] += self.scores[name][1]
            self.scores[name][1] = score
            self.scores_count += 1
            if self.scores_count == self.num_players:
                self.scores_count = 0
                return True
            return False
    
    def get_scores(self):
        with self.mutex:
            return self.scores
        
    def update_nertz_count(self, name, count): 
        with self.mutex: 
            self.nertz_counts[name] = count
    
    def reset(self): 
        self.community_section.reset()

