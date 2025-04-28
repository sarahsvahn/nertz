# client.py
# Authors: Cliodhna Reidy, Sarah Svahn, Owen Thomas
# 
# This file contains the client class and main functionality of client. Handles
# connection to server, and handles the query loop in which a player enters
# their moves. Communicates directly with server to play game.
# 

from hand import Hand
import threading
import socketio
from enums import Status, Origin
from card import Card
import curses 
from windows import Windows
import time
import sys

class Client():
    def __init__(self, stdscr, url):
        self.sio = socketio.Client()
        self.cp_move_done = threading.Event()
        self.server_url = url
        self.hand = Hand()
        self.windows = Windows(stdscr)
        self.event = threading.Event()
        self.query = None
        self.thread = None
        self.can_shuffle = False
        self.game_over = False

        self.setup_handlers()
    
    @classmethod
    def validate_card(cls, card_name):
        ''' 
        Parameters: card_name as a string
        Purpose: Validates that card_name is a valid card name
        Effects: None
        Returns: Status.INVALID_CARD or Status.SUCCESS
        ''' 
        if not card_name.isalnum(): 
            return Status.INVALID_CARD
        card_letter = card_name[-1]
        if card_letter.isalpha():
            if card_letter.upper() not in ["D", "H", "C", "S"]:
                return Status.INVALID_CARD
        else:
            return Status.INVALID_CARD
        if card_name[:-1].isnumeric():
            if int(card_name[:-1]) > 13 or int(card_name[:-1]) <= 0:
                return Status.INVALID_CARD
        return Status.SUCCESS     

    def establish_player(self):
        ''' 
        Parameters: None
        Purpose: Gets player name and connects to server
        Effects: Writes to input window, sets player's name in their Hand, 
                 emits to server that player has joined
        Returns: None
        ''' 
        self.windows.input_write("Welcome to Nertz! Enter your name: ")
        name = self.windows.input_read()
        self.hand.set_name(name)
        self.windows.input_refresh()
        self.sio.emit("player_join", {"name": name})
        self.sio.wait()
    
    def print_scores(self, scores, name, winner=None):
        ''' 
        Parameters: scores
        Purpose: Prints all player's scores to window
        Effects: Prints to the community window
        Returns: None
        ''' 
        self.windows.print_scores(scores, name, winner)

    def input_thread(self): 
        ''' 
        Parameters: None
        Purpose: Gets input from input window, once input is received, sets 
                 event
        Effects: Updates query, event, and thread
        Returns: None
        Note: Used as the threading function for thread
        ''' 
        self.query = self.windows.input_read().lower()
        self.modify_query()
        self.event.set()
        self.thread = None
    
    def modify_query(self):
        ''' 
        Parameters: None
        Purpose: Modifies player's query to fit card specifications
        Effects: Updates query
        Returns: None
        ''' 
        self.query = self.query.replace("a", "1")
        self.query = self.query.replace("j", "11")
        self.query = self.query.replace("q", "12")
        self.query = self.query.replace("k", "13")

    def setup_handlers(self):
        ''' 
        Parameters: None
        Purpose: Sets up all handler functions that communicate with server
        Effects: None
        Returns: None
        Note: All of these functions are called by the server
        ''' 
        @self.sio.on("get_scores")
        def send_score(data):
            ''' 
            Parameters: data - a dict with the key:
                               nertz - player's current number of cards in
                                       nertz pile
            Purpose: Sends player's info to server my_score function
            Effects: None
            Returns: None
            ''' 
            self.sio.emit("my_score", {"score": self.hand.get_score(),
                                       "name": self.hand.get_name(),
                                       "nertz": data.get("nertz")})

        @self.sio.on("game_joined")
        def handle_game_joined():
            ''' 
            Parameters: None
            Purpose: Allows player to wait for all players to join
            Effects: None
            Returns: None
            ''' 
            self.windows.error_write("Waiting for other players to join")
            self.windows.input_refresh()
            self.sio.wait()

        @self.sio.on("cp_move_result")
        def cp_move_result(data):
            ''' 
            Parameters: data - dict that containing the keys:
                               status - either SUCCESS or not
                               origin - where the card originally came from
            Purpose: Removes card from user's hand if the move is successful
            Effects: Prints to windows error if move is unsuccessful, removes 
                     card from hand if move is successful
            Returns: None
            ''' 
            if Status[data.get("status")] == Status.SUCCESS:
                remove_location = data.get("origin")
                self.hand.remove_from_origin(Origin[remove_location])
                self.can_shuffle = False
            else: 
                self.windows.error_write("Invalid Move")
                # TODO Print a different message for a race condition
                # "Another user beat you to it. RIPPPPP that sucks"

            self.cp_move_done.set()

        @self.sio.on("reset")
        def reset(data): 
            ''' 
            Parameters: data - a dict that contains the keys:
                               scores - dictionary of player names to lists
                                        of size 2 [previous score, new score]
                               nertz - name of player who had nertz
            Purpose: Prints last round info to CS and waits for players to 
                     agree to next round
            Effects: Prints to CS window and input window, emits player_rejoin
            Returns: None
            ''' 
            self.event.set()

            scores = data.get("scores")
            self.print_scores(scores, data.get("nertz"))
            self.hand.reset_hand()

            self.windows.input_refresh()
            self.windows.hand_refresh()

            self.windows.input_write("Enter any key to start the next round: ")
            self.event.wait()
            self.event.clear()

            self.sio.emit("test", {"parameter": "entered key"})
            self.sio.emit("player_rejoin", {"name": self.hand.get_name()})
            
        @self.sio.on("game_over")
        def game_over(data):
            ''' 
            Parameters: data - a dict that contains the keys:
                               scores - dictionary of player names to lists
                                        of size 2 [previous score, new score]
                               nertz - name of player who had nertz
            Purpose: Finishes the game for all players
            Effects: Writes to CS and input windows, disconnects all users 
                     after 10 seconds
            Returns: None
            ''' 
            self.event.set()
            self.game_over = True

            scores = data.get("scores")
            winner = max(scores, key=scores.get)
            self.print_scores(scores, data.get("nertz"), winner)
            
            self.windows.input_write("Game over!")
            self.event.wait()

            self.thread = None
            self.query = None

            time.sleep(10)

            self.windows.end()
            self.sio.emit("disconnect")
            self.sio.disconnect()

        @self.sio.on("cs_updated")
        def update_cs(data):
            ''' 
            Parameters: data - a dict containing the keys:
                               board - current state of community section board
                               nertz - boolean whether nertz was updated or a 
                                       new card was added (T for nertz F for
                                       card)
            Purpose: Sends current board and nertz state to print
            Effects: Calls print_cs in Windows class
            Returns: None
            ''' 
            board = data.get("board")
            nertz_updated = data.get("nertz")
            self.windows.print_cs(board, nertz_updated)

        @self.sio.on("allow_shuffle")
        def allow_shuffle():
            ''' 
            Parameters: None
            Purpose: Allows a player to be able to shuffle
            Effects: Prints Hand board with can_shuffle boolean True
            Returns: None
            ''' 
            self.can_shuffle = True
            self.windows.print_board(self.hand, self.hand.get_name(),
                                     self.can_shuffle)

        @self.sio.on("start_game")
        def query_loop(): 
            ''' 
            Parameters: None
            Purpose: Runs the query loop for player input
            Effects: Prints to all windows
            Returns: None
            ''' 
            self.windows.error_write("Game started, make a move!")
            curses.echo()
            self.windows.community_refresh()
            self.sio.emit("update_my_cs")
            self.windows.input_refresh()
            self.windows.print_board(self.hand, self.hand.get_name(),
                                     self.can_shuffle)
            self.windows.input_write("> ")
            self.query = self.windows.input_read().lower()
            self.modify_query()
            
            while self.query != None: 
                self.windows.error_refresh()
                if not self.game_over:
                    self.event.clear()
                    self.handle_input()
                    
                self.windows.print_board(self.hand, self.hand.get_name(),
                                         self.can_shuffle)
                self.windows.input_write("> ")
                self.query = None
                self.thread = threading.Thread(target=self.input_thread,
                                               args=()).start()
                self.event.wait()
            
    def handle_input(self):
        ''' 
        Parameters: None
        Purpose: Handles user input from query loop
        Effects: Prints to error window if bad input
        Returns: None
        ''' 
        if len(self.query) == 0: 
            self.windows.error_write("Usage: m <card> <pile> | m <ace> cp | d"
                                     " | s | nertz")
        else: 
            self.query = self.query.split()
            if self.query[0] == 'm' and len(self.query) == 3:
                self.handle_move()
            elif self.query == ['d']: 
                self.hand.draw()
            elif self.query == ['s']:
                self.handle_shuffle()
            elif self.query == ['nertz']:
                self.handle_nertz()
            else: 
                self.windows.error_write("Usage: m <card> <pile> | m <ace> cp | d | s | nertz")

    def handle_move(self):
        ''' 
        Parameters: None
        Purpose: Handles move command from user
        Effects: Prints to error window if bad input, emits update_nertz to 
                 server if Nertz pile is decremented, emits cp_move if there 
                 is a move to a community pile
        Returns: None
        ''' 
        if Client.validate_card(self.query[1]) == Status.INVALID_CARD:
            self.windows.error_write("Invalid card")
        else:
            if "cp" in self.query[2]:
                new_card = Card.card_with_name(self.query[1])
                origin = self.hand.find_og_location(new_card, "CP")
                if origin != Origin.NOT_FOUND:
                    self.cp_move_done.clear()
                    self.sio.emit("cp_move", {"card": self.query[1],
                                              "pile": self.query[2],
                                              "name": self.hand.get_name(),
                                              "origin": origin.name})
                    self.cp_move_done.wait()
                    if origin == Origin.NERTZ: 
                        self.sio.emit("update_nertz",
                                      {"name": self.hand.get_name(),
                                       "count": self.hand.count_nertz()})
                else:
                    self.windows.error_write("Invalid move")
            elif "wp" in self.query[2]: 
                result = self.hand.move_to_wp(self.query[1], self.query[2])
                if result == Status.INVALID_MOVE: 
                    self.windows.error_write("Invalid move")
                else: 
                    self.can_shuffle = False
                    if result == Origin.NERTZ: 
                        self.sio.emit("update_nertz",
                                      {"name": self.hand.get_name(),
                                       "count": self.hand.count_nertz()})
            else: 
                self.windows.error_write("Usage: m <card> <pile> | m <ace> cp |"
                                         " d | s | nertz")

    def handle_shuffle(self):
        ''' 
        Parameters: None
        Purpose: Handles shuffle command from user
        Effects: emits i_want_to_shuffle with user's name if can_shuffle is 
                 False, otherwise shuffles hand and resets can_shuffle
        Returns: None
        ''' 
        if self.can_shuffle:
            self.hand.shuffle()
            self.can_shuffle = False
        else: 
            self.sio.emit("i_want_to_shuffle", {"name": self.hand.get_name()})
    
    def handle_nertz(self):
        ''' 
        Parameters: None
        Purpose: Handles nertz command from user
        Effects: Checks if Nertz is valid, if it is, emits has_nertz with user's
                 name
        Returns: None
        ''' 
        if self.hand.has_nertz():
            self.sio.emit("has_nertz", {"nertz": self.hand.get_name()})
        else: 
            self.windows.error_write("Your nertz pile is not empty. Keep playing.")

    def connect(self):
        ''' 
        Parameters: None
        Purpose: Allows client to connect to server
        Effects: Connects client to server url
        Returns: None
        ''' 
        self.sio.connect(self.server_url)

def main(stdscr):
    args = sys.argv
    url = "http://localhost:8080"
    if len(args) == 2: 
        url = args[1]
    client = Client(stdscr, url)
    client.connect()
    client.establish_player()

curses.wrapper(main)
