from working_pile import WorkingPile
from card import Card
from draw_pile import DrawPile
from working_pile import WorkingPile
from enums import Suit, Status, Origin
import random

class Hand():
    def __init__(self): 
        self.reset_hand()

    def reset_hand(self):
        deck = Hand.generate_deck()
        self.working_piles = [WorkingPile(deck[0]), WorkingPile(deck[1]),
                              WorkingPile(deck[2]), WorkingPile(deck[3])]
        self.nertz_pile = deck[4:17] #TODO uncomment this line
        # self.nertz_pile = [Card("D", "1")] #TODO remove this line
        self.draw_pile = DrawPile(deck[17:])
        self.score = -26
    
    @staticmethod
    def generate_deck():
        deck = []
        for i in range(1, 14):
            for j in range(4):
                deck.append(Card(Suit(j).name, i))
        # random.shuffle(deck) #TODO Add back in when ready
        return deck 
    
    def shuffle(self):
        self.draw_pile.shuffle_cards()

    def draw(self): 
        return self.draw_pile.draw_three()
    
    def get_score(self): 
        return self.score

    def top_nertz(self):
        if len(self.nertz_pile) == 0: 
            return Card("S", "0")
        return self.nertz_pile[-1]
    
    def get_wp(self, idx): 
        return self.working_piles[idx]
    
    def get_top3(self): 
        return self.draw_pile.get_top_three()
    
    def find_og_location(self, card, pile):
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
    
    def move_to_wp(self, card_name, pile): # TODO refactor this function to use find_og_location
        print(card_name[-1].upper())
        card = Card(card_name[-1].upper(), card_name[:-1])
        valid = False
        if pile[:-1] == "wp":
            if pile[-1].isnumeric():
                if int(pile[-1]) <= 4:
                    top_wp_card = self.working_piles[int(pile[-1]) - 1].get_top_card()
                    if top_wp_card.get_value() == -1 or top_wp_card.next_wp(card): 
                        valid = True
        if not valid: 
            print("invalid move") # TODO print to a window 
            return Status.INVALID_MOVE
        # check that card is available to move
        new_cards = -1
        og_location = -1 # TODO why is this never used?? can we delete??
        if card == self.top_nertz(): 
            new_cards = [self.nertz_pile.pop()]
            self.score += 2
            og_location = Origin.NERTZ
        elif len(self.get_top3()) > 0 and card == self.get_top3()[0]: 
            new_cards = [self.draw_pile.take_card()]
            og_location = Origin.DRAW
        else:
            for index, working_pile in enumerate(self.working_piles): 
                if working_pile.in_pile(card):
                    new_cards = working_pile.remove_cards(card)
                    og_location = list(Origin)[index]
        if new_cards == -1: # can't find card
            return Status.INVALID_MOVE

        # move card 
        if pile[:-1] == "wp":
            working_pile = self.working_piles[int(pile[-1]) - 1]
            working_pile.put_cards(new_cards)

    def remove_from_origin(self, origin): 
        if origin == Origin.NERTZ:
            self.nertz_pile.pop(-1)
            self.score += 2
        elif origin == Origin.DRAW:
            self.draw_pile.take_card()
        else: 
            self.working_piles[origin.value].remove_top_card()
        self.score += 1 # a card was moved to CS

    def has_nertz(self):
        return len(self.nertz_pile) == 0

    def count_nertz(self):
        return len(self.nertz_pile)
