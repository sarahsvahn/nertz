# draw_pile.py
# Authors: Cliodhna Reidy, Sarah Svahn, Owen Thomas
# 
# This file contains the DrawPile class which represents the pile of cards 
# that a player uses to draw from. The only instances of the DrawPile class 
# exist in the Hand class. The DrawPile has two piles of cards, faceUp and 
# faceDown to simulate actual gameplay.
#

import random
from enums import Status

class DrawPile(): 
    def __init__(self, cards):
        self.faceDown = cards # top of deck (idx len - 1) is back
        self.faceUp = []      # first card is front (idx 0)


    def get_card(self):
        ''' 
        Parameters: None
        Purpose: Gets the top card from the faceUp pile
        Effects: None
        Returns: Top card from faceUp pile, or Status.EMPTY
        ''' 
        if len(self.faceUp) == 0:
            return Status.EMPTY
        return self.faceUp[0]


    def draw_three(self):
        ''' 
        Parameters: None
        Purpose: Draws the top three cards from the faceDown pile
        Effects: Removes top three from faceDown and moves them to faceUp. 
                 Starts pile over if we have reached the end.
        Returns: List of top three cards
        ''' 
        if len(self.faceDown) == 0:
            self.faceDown = self.faceUp
            self.faceUp = []
        
        num_flipped = 0
        while len(self.faceDown) != 0 and num_flipped < 3: 
            self.faceUp.insert(0, self.faceDown.pop())
            num_flipped += 1
        
        return self.get_top_three() 
            

    def get_top_three(self):
        ''' 
        Parameters: None
        Purpose: Gets the top three cards in the faceUp deck
        Effects: None
        Returns: List of top three cards (may be less than three)
        ''' 
        num_checked = 0
        top_three = []
        while num_checked < len(self.faceUp) and num_checked < 3: 
            top_three.append(self.faceUp[num_checked])
            num_checked += 1
        return top_three


    def take_card(self): 
        ''' 
        Parameters: None
        Purpose: Removes a card from faceUp
        Effects: Removes the top card from faceUp
        Returns: Top card from faceUp or Status.EMPTY if faceUp is empty
        Note: Parent module must verify move before calling      
        '''
        if len(self.faceUp) == 0:
            return Status.EMPTY
        card = self.faceUp.pop(0)
        return (card) # TODO, used to be a tuple 


    def shuffle_cards(self): 
        ''' 
        Parameters: None
        Purpose: Shuffles the entire draw_pile
        Effects: Resets faceUp and faceDown and reorders the new pile, draws 
                 the top three cards
        Returns: Top three drawn cards 
        ''' 
        self.faceDown = self.faceDown + self.faceUp
        self.faceUp = []
        random.shuffle(self.faceDown)
        return self.draw_three()