from enums import Color, Suit

class Card(): 
    def __init__(self, suit, value): 
        self.suit = suit
        self.value = value
        if suit == Suit.DIAMONDS or suit == Suit.HEARTS:
            self.color = Color.RED
        else: 
            self.color = Color.BLACK
            
    def get_color(self):
        return self.color
    
    def get_suit(self): 
        return self.suit
    
    def get_value(self):
        return self.value
        
    # def print(self):
    #     print(f"{self.suit}{self.value}")

    def __repr__(self):
        return f"{self.value}{self.suit[0]}"