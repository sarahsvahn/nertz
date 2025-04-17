import threading
from enums import Status
from community_pile import CommunityPile

class CommunitySection():
    def __init__(self, num_players):
        self.num_players = num_players
        self.piles = [0] * (4 * num_players)
        self.piles_count = 0
        self.count_mutex = threading.Lock()
    
    def reset(self):
        self.piles = [0] * (4 * self.num_players)
        self.piles_count = 0

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

    def get_board(self, name, card, nertz_count, pile): 
        to_return = [[f"COMMUNITY SECTION"], [f"{name} added {card} to {pile}\n"]]
        top_cards = []
        pile_names = []

        nertz_str = "Nertz Counts\n "
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
        
        curr_idx = 0
        for i in range(len(top_cards)):
            if i % 4 == 0:
                to_return.append([top_cards[i]])
                to_return.append([pile_names[i]])
                curr_idx += 2
            else:
                to_return[curr_idx].append(top_cards[i])
                to_return[curr_idx + 1].append(pile_names[i])
        
        return to_return