from enums import Status

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
        if card not in self.card:
            return Status.INVALID_MOVE
        index = self.cards.index(card)
        removed = self.cards[index:]
        self.cards = self.cards[:index]
        return removed
    
    def put_card(self, card):
        if len(self.cards) == 0:
            self.cards = [card]
            return Status.SUCCESS
        top = self.cards[-1]
        if top.color != card.color and (top.value - 1) == card.value:
            self.cards.append(card)
            return Status.SUCCESS
        return Status.INVALID_MOVE
    
    