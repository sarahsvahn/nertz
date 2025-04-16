from hand import Hand
import threading
import socketio
from enums import Status, Origin
from card import Card
import curses 
from windows import Windows
import sys

# TODO make name a member variable of Hand, with a getter and a setter func - done, not tested

# TODO starting the next game doesn't work 
# TODO shuffle
# TODO alert player when the draw deck is turned over 
# TODO indicate which card you are allowed to take from top3 and wps visually
# TODO say who got nertz
# TODO put everything in client.py in a class


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

        self.setup_handlers()
    
    @classmethod
    def validate_card(cls, card_name):
        print(card_name)
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
        self.windows.input_write("Welcome to Nertz! Enter your name: ")
        name = self.windows.input_read()
        self.hand.set_name(name)
        self.windows.input_refresh()
        self.sio.emit("player_join", {"name": name})
        self.sio.wait()
    
    def print_scores(self, scores):
        self.windows.print_scores(scores)

    # thread function
    def input_thread(self): 
        self.query = self.windows.input_read().lower()
        self.event.set()
        self.thread = None

    def setup_handlers(self):
        @self.sio.on("get_scores")
        def send_score(data):
            self.sio.emit("my_score", {"score": self.hand.get_score(), "name": self.hand.get_name()})

        @self.sio.on("game_joined")
        def handle_game_joined(data):
            self.sio.wait()

        @self.sio.on("cp_move_result")
        def cp_move_result(data):
            if Status[data.get("status")] == Status.SUCCESS:
                remove_location = data.get("origin")
                self.hand.remove_from_origin(Origin[remove_location])
            else: 
                self.windows.error_write(1, 1, "Move failed. RIPPPPP that sucks.")
                self.windows.error_refresh()

            self.cp_move_done.set()

            # self.thread = self.cp_move_done.set()

        @self.sio.on("reset")
        def reset(data): 
            self.event.set()

            scores = data.get("scores")
            self.print_scores(scores)
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
            Client.print_scores(scores)
            winner = min(scores, key=scores.get)
            self.windows.community_write(f"{winner} is the winner!", len(scores) + 1, 1)
            self.windows.community_refresh()

        @self.sio.on("cs_updated")
        def update_cs(data):
            board = data.get("board")
            self.windows.print_cs(board)

        @self.sio.on("start_game")
        def query_loop(): 
            curses.echo()

            self.windows.community_refresh()
            self.windows.input_refresh()
            self.windows.print_board(self.hand, self.hand.get_name())

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
                            self.windows.error_write("Invalid move")
                        else:
                            if "cp" in self.query[2]:
                                origin = self.hand.find_og_location(Card.card_with_name(self.query[1]), "CP")
                                if origin != Origin.NOT_FOUND:
                                    self.cp_move_done.clear()
                                    self.sio.emit("cp_move", {'card': self.query[1], 'pile': self.query[2], "name": self.hand.get_name(), "origin": origin.name})
                                    self.cp_move_done.wait()
                                else:
                                    self.windows.error_write("Invalid move")
                            elif "wp" in qself.self.uery[2]: 
                                result = self.hand.move_to_wp(self.query[1], self.query[2])
                                if result == Status.INVALID_MOVE: 
                                    self.windows.error_write("Invalid move")
                            else: 
                                self.windows.error_write("Usage: m <card> <pile> | m <ace> cp | d | s | nertz")
                    elif self.query == ['d']: 
                        self.hand.draw()
                    elif self.query == ['s']:
                        self.hand.shuffle()
                        # TODO 
                    elif self.query == ['nertz']:
                        self.sio.emit("test", {"parameter": "You think you have nertz?"})
                        if self.hand.has_nertz():
                            self.sio.emit("has_nertz")
                        else: 
                            self.windows.error_write("Your nertz pile is not empty. Keep playing.")
                    else: 
                        self.windows.error_write("Usage: m <card> <pile> | m <ace> cp | d | s | nertz")

                self.windows.print_board(self.hand, self.hand.get_name())
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