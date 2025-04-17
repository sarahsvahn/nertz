from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from game import Game
import threading
from enums import Status

class Server(): 
    def __init__(self, num_players):
        self.num_players = num_players
        self.game = Game(num_players)
        self.mutex = threading.Lock()
        self.players = []
        self.players_joined = 0
        self.mutex = threading.Lock()

        app = Flask(__name__) 
        app.config["SECRET_KEY"] = ""
        self.socketio = SocketIO(app, cors_allowed_origins="*")

        self.setup_handlers()

        self.socketio.run(app, host='0.0.0.0', port=5000)
    
    def setup_handlers(self):   
        @self.socketio.on('connect')
        def handle_connect():
            print("A client connected!")
            
        @self.socketio.on("player_join")
        def join_game(data):
            print(data)
            name = data.get("name")
            with self.mutex:
                self.players.append((request.sid, name))
                self.game.update_nertz_count(name, 13)
                emit("game_joined")
                if len(self.players) == self.num_players:
                    print("about to emit start")
                    emit("start_game", broadcast=True)

        @self.socketio.on("player_rejoin")
        def rejoin_game(): 
            global players_joined
            print("player has rejoined")
            with self.mutex:
                players_joined += 1
            print("count: ", players_joined)
            with self.mutex:
                if players_joined == self.num_players:
                    print("about to emit start again")
                    emit("start_game", broadcast=True)
                    players_joined = 0

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
            print("In tester: " + data.get("parameter"))

        @self.socketio.on("my_score")
        def get_player_score(data):
            name = data.get("name")
            score = data.get("score")
            result = self.game.set_score(name, score)
            scores = self.game.get_scores()
            if result: # all scores updated
                if any(sum(pair) >= 100 for pair in scores.values()):
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

def main(): 
    n = int(input("Number of players: "))
    Server(n)

if __name__ == '__main__':
    main()