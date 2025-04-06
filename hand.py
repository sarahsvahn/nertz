from working_pile import WorkingPile
from card import Card
from draw_pile import DrawPile
from working_pile import WorkingPile
from enums import Suit, Status, Origin
import random

class Hand():
    def __init__(self): 
        deck = Hand.generate_deck()
        # deck2 = [Card(Suit(0).name, 12), Card(Suit(1).name, 11), Card(Suit(3).name, 10), Card(Suit(2).name, 9)]
        # deck = deck2 + deck
        self.working_piles = [WorkingPile(deck[0]), WorkingPile(deck[1]),
                              WorkingPile(deck[2]), WorkingPile(deck[3])]
        self.nertz_pile = deck[4:17]
        self.draw_pile = DrawPile(deck[17:])
        self.score = -26
    
    @staticmethod
    def generate_deck():
        deck = []
        for i in range(1, 14):
            for j in range(4):
                deck.append(Card(Suit(j).name, i))
        random.shuffle(deck)
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
    
    def move_to_wp(self, card_name, pile):
        print(card_name[-1].upper())
        card = Card(card_name[-1].upper(), card_name[:-1])
        # check that move could be valid 
        valid = False
        if pile[:-1] == "wp":
            top_wp_card = self.working_piles[int(pile[-1]) - 1].get_top_card()
            if top_wp_card.get_value() == -1 or top_wp_card.next_wp(card): 
                valid = True
        # if pile[:-1] == "cp" TODO 
            #send message to community pile to inquire about valiidity, set `valid`
            # check that it's coming from the top of something (ie not a chunk from a wp)
        if not valid: 
            print("invalid move")
            return Status.INVALID_MOVE
        # check that card is available to move
        new_cards = -1
        og_location = -1
        if card == self.top_nertz(): 
            new_cards = [self.nertz_pile.pop()]
            og_location = Origin.NERTZ
        elif len(self.get_top3()) > 0 and card == self.get_top3()[0]: 
            new_cards = [self.draw_pile.take_card()]
            og_location = Origin.DRAW
        else:
            for index, working_pile in enumerate(self.working_piles): 
                if working_pile.in_pile(card):
                    new_cards = working_pile.remove_cards(card)
                    print(new_cards)
                    og_location = list(Origin)[index]
        if new_cards == -1: # can't find card
            return Status.INVALID_MOVE

        # move card 
        if pile[:-1] == "wp":
            working_pile = self.working_piles[int(pile[-1]) - 1]
            working_pile.put_cards(new_cards)
        # elif pile[:-1] == "cp" TODO 
            #send message to community pile to put cards 
