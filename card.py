from enums import Color, Suit

class Card(): 
    def __init__(self, suit, value:int): 
        self.suit = Suit[suit]
        self.value = value
        if self.suit == Suit.D or self.suit == Suit.H:
            self.color = Color.RED
        else: 
            self.color = Color.BLACK
            
    def get_color(self):
        return self.color
    
    def get_suit(self): 
        return self.suit
    
    def get_value(self):
        return int(self.value)

    def __eq__(self, card):
        # print("suit equality")
        # print(self.suit == card.get_suit())
        # print("value eq")
        # print(self.value == card.get_value())
        return (self.suit == card.get_suit() and int(self.value) == int(card.get_value()))

    # def card_equal(self, card):
    #     return self.value == card.get_value() and self.suit == card.get_suit()
    
    def next_wp(self, card):
        # print(self.value)
        # print(self.color)
        # print(card.get_value())
        # print(card.get_color())xw
        return self.value == card.get_value() + 1 and self.color != card.get_color()

    def next_cp(self, card):
        return self.value == card.get_value() - 1 and self.suit == card.get_suit()
    
    def __repr__(self):
        return f"{self.value}{self.suit.name}"