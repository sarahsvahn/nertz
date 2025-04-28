# flask_server.py
# Authors: Cliodhna Reidy, Sarah Svahn, Owen Thomas
# 
# This file contains the Server class which handles the main functionality of 
# the flask server. It communicates directly with 1 or more client to play the
# game. 
# 

from flask import Flask, request
from flask_socketio import SocketIO, emit
from game import Game
import threading
from enums import Status
import sys

NERTZ_LEN = 13

class Server(): 
    def __init__(self, num_players, score):
        self.num_players = num_players
        self.winning_score = score
        self.game = Game(num_players)
        self.mutex = threading.Lock()
        self.players = []
        self.players_joined = 0
        self.shuffle_count = set()
        self.shuffle_mutex = threading.Lock()

        app = Flask(__name__) 
        app.config["SECRET_KEY"] = ""
        self.socketio = SocketIO(app, cors_allowed_origins="*")

        self.setup_handlers()

        self.socketio.run(app, host='0.0.0.0', port=8000)
    
    def setup_handlers(self):   
        @self.socketio.on("connect")
        def handle_connect():
            print("A client connected!")

        @self.socketio.on("disconnect")
        def handle_disconnect():
            with self.mutex:
                self.num_players -= 1
            print("A player has disconnected")
            
        @self.socketio.on("player_join")
        def join_game(data):
            print(data)
            name = data.get("name")
            with self.mutex:
                self.players.append((request.sid, name))
                # self.game.update_nertz_count(name, 13) # TODO fix for shorter/longer nertz pile
                self.game.update_nertz_count(name, NERTZ_LEN)
                emit("game_joined")
                if len(self.players) == self.num_players:
                    print("about to emit start")
                    emit("start_game", broadcast=True)
                    # emit("cs_updated", {"board": self.game.get_board(), "nertz": True}, broadcast=True)

        @self.socketio.on("player_rejoin")
        def rejoin_game(data): 
            print("player has rejoined")
            with self.mutex:
                self.players_joined += 1
            self.game.update_nertz_count(data.get("name"), 13)
            print("count: ", self.players_joined)
            with self.mutex:
                if self.players_joined == self.num_players:
                    print("about to emit start again")
                    emit("start_game", broadcast=True)
                    # emit("cs_updated", {"board": self.game.get_board(), "nertz": True}, broadcast=True)
                    self.players_joined = 0

        @self.socketio.on("update_my_cs")        
        def update():
            board = self.game.get_board()
            board[1][0] = ""
            emit("cs_updated", {"board": board, "nertz": False}, broadcast=True)
        
        @self.socketio.on("cp_move")
        def cp_move(data):
            print(data)
            card = data.get("card")
            pile = data.get("pile")
            name = data.get("name")
            result = self.game.cp_move(card, pile)
            emit("cp_move_result", {"status": result.name, "card": card, "origin": data.get("origin")})
            if result == Status.SUCCESS: 
                print(self.game.get_board(name, card, pile))
                emit("cs_updated", {"board": self.game.get_board(name, card, pile), "nertz": False}, broadcast=True)

        @self.socketio.on("has_nertz")
        def game_over(data): 
            print("self. NERTZ")
            emit("get_scores", {"nertz": data.get("nertz")}, broadcast=True)

        @self.socketio.on("test")
        def test(data):
            print("In tester: " + str(data.get("parameter")))

        @self.socketio.on("my_score")
        def get_player_score(data):
            name = data.get("name")
            score = data.get("score")
            result = self.game.set_score(name, score)
            scores = self.game.get_scores()
            if result: # all scores updated
                if any(sum(pair) >= self.winning_score for pair in scores.values()):
                    print("GAME OVER")
                    emit("game_over", {"scores": scores, "nertz": data.get("nertz")}, broadcast=True)
                else: 
                    print("reset")
                    emit("reset", {"scores": scores, "nertz": data.get("nertz")}, broadcast=True)
                    self.game.reset()
            print(name, " ", score)

        @self.socketio.on("update_nertz")
        def update_nertz(data): 
            name = data.get("name")
            count = data.get("count")
            self.game.update_nertz_count(name, count)
            emit("cs_updated", {"board": self.game.get_board(), "nertz": True}, broadcast=True)

        @self.socketio.on("i_want_to_shuffle")
        def someone_wants_to_shuffle(data):
            print("SOMEONE WANTS TO shuffle")
            with self.shuffle_mutex:
                self.shuffle_count.add(data.get("name"))
                if len(self.shuffle_count) == self.num_players:
                    emit("allow_shuffle", broadcast=True)
                    self.shuffle_count = set()

def main(args): 
    if len(args) != 2 and len(args) != 3: 
        print("Usage: server.py <num_players> [final_score]")
        sys.exit()
    n = int(args[1])
    if n < 1: 
        print("Number of players must be greater than 0.")
        sys.exit()
    score = 100
    if len(args) == 3: 
        score = int(args[2])
        if score <= 0:
            print("Final score must be greater than 0.")
            sys.exit()
    Server(n, score)

if __name__ == '__main__':
    main(sys.argv)