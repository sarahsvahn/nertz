# card.py
# Authors: Cliodhna Reidy, Sarah Svahn, Owen Thomas
# 
# This file contains the Card class which represents a playing card, which has a
# suit, value, and color. Two cards are equal if they have the same value and 
# suit

from enums import Color, Suit

class Card(): 
    def __init__(self, suit, value:int): 
        ''' 
        Parameters: suit - enum, value - int
        Purpose: Creates a new Card from its suit and value 
        Effects: None
        Returns: Card
        ''' 
        self.suit = Suit[suit]
        self.value = value
        if self.suit == Suit.D or self.suit == Suit.H:
            self.color = Color.RED
        else: 
            self.color = Color.BLACK

    @classmethod
    def card_with_name(cls, name): 
        ''' 
        Parameters: name - string of card
        Purpose: Creates a new Card from a string {value}{suit}
        Effects: None
        Returns: Card
        ''' 
        return cls(name[-1].upper(), int(name[:-1]))

    def stringify(self):
        ''' 
        Parameters: None
        Purpose: Converts card into a string of value and name
        Effects: None
        Returns: String representation of card 
        ''' 
        return str(self.value) + self.suit.name
     
    def get_color(self):
        ''' 
        Parameters: None
        Purpose: Gets card's color
        Effects: None
        Returns: Color (enum)
        ''' 
        return self.color
    
    def get_suit(self): 
        ''' 
        Parameters: None
        Purpose: Gets card's suit
        Effects: None
        Returns: Suit (enum)
        ''' 
        return self.suit
    
    def get_value(self):
        ''' 
        Parameters: None
        Purpose: Gets card's value
        Effects: None
        Returns: Value (int)
        ''' 
        return int(self.value)

    def __eq__(self, card):
        ''' 
        Parameters: card to compare 
        Purpose: Compares this card for equality to the parameter card, cards 
            are equal if they have the same suit and value 
        Effects: Overwrites the equality function 
        Returns: Boolean - says whether the cards are equal
        ''' 
        return (
            self.suit == card.get_suit()
            and int(self.value) == int(card.get_value())
        )
    
    def next_wp(self, card):
        ''' 
        Parameters: card - potential next card on a working pile 
        Purpose: Decides whether the parameter card can be placed on top of this
            card in a working pile 
        Effects: None
        Returns: Boolean - says whether this card is a valid next card for a 
            working pile 
        ''' 
        return (
            self.value == card.get_value() + 1 
            and self.color != card.get_color()
        )

    def next_cp(self, card):
        ''' 
        Parameters: card - potential next card on a community pile 
        Purpose: Decides whether the parameter card can be placed on top of this
            card in a community pile 
        Effects: None
        Returns: Boolean - says whether this card is a valid next card for a 
            community pile 
        ''' 
        return (
            self.value == card.get_value() - 1 and self.suit == card.get_suit()
        )
    
    def __repr__(self):
        ''' 
        Parameters: None
        Purpose: Defines the representation (for printing) of a card as its 
            value and suit ascii symbol
        Effects: Overwrites the repr function
        Returns: String representation of card 
        ''' 
        val = str(self.value).replace("11", "J")
        val = val.replace("12", "Q")
        val = val.replace("13", "K")
        if int(self.value) == 1:
            val = "A"

        if self.suit == Suit.H:
            symb = "\u2764"
        elif self.suit == Suit.D:
            symb = "\u2666"
        elif self.suit == Suit.S:
            symb = "\u2660"
        else: # C
            symb = "\u2663"
        return f"{val}{symb}"
