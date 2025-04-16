# working_pile.py
# Authors: Cliodhna Reidy, Sarah Svahn, Owen Thomas
# 
# This file contains the WorkingPile class which represents one working 
# pile as a list of Cards. There are four instances of the WorkingPile in
# the Hand class. Working piles may be added to from any other piles in a
# Hand. Cards must appear in decreasing order with alternating colors
# (black/red).
#

from enums import Status
from card import Card

class WorkingPile(): 
    def __init__(self, card):
        self.cards = [card]


    def get_cards(self): 
        ''' 
        Parameters: None
        Purpose: Gets top card of the workingPile
        Effects: None
        Returns: Top card of workingPile
        ''' 
        return self.cards


    def remove_top_card(self): 
        ''' 
        Parameters: None
        Purpose: Removes top card from workingPile
        Effects: Removes top card from workingPile
        Returns: Top card from working pile, or Status.EMPTY
        Note: Move must be validated before calling
        ''' 
        if len(self.cards) >= 1:
            return self.cards.pop()
        else:
            return Status.EMPTY
    

    def remove_cards(self, card):
        ''' 
        Parameters: card - Card where remove begins
        Purpose: Removes at least one card from a workingPile
        Effects: Removes a set of cards from workingPile
        Returns: List of Cards that were removed
        Note: Move must be validated before calling
        ''' 
        if card not in self.cards:
            return Status.INVALID_MOVE
        idx = self.cards.index(card)
        removed = self.cards[idx:]
        self.cards = self.cards[:idx]
        return removed
    

    def put_cards(self, cards:list[Card]):
        ''' 
        Parameters: cards - list of Cards to remove
        Purpose: 
        Effects: None
        Returns: 
        ''' 
        if len(self.cards) == 0:
            self.cards = cards
            return Status.SUCCESS
        top = self.cards[-1]
        if top.next_wp(cards[0]):
            self.cards += cards
            return Status.SUCCESS
        return Status.INVALID_MOVE
    

    def get_top_card(self):
        if len(self.cards) == 0:
            return Card("S", 0) # empty card 
        return self.cards[-1]
    

    def in_pile(self, card):
        return card in self.cards
        
        
    def __repr__(self):
        return f"{self.cards}"