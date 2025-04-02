import random

class DrawPile(): 
    def __init__(self, cards):
        self.faceDown = cards # top of deck (idx len - 1) is back
        self.faceUp = []      # first card is front (idx 0)

    def getCard(self):
        return self.faceUp[0]

    def drawThree(self):
        if len(self.faceDown) == 0:
            self.faceDown = self.faceUp
            self.faceUp = []
        
        num_flipped = 0
        while len(self.faceDown) != 0 and num_flipped < 3: 
            self.faceUp.append(self.faceDown.pop())
            num_flipped += 1
        
        return self.getTopThree()
        
    def getTopThree(self):
        num_checked = 0
        top_three = []
        while len(self.faceDown) != 0 and num_checked < 3: 
            top_three.append(self.faceUp[num_checked])
        
        return top_three
    

    def takeCard(self): 
        ''' 
        Returns: Tuple of card removed and list of new top 3 cards
        Note:    Parent module verifies move before calling this      
        '''
        card = self.cards[self.idx]
        self.cards.remove(card)
        return (card, self.getTopThree())

    def shuffle(self): 
        random.shuffle(self.cards)