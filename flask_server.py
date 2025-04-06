from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from game import Game
import threading

app = Flask(__name__)
num_players = int(input("Number of players: "))
game = Game(num_players)
mutex = threading.Lock()
players = []

app = Flask(__name__)
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

# @app.route('/message', methods=['POST'])
# def receive_message():
#     global player_count
#     data = request.json
#     print("Received:", data)

#     # {"message": "player_join" }
#     # {"message": "move", "card": "[Card]"}

#     message = data.get("message")

#     return jsonify({"reply": reply})
#     # data = request.json
#     # print("Received:", data)
#     # response = {"reply": f"Echo: {data['message']}"}
#     # return jsonify(response)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)