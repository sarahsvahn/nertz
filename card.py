from enums import Color, Suit

class Card(): 
    def __init__(self, suit, value:int): 
        # TODO handle invalid suit/values
        self.suit = Suit[suit]
        self.value = value
        if self.suit == Suit.D or self.suit == Suit.H:
            self.color = Color.RED
        else: 
            self.color = Color.BLACK

    @classmethod
    def card_with_name(cls, name): 
        return cls(name[-1].upper(), int(name[:-1]))

    def stringify(self):
        return str(self.value) + self.suit.name
     
    def get_color(self):
        return self.color
    
    def get_suit(self): 
        return self.suit
    
    def get_value(self):
        return int(self.value)

    def __eq__(self, card):
        return (self.suit == card.get_suit() and int(self.value) == int(card.get_value()))
    
    def next_wp(self, card):
        return self.value == card.get_value() + 1 and self.color != card.get_color()

    def next_cp(self, card):
        return self.value == card.get_value() - 1 and self.suit == card.get_suit()
    
    def __repr__(self):
        return f"{self.value}{self.suit.name}"