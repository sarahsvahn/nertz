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

# TODO function contracts and file headers 
# TODO asciii cards suit emojis
# TODO community section starts

class Client():
    def __init__(self, stdscr):
        self.sio = socketio.Client()
        self.cp_move_done = threading.Event()
        self.server_url = "http://localhost:5000"
        self.hand = Hand()
        self.windows = Windows(stdscr)
        self.event = threading.Event()
        self.query = None
        self.thread = None
        self.can_shuffle = False

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
    
    def print_scores(self, scores, name):
        ''' 
        Parameters: scores
        Purpose: Prints all player's scores to window
        Effects: Prints to the community window
        Returns: None
        ''' 
        self.windows.print_scores(scores, name)

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
        self.event.set()
        self.thread = None

    def setup_handlers(self):
        ''' 
        Parameters: None
        Purpose: Sets up all handler functions that communicate with server
        Effects: None
        Returns: None
        ''' 
        @self.sio.on("get_scores")
        def send_score(data):
            ''' 
            Parameters: None
            Purpose: Sends player's score to server my_score function
            Effects: None
            Returns: None
            ''' 
            self.sio.emit("my_score", {"score": self.hand.get_score(), "name": self.hand.get_name(), "nertz": data.get("nertz")})

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
            if Status[data.get("status")] == Status.SUCCESS:
                remove_location = data.get("origin")
                self.hand.remove_from_origin(Origin[remove_location])
                self.can_shuffle = False
            else: 
                self.windows.error_write("Move failed. RIPPPPP that sucks.")
                self.windows.error_refresh()

            self.cp_move_done.set()

        @self.sio.on("reset")
        def reset(data): 
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
            self.sio.emit("player_rejoin")
            
        @self.sio.on("game_over")
        def game_over(data): 
            scores = data.get("scores")
            Client.print_scores(scores, data.get("nertz"))
            winner = min(scores, key=scores.get)
            self.windows.community_write(f"{winner} is the winner!", len(scores) + 1, 1)
            self.windows.community_refresh()

        @self.sio.on("cs_updated")
        def update_cs(data):
            board = data.get("board")
            nertz_updated = data.get("nertz")
            self.windows.print_cs(board, nertz_updated)


        @self.sio.on("allow_shuffle")
        def allow_shuffle():
            self.can_shuffle = True
            self.windows.print_board(self.hand, self.hand.get_name(), self.can_shuffle)

        @self.sio.on("start_game")
        def query_loop(): 
            self.windows.error_write("Game started, make a move!")
            curses.echo()

            # self.windows.community_refresh()
            self.windows.input_refresh()
            self.windows.print_board(self.hand, self.hand.get_name(), self.can_shuffle)

            self.windows.input_write("> ")
            self.query = self.windows.input_read().lower()
            
            while self.query != None: 
                self.sio.emit("test", {"parameter": "Starting loop"})
                self.sio.emit("test", {"parameter": f"Query: {self.query}"})
                self.windows.error_refresh()
                if len(self.query) == 0: 
                    self.windows.error_write("Usage: m <card> <pile> | m <ace> cp | d | s | nertz")
                else: 
                    self.query = self.query.split()
                    if self.query[0] == 'm' and len(self.query) == 3:
                        if Client.validate_card(self.query[1]) == Status.INVALID_CARD:
                            self.windows.error_write("Invalid card")
                        else:
                            if "cp" in self.query[2]:
                                origin = self.hand.find_og_location(Card.card_with_name(self.query[1]), "CP")
                                if origin != Origin.NOT_FOUND:
                                    self.cp_move_done.clear()
                                    self.sio.emit("cp_move", {'card': self.query[1], 'pile': self.query[2], "name": self.hand.get_name(), "origin": origin.name})
                                    self.cp_move_done.wait()
                                    if origin == Origin.NERTZ: 
                                        self.sio.emit("update_nertz", {"name": self.hand.get_name(), "count": self.hand.count_nertz()})
                                else:
                                    self.windows.error_write("Invalid move")
                            elif "wp" in self.query[2]: 
                                result = self.hand.move_to_wp(self.query[1], self.query[2])
                                if result == Status.INVALID_MOVE: 
                                    self.windows.error_write("Invalid move")
                                else: 
                                    self.can_shuffle = False
                                    if result == Origin.NERTZ: 
                                        self.sio.emit("update_nertz", {"name": self.hand.get_name(), "count": self.hand.count_nertz()})
                            else: 
                                self.windows.error_write("Usage: m <card> <pile> | m <ace> cp | d | s | nertz")
                    elif self.query == ['d']: 
                        self.hand.draw()
                    elif self.query == ['s']:
                        if self.can_shuffle:
                            self.hand.shuffle()
                            self.can_shuffle = False
                        else: 
                            self.sio.emit("i_want_to_shuffle", {"name": self.hand.get_name()})
                        # TODO 
                    elif self.query == ['nertz']:
                        self.sio.emit("test", {"parameter": "You think you have nertz?"})
                        if self.hand.has_nertz():
                            self.sio.emit("has_nertz", {"nertz": self.hand.get_name()})
                        else: 
                            self.windows.error_write("Your nertz pile is not empty. Keep playing.")
                    else: 
                        self.windows.error_write("Usage: m <card> <pile> | m <ace> cp | d | s | nertz")

                self.windows.print_board(self.hand, self.hand.get_name(), self.can_shuffle)
                self.windows.input_write("> ")
                self.query = None
                self.thread = threading.Thread(target=self.input_thread, args=()).start()
                self.event.wait()
                self.event.clear()

            self.sio.emit("test", {"parameter": "After loop"})

    def connect(self):
        self.sio.connect(self.server_url)

def main(stdscr):
    client = Client(stdscr)
    client.connect()
    client.establish_player()

curses.wrapper(main)

if __name__ == "__main__":
    main()