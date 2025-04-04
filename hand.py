from working_pile import WorkingPile
from card import Card
from draw_pile import DrawPile
from working_pile import WorkingPile
from enums import Suit

class Hand():
    def __init__(self): 
        deck = Hand.generate_deck()
        self.working_piles = [WorkingPile(deck[0]), WorkingPile(deck[1]),
                              WorkingPile(deck[2]), WorkingPile(deck[3])]
        self.nertz_pile = deck[4:17]
        self.draw_pile = DrawPile(deck[17:])
        self.score = -26
    
    @staticmethod
    def generate_deck():
        deck = []
        for i in range(13):
            for j in range(4):
                deck.append(Card(Suit(j).name, i))
        return deck 
    
    def shuffle(self):
        self.draw_pile.shuffle_cards()

    def draw(self): 
        return self.draw_pile.draw_three()

    def top_nertz(self):
        return self.nertz_pile[-1]
    
    def get_wp(self, idx): 
        return self.working_piles[idx]
    
    def get_top3(self): 
        return self.draw_pile.get_top_three()

    # def get_draw_pile(self):
    #     return self.draw_pile
