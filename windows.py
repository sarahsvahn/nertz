import threading
import curses 
from card import Card
from enums import Status
import sys

MAX_PLAYERS = 6

class Windows():
    def __init__(self, stdscr):
        self.print_mutex = threading.Lock()
        
        stdscr.clear()
        curses.curs_set(1)
        curses.echo()
        stdscr.bkgd(' ', curses.color_pair(3))

        self.last_move = ""
        
        # colors 
        curses.can_change_color()
        curses.start_color()
        curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000) # redefine white
        curses.init_color(8, 500, 500, 500) # grey 
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE) 
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, 8, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)
        
        if self.init_windows(stdscr) == Status.FAILED_JOIN:
            sys.exit("Please make your terminal bigger and try again.")
    
    def init_windows(self, stdscr):
        height, width = stdscr.getmaxyx()
        min_height = max(11 + 3 * MAX_PLAYERS, 19)
        min_width = 64 # 30 for each window + the borders
        if height < min_height or width < min_width: 
            return Status.FAILED_JOIN
        input_height = 3
        output_height = height - input_height * 2
        self.hand_win = curses.newwin(output_height, int(width / 2), 0, 0)
        self.community_win = curses.newwin(output_height, int(width / 2), 0, int(width / 2))
        self.input_win = curses.newwin(input_height, width, output_height + 3, 0)
        self.error_win = curses.newwin(input_height, width, output_height, 0)

        self.hand_win.bkgd(' ', curses.color_pair(3))
        self.community_win.bkgd(' ', curses.color_pair(3))
        self.input_win.bkgd(' ', curses.color_pair(3))
        self.error_win.bkgd(' ', curses.color_pair(3))

        with self.print_mutex:
            self.input_win.border()
            self.input_win.refresh()

            self.community_win.border()
            self.community_win.refresh()

            self.hand_win.border()
            self.hand_win.refresh()

            self.error_win.border()
            self.error_win.addstr(1, 1, "", curses.color_pair(4))
            self.error_win.refresh()  
                        
    def write(self, window, str, y, x):
        window.clear()
        window.border()
        if str == "> " or "HAND" in str or str == "COMMUNITY SECTION":
            window.addstr(y, x, str, curses.color_pair(4))
        else: 
            window.addstr(y, x, str)
        with self.print_mutex:
            window.refresh()
        
    def input_write(self, str, y = 1, x = 1):
        self.write(self.input_win, str, y, x)
    
    def error_write(self, str, y = 1, x = 1):
        self.write(self.error_win, str, y, x)

    @classmethod
    def read(cls, window):
        return window.getstr().decode("utf-8")

    def input_read(self):
        return Windows.read(self.input_win)
    
    def clear_and_refresh(self, window):
        window.clear()
        window.border()
        with self.print_mutex: 
            window.refresh()

    def input_refresh(self):
        self.clear_and_refresh(self.input_win)

    def hand_refresh(self):
        self.clear_and_refresh(self.hand_win)

    def community_refresh(self):
        self.clear_and_refresh(self.community_win)

    def error_refresh(self): 
        self.clear_and_refresh(self.error_win)

    def print_board(self, hand, name):
        self.hand_win.clear()
        self.hand_win.border()

        self.hand_win.addstr(1, 1, f"{name}'s HAND", curses.color_pair(4))
        Windows.print_cards(3, 1, [hand.top_nertz()], "nertz", self.hand_win)
        self.hand_win.addstr(4, 1, f"         {hand.count_nertz()}")
        Windows.print_cards(6, 1, hand.get_wp(0).get_cards(), "wp1", self.hand_win)
        Windows.print_cards(7, 1, hand.get_wp(1).get_cards(), "wp2", self.hand_win)
        Windows.print_cards(8, 1, hand.get_wp(2).get_cards(), "wp3", self.hand_win)
        Windows.print_cards(9, 1, hand.get_wp(3).get_cards(), "wp4", self.hand_win)
        Windows.print_cards(11, 1, hand.get_top3(), "draw pile", self.hand_win)

        with self.print_mutex:
            self.hand_win.refresh()         

    @classmethod
    def print_cards(cls, y, x, cards, pile_name, window):
        if pile_name == "nertz" or pile_name == "draw pile": 
            window.addstr(y, x, f"{pile_name}:  [")
            running_len = len(pile_name) + 4
        else: 
            window.addstr(y, x, f"{pile_name}:    [")
            running_len = len(pile_name) + 6
        for i, card in enumerate(cards):
            if card.get_value() != 0:
                if i == len(cards) - 1:
                    window.addstr(y, x + running_len, f"{card}", curses.color_pair(card.get_color().value + 1))
                    running_len += len(card.stringify())
                else:
                    window.addstr(y, x + running_len, f"{card}, ", curses.color_pair(card.get_color().value + 1))
                    running_len += len(card.stringify()) + 2
        if pile_name == "draw pile":
            window.addstr(y + 1, x + len(pile_name + ":  ["), f"^")
        window.addstr(y, x + running_len, "]")

    @classmethod
    def print_cp_cards(cls, y, x, cards, pile_names, window):
        real_cards = []
        running_len = 0

        for card in cards:
            real_cards.append(Card.card_with_name(card))

        for i in range(len(real_cards)):
            window.addstr(y, x + running_len, f"[ {real_cards[i]} ]", curses.color_pair(real_cards[i].get_color().value + 1))
            window.addstr(y + 1, x + running_len + 2, f"{pile_names[i]}")
            running_len += len(real_cards[i].stringify()) + 4

    def print_cs(self, board, nertz_changed):
        self.community_win.clear()
        self.community_win.addstr(1, 1, board[0][0], curses.color_pair(4))
        # self.community_win.addstr(2, 1, board[1][0], curses.color_pair(5))
        if not nertz_changed:
            self.last_move = board[1][0]
        self.community_win.addstr(2, 1, self.last_move, curses.color_pair(5))

        for i in range(0, len(board[3:]), 2):
            Windows.print_cp_cards(i + 4, 1, board[i + 3], board[i + 4], self.community_win)

        self.community_win.addstr(len(board) + 2, 1, board[2][0], curses.color_pair(5))
        self.community_win.border()
        
        with self.print_mutex:  
            self.community_win.refresh()
            self.input_win.refresh()
    
    def print_scores(self, scores, name):
        self.community_win.clear()
        self.community_win.border()
        for i, player in enumerate(scores):
            self.community_win.addstr(i + 1, 1, f"{player}: {scores[player][0]} + {scores[player][1]} = {scores[player][0] + scores[player][1]}")
        self.community_win.addstr(len(scores) + 2, 1, f"{name} got nertz!", curses.color_pair(5))
        with self.print_mutex: 
            self.community_win.refresh()
        