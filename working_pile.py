from enums import Status
from card import Card

class WorkingPile(): 
    def __init__(self, card):
        self.cards = [card]

    def get_cards(self): 
        return self.cards

    def remove_top_card(self): 
        if len(self.cards) >= 1:
            return self.cards.pop()
        else:
            return Status.EMPTY
    
    def remove_cards(self, card):
        # validation of proper move before func is called in parent class
        if card not in self.cards:
            return Status.INVALID_MOVE
        idx = self.cards.index(card)
        removed = self.cards[idx:]
        self.cards = self.cards[:idx]
        return removed
    
    def put_cards(self, cards:list[Card]):
        if len(self.cards) == 0:
            self.cards = cards
            return Status.SUCCESS
        top = self.cards[-1]
        if top.color != cards[0].color and (top.value - 1) == cards[0].value:
            self.cards += cards
            return Status.SUCCESS
        return Status.INVALID_MOVE
        