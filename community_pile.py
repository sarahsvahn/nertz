# community_pile.py
# Authors: Cliodhna Reidy, Sarah Svahn, Owen Thomas
# 
# This file contains the CommunityPile class which represents one pile in the 
# community section. A CommunityPile has a list of cards, a suit, and a mutex
# that protects adding to it. 

from enums import Suit, Status
import threading

class CommunityPile():
    def __init__(self, card):
        self.suit = card.get_suit()
        self.cards = [card]
        self.pile_lock = threading.Lock()

    def get_top_card(self):
        ''' 
        Parameters: None
        Purpose: Gets the top card of the community pile
        Effects: None
        Returns: The top card in the pile
        ''' 
        with self.pile_lock:
            return self.cards[-1]
    
    def get_top_card_non_atomic(self): 
        ''' 
        Parameters: None
        Purpose: Gets the top card of the community pile without the lock for 
                 internal use
        Effects: None
        Returns: The top card in the pile
        ''' 
        print("cards: ", self.cards[-1])
        return self.cards[-1]

    def add_to_pile(self, card):
        ''' 
        Parameters: card - the card to add to the pile
        Purpose: Adds a new card to the community section
        Effects: Updates the cards array
        Returns: A status of either SUCCESS if the user is able to add to the 
                 pile or INVALID_MOVE otherwise
        ''' 
        with self.pile_lock:
            if self.get_top_card_non_atomic().next_cp(card):
                self.cards.append(card)
                return Status.SUCCESS
            else:
                return Status.INVALID_MOVE
