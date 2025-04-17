# hand.py
# Authors: Cliodhna Reidy, Sarah Svahn, Owen Thomas
# 
# This file contains the hand class which represents an individual user's 
# playing cards. The cards are divided into four working piles, a 
# nertz pile, and a draw pile. Each player has a score which is updated
# as appropriate as cards as discarded/moved.
# 

from working_pile import WorkingPile
from card import Card
from draw_pile import DrawPile
from working_pile import WorkingPile
from enums import Suit, Status, Origin
import random

class Hand():
    def __init__(self): 
        self.reset_hand()
        self.name = ""

    def set_name(self, name): 
        self.name = name

    def get_name(self):
        return self.name

    def reset_hand(self):
        ''' 
        Parameters: None
        Purpose: Resets hand back to default (empty piles, new deck)
        Effects: Updates all Hand member variables back to default
        Returns: None
        ''' 
        deck = Hand.generate_deck()
        self.working_piles = [WorkingPile(deck[0]), WorkingPile(deck[1]),
                              WorkingPile(deck[2]), WorkingPile(deck[3])]
        self.nertz_pile = deck[4:17] #TODO uncomment this line
        # self.nertz_pile = [Card("D", "1")] #TODO remove this line
        self.draw_pile = DrawPile(deck[17:])
        self.score = -26
    
    @staticmethod
    def generate_deck():
        ''' 
        Parameters: None
        Purpose: Generates a full deck of cards
        Effects: None
        Returns: Shuffled deck of cards as a list of Cards
        ''' 
        deck = []
        for i in range(1, 14):
            for j in range(4):
                deck.append(Card(Suit(j).name, i))
        random.shuffle(deck) #TODO Add back in when ready
        return deck 
    
    def shuffle(self):
        ''' 
        Parameters: None
        Purpose: Shuffle a list
        Effects: Shuffles the draw_pile
        Returns: None
        ''' 
        self.draw_pile.shuffle_cards()

    def draw(self): 
        ''' 
        Parameters: None
        Purpose: Draws top three cards from draw_pile
        Effects: Modifies draw_pile
        Returns: List of 3 new top cards on draw_pile
        ''' 
        return self.draw_pile.draw_three()
    
    def get_top3(self): 
        ''' 
        Parameters: None
        Purpose: Gets top three cards from draw_pile
        Effects: None
        Returns: List of 3 top cards on draw_pile
        ''' 
        return self.draw_pile.get_top_three()
    
    def get_score(self): 
        ''' 
        Parameters: None
        Purpose: Gets score
        Effects: None
        Returns: Hand's score
        ''' 
        return self.score

    def top_nertz(self):
        ''' 
        Parameters: None
        Purpose: Gets top element from nertz_pile
        Effects: None
        Returns: Top element from nertz_pile, returns Card S0 if empty
        ''' 
        if len(self.nertz_pile) == 0: 
            return Card("S", "0")
        return self.nertz_pile[-1]

    def get_wp(self, idx): 
        ''' 
        Parameters: idx representing working pile index
        Purpose: Gets the working pile at a specifed index
        Effects: None
        Returns: Hand's working_pile at specified index
        ''' 
        return self.working_piles[idx]

    def find_og_location(self, card, pile):
        ''' 
        Parameters: card - original Card, pile - either string "WP" or "CP"
        Purpose: Find the original location of a card before moving
        Effects: None
        Returns: Hand's working_pile at specified index
        ''' 
        if card == self.top_nertz(): 
            return Origin.NERTZ
        elif len(self.get_top3()) > 0 and card == self.get_top3()[0]: 
            return Origin.DRAW
        else:
            for index, working_pile in enumerate(self.working_piles): 
                if pile == "WP" and working_pile.in_pile(card):
                    return list(Origin)[index]
                elif pile == "CP" and working_pile.get_top_card() == card:
                    return list(Origin)[index]
        return Origin.NOT_FOUND
    
    def validate_wp(self, pile):
        if pile[:-1] == "wp":
            if pile[-1].isnumeric():
                if int(pile[-1]) <= 4 and int(pile[-1]) > 0:
                    return True
        return False

    def move_to_wp(self, card_name, pile): 
        ''' 
        Parameters: card_name - string representing card, pile - string
                    representing working pile destination
        Purpose: Validates and executes a working pile move
        Effects: Moves card to specified working pile if move is valid
        Returns: Status.SUCCESS or Status.INVALID_MOVE
        ''' 
        card = Card.card_with_name(card_name)
        if self.validate_wp(pile):
            top_wp_card = self.working_piles[int(pile[-1]) - 1].get_top_card()
            if top_wp_card.get_value() != 0 and not top_wp_card.next_wp(card): 
                return Status.INVALID_MOVE
        
        new_cards = -1
        og_location = self.find_og_location(card, "WP")
        if og_location == Origin.NOT_FOUND:
            return Status.INVALID_MOVE
        elif og_location == Origin.NERTZ: 
            new_cards = [self.nertz_pile.pop()]
            self.score += 2
        elif og_location == Origin.DRAW: 
            new_cards = [self.draw_pile.take_card()]
        else: # must be working pile
            for working_pile in self.working_piles: 
                if working_pile.in_pile(card):
                    new_cards = working_pile.remove_cards(card)

        # actually move card 
        working_pile = self.working_piles[int(pile[-1]) - 1]
        working_pile.put_cards(new_cards)
        return og_location

    def remove_from_origin(self, origin): 
        ''' 
        Parameters: origin - an Origin enum
        Purpose: Removes the top card from a specified origin (to the
                 Community Section)
        Effects: Removes top card from specified Hand pile
        Returns: None
        ''' 
        if origin == Origin.NERTZ:
            self.nertz_pile.pop(-1)
            self.score += 2
        elif origin == Origin.DRAW:
            self.draw_pile.take_card()
        else: 
            self.working_piles[origin.value].remove_top_card()
        self.score += 1 # a card was moved to CS

    def has_nertz(self):
        ''' 
        Parameters: None
        Purpose: Checks if Hand has nertz
        Effects: None
        Returns: Whether nertz pile is empty
        ''' 
        return len(self.nertz_pile) == 0

    def count_nertz(self):
        ''' 
        Parameters: None
        Purpose: Checks how many cards left in nertz pile
        Effects: None
        Returns: Number of cards in nertz pile
        ''' 
        return len(self.nertz_pile)
