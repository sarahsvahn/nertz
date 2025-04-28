# game.py
# Authors: Cliodhna Reidy, Sarah Svahn, Owen Thomas
# 
# This file contains the main logic for the game. The Game stores the player's 
# scores and initializes and adds to the CommunitySection 
# 

from community_section import CommunitySection
from card import Card
import threading

class Game(): 
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        self.scores = {} # dictionary of names to lists of size 2 
                         # [previous score, new score]
        self.community_section = CommunitySection(self.num_players)
        self.scores_count = 0
        self.mutex = threading.Lock()
        self.nertz_counts = {} # dictionary of names to nertz counts
    
    def cp_move(self, card_name, pile_name):
        ''' 
        Parameters: card_name - name of the card to move, pile_name - name of 
                    the pile to move the card to
        Purpose: Moves a card from the user's hand to the commnuity section
        Effects: If able, adds the card to the community section 
        Returns: The status of the move
        '''
        card = Card(card_name[-1].upper(), int(card_name[:-1]))
        return self.community_section.add_to_pile(card, pile_name)
    
    def get_board(self, name = "", card = "", pile = ""):
        ''' 
        Parameters: name - name of the user who made a move, card - name of 
                    the card that was moved, pile - name of the pile the card
                    was moved to
        Purpose: Creates a string of the current community section board
        Effects: None
        Returns: The string of the current board
        '''
        return self.community_section.get_board(name, card, self.nertz_counts, 
                                                pile)
    
    def set_score(self, name, score):
        ''' 
        Parameters: name - name of the user whose score to set, score - the 
                    user's new score
        Purpose: Updates the user's previous score by combining their old score
                 with the score from the last round, then sets the new score
                 to be their score from the most recent round
        Effects: None
        Returns: True once all users' scores have been updated, false otherwise
        '''
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
        ''' 
        Parameters: None
        Purpose: Get the scores dictionary
        Effects: None
        Returns: The scores dictionary
        '''
        with self.mutex:
            return self.scores
        
    def update_nertz_count(self, name, count): 
        ''' 
        Parameters: name - the name of the player whose nertz count needs to 
                    be updated, count - the new nertz count
        Purpose: Update a player's nertz count
        Effects: None
        Returns: None
        '''
        with self.mutex: 
            self.nertz_counts[name] = count
    
    def reset(self): 
        ''' 
        Parameters: None
        Purpose: Resets the community section after each round
        Effects: Erases the old piles and creates new fresh ones
        Returns: None
        '''
        self.community_section.reset()

