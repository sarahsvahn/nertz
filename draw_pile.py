import random

class DrawPile(): 

    def __init__(self, cards):
        self.cards = cards
        self.idx = len(cards) - 1

    def getCard(self):
        return self.cards[self.idx]

    def drawThree(self):
        # [1, 2, 3, 4, 5]
        # would want to return [3, 4, 5]
        # idx is 5
        # [1, 2]
        # start_idx -1 -> 0
        # check if self.idx 
        if self.idx == 0:
            # start over 
        start_idx = self.idx - 2
        if start_idx < 0:
            start_idx = 0
        return self.cards[start_idx:self.idx]

    def takeCard(self): 
        card = self.cards[self.idx]
        self.cards.remove(card)
        return card


    def shuffle(self): 
        random.shuffle(self.cards)