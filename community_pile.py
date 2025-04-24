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
        return self.cards[-1]
        
    def add_to_pile(self, card):
        with self.pile_lock:
            if self.get_top_card().next_cp(card):
                self.cards.append(card)
                return Status.SUCCESS
            else:
                return Status.INVALID_MOVE