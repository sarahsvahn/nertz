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
players_joined = 0

app = Flask(__name__) # TODO why do we have this again
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")
mutex = threading.Lock()
@socketio.on('connect')
def handle_connect():
    print("A client connected!")
    
@socketio.on("player_join")
def join_game(data):
    print(data)
    with mutex:
        players.append((request.sid, data.get("name")))
        emit("game_joined")
        if len(players) == num_players:
            print("about to emit start")
            emit("start_game", broadcast=True)

@socketio.on("player_rejoin")
def rejoin_game(): 
    global players_joined
    print("player has rejoined")
    with mutex:
        players_joined += 1
    print("count: ", players_joined)
    with mutex:
        if players_joined == num_players:
            print("about to emit start again")
            emit("start_game", broadcast=True)
            players_joined = 0

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
def game_over(data): 
    print("HAS NERTZ")
    emit("get_scores", {"nertz": data.get("nertz")}, broadcast=True)

@socketio.on("test")
def test(data):
    print("In tester: " + data.get("parameter"))

@socketio.on("my_score")
def get_player_score(data):
    name = data.get("name")
    score = data.get("score")
    result = game.set_score(name, score)
    scores = game.get_scores()
    if result: # all scores updated
        if any(sum(pair) >= 100 for pair in scores.values()):
            print("GAME OVER")
            emit("game_over", {"scores": scores, "nertz": data.get("nertz")}, broadcast=True)
        else: 
            print("reset")
            emit("reset", {"scores": scores, "nertz": data.get("nertz")}, broadcast=True)
            game.reset()
    print(name, " ", score)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)