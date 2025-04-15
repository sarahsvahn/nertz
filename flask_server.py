from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from game import Game
import threading
from enums import Status

app = Flask(__name__)
num_players = int(input("Number of players: "))
game = Game(num_players)
mutex = threading.Lock()
players = []

app = Flask(__name__) # TODO why do we have this again
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print("A client connected!")
    

@socketio.on("player_join")
def join_game(data):
    print(data)
    with mutex:
        players.append((request.sid, data.get("name")))
        emit("game_joined", {"name": data.get("name")})
        if len(players) == num_players:
            print("about to emit start")
            emit("start_game", broadcast=True)

# @socketio.on("start_game")
# def start_game(data):
#     print(data)

@socketio.on("cp_move")
def cp_move(data):
    print(data)
    card = data.get("card")
    pile = data.get("pile")
    name = data.get("name")
    result = game.cp_move(card, pile)
    emit("cp_move_result", {"status": result.name, "card": card, "origin": data.get("origin")})
    if result == Status.SUCCESS: 
        print(game.get_board(name, card, pile))
        emit("cs_updated", {"board": game.get_board(name, card, pile)}, broadcast=True)

@socketio.on("has_nertz")
def game_over(): 
    print("HAS NERTZ")
    emit("get_scores", {}, broadcast=True)

@socketio.on("my_score")
def get_player_score(data):
    name = data.get("name")
    score = data.get("score")
    game.set_score(name, score)
    print(name, " ", score)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)