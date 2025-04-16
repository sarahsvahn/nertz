import threading
from enums import Status
from community_pile import CommunityPile

class CommunitySection():
    def __init__(self, num_players):
        self.piles = [0] * (4 * num_players)
        self.piles_count = 0
        self.count_mutex = threading.Lock()

    def start_new_pile(self, card):
        with self.count_mutex:
            idx = self.piles_count
            self.piles_count += 1
            self.piles[idx] = CommunityPile(card) # TODO update design doc to reflect this

    def add_to_pile(self, card, pile_name="new_pile"):
        if card.get_value() == 1:
            self.start_new_pile(card)
            return Status.SUCCESS
        else: 
            if pile_name[2:].isnumeric():
                pile_idx = int(pile_name[2:]) - 1
            else:
                return Status.INVALID_MOVE
            # if self.piles[pile_idx].get_top_card().next_cp(card): #TODO keep for higher concurrency?
            return self.piles[pile_idx].add_to_pile(card)
            # else:
            #     return Status.INVALID_MOVE

    def get_board(self, name, card, pile): # think about printing unupdated data, would have to lock whole CS
        top_cards = []
        pile_names = []
        piles_count = 0
        with self.count_mutex:
            piles_count = self.piles_count
        for i in range(piles_count):
            top_cards.append(self.piles[i].get_top_card())
            pile_names.append("cp" + str(i + 1))
        
        to_return = f"COMMUNITY SECTION\n{name} added {card} to {pile}\n"
        cp_string = f""
        for i in range(len(top_cards)):
            if i % 4 == 0:
                to_return += "[ "
                cp_string = "  "
            
            # to_print = top_cards[i].__repr__() #this gets an fstring
            to_print = top_cards[i].stringify()
            cp_string += pile_names[i]
            
            to_print += " "
            cp_string += " "
            if len(to_print) < 4:
                to_print += " "

            to_return += to_print

            if i % 4 == 3 or i == len(top_cards) - 1:
                to_return = to_return[:-1]
                to_return += "]\n" + cp_string + "\n\n"
            else:
                to_return += " "
                cp_string += " "
        
        return to_return