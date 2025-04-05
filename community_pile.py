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
        if self.get_top_card().next_cp(card):
            self.cards.append(card)
            return Status.SUCCESS
        else:
            return Status.INVALID_MOVE