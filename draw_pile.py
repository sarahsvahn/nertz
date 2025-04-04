import random
from enums import Status

class DrawPile(): 
    def __init__(self, cards):
        self.faceDown = cards # top of deck (idx len - 1) is back
        self.faceUp = []      # first card is front (idx 0)

    def get_card(self):
        if len(self.faceUp) == 0:
            return Status.EMPTY
        return self.faceUp[0]

    def draw_three(self):
        if len(self.faceDown) == 0:
            self.faceDown = self.faceUp
            self.faceUp = []
        
        num_flipped = 0
        while len(self.faceDown) != 0 and num_flipped < 3: 
            self.faceUp.insert(0, self.faceDown.pop())
            num_flipped += 1
        
        return self.get_top_three()
        
    def get_top_three(self):
        num_checked = 0
        top_three = []
        while len(self.faceUp) != 0 and num_checked < 3: 
            top_three.append(self.faceUp[num_checked])
            num_checked += 1
        
        return top_three

    def take_card(self): 
        ''' 
        Returns: Tuple of card removed and list of new top 3 cards
        Note:    Parent module verifies move before calling this      
        '''
        if len(self.faceUp) == 0:
            return Status.EMPTY
        card = self.faceUp.pop(0)
        return (card, self.get_top_three())

    def shuffle_cards(self): 
        self.faceDown = self.faceDown + self.faceUp
        self.faceUp = []
        random.shuffle(self.faceDown)
        return self.draw_three()