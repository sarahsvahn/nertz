# community_section.py
# Authors: Cliodhna Reidy, Sarah Svahn, Owen Thomas
# 
# This file contains the CommunitySection class which represents the concurrent,
# multiplayer section of our game. It has a list of CommunityPiles and a lock
# protecting access to that list. 

import threading
from enums import Status
from community_pile import CommunityPile
from card import Card

class CommunitySection():
    def __init__(self, num_players):
        ''' 
        Parameters: num_players - int
        Purpose: Creates a new CommunitySection for num_players 
        Effects: None
        Returns: CommunitySection
        ''' 
        self.num_players = num_players
        self.piles = [0] * (4 * num_players)
        self.piles_count = 0
        self.count_mutex = threading.Lock()
    
    def reset(self):
        ''' 
        Parameters: None
        Purpose: Resets community section by clearing all piles 
        Effects: None
        Returns: None
        ''' 
        self.piles = [0] * (4 * self.num_players)
        self.piles_count = 0

    def add_to_pile(self, card, pile_name="new_pile"):
        if card.get_value() == 1:
            self.start_new_pile(card)
            return Status.SUCCESS
        else: 
            if pile_name[2:].isnumeric():
                pile_idx = int(pile_name[2:]) - 1
                with self.count_mutex:
                    if pile_idx >= self.piles_count:
                        return Status.INVALID_MOVE
            else:
                return Status.INVALID_MOVE
            return self.piles[pile_idx].add_to_pile(card)

    def start_new_pile(self, card):
        ''' 
        Parameters: card to add, pile (string) to add it to 
        Purpose: Adds a card to the community section, either to a pre-existing 
            pile or a new pile
        Effects: None
        Returns: Status (enum) - result of the move
        ''' 
        with self.count_mutex:
            idx = self.piles_count
            self.piles_count += 1
            self.piles[idx] = CommunityPile(card) 

    def get_board(self, name, card, nertz_count, pile): 
        ''' 
        Parameters: name (string) of player who made the most recent move
                    card (Card) added to community section 
                    nertz_count (int) dictionary of each player's count of nertz
                    pile (string) that the card was added to 
        Purpose: Builds a string representation of the community section 
            including the most recent move made, the top card of each community
            pile, and each player's nertz count
        Effects: None
        Returns: String representation of the community section 
        '''
        if card != "":
            card = Card.card_with_name(card).__repr__()
        to_return = [[f"COMMUNITY SECTION"], [f"{name} added {card} to {pile}\n"]]
        top_cards = []
        pile_names = []

        nertz_str = "Nertz Counts\n " # space added to be overwritten by border
        for player, count in nertz_count.items():
            nertz_str += str(player) + ": " + str(count) + ", "
        nertz_str = nertz_str[:-2]
        to_return.append([nertz_str])
        
        piles_count = 0
        with self.count_mutex:
            piles_count = self.piles_count
        for i in range(piles_count):
            top_cards.append(self.piles[i].get_top_card().stringify())
            pile_names.append("cp" + str(i + 1))
        
        curr_idx = 1 # why are we appendeing startign at 0 i think it should be 4? or maybe 1 because were off by 1
        for i in range(len(top_cards)):
            if i % 4 == 0:
                to_return.append([top_cards[i]])
                to_return.append([pile_names[i]])
                curr_idx += 2
            else:
                to_return[curr_idx].append(top_cards[i])
                to_return[curr_idx + 1].append(pile_names[i])

        return to_return