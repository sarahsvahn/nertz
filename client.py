from hand import Hand
import threading
import socketio
from enums import Status, Origin
from card import Card
import curses 
from windows import Windows
import sys

# TODO starting the next game doesn't work 
# TODO shuffle
# TODO alert player when the draw deck is turned over 
# TODO indicate which card you are allowed to take from top3 and wps visually
# TODO make name a member variable of Hand, with a getter and a setter func
# TODO say who got nertz
# TODO put everything in client.py in a class

sio = socketio.Client()

cp_move_done = threading.Event()

server_url = "http://localhost:5000"

hand = Hand()
name = "" 

windows = None


event = threading.Event() # TODO not global
query = None # TODO not global 

def main(stdscr):
    global hand, windows
    windows = Windows(stdscr)
    sio.connect(server_url)
    establish_player()

def establish_player():
    global name, windows
    windows.input_write("Welcome to Nertz! Enter your name: ")
    name = windows.input_read()
    windows.input_refresh()
    sio.emit("player_join", {"name": name})
    sio.wait()

@sio.on("get_scores")
def send_score(data):
    global name, hand
    sio.emit("my_score", {"score": hand.get_score(), "name": name})

@sio.on("game_joined")
def handle_game_joined(data):
    sio.wait()

@sio.on("cp_move_result")
def cp_move_result(data):
    global hand
    if Status[data.get("status")] == Status.SUCCESS:
        remove_location = data.get("origin")
        hand.remove_from_origin(Origin[remove_location])
    else: 
        windows.error_write(1, 1, "Move failed. RIPPPPP that sucks.")
        windows.error_refresh()

    cp_move_done.set()


@sio.on("reset")
def reset(data): 
    global windows, event

    event.set()

    scores = data.get("scores")
    print_scores(scores)
    hand.reset_hand()

    windows.input_refresh()
    windows.hand_refresh()
    windows.input_write("Enter any key to start the next round: ")
    windows.input_read()
    sio.emit("player_rejoin")
           
@sio.on("game_over")
def game_over(data): 
    scores = data.get("scores")
    print_scores(scores)
    winner = min(scores, key=scores.get)
    windows.community_write(f"{winner} is the winner!", len(scores) + 1, 1)
    windows.community_refresh()

def print_scores(scores):
    global windows
    windows.print_scores(scores)

def input_thread(event): 
    global query
    query = windows.input_read().lower()
    event.set()

@sio.on("start_game")
def query_loop(): 
    global name, hand, windows, query 
    curses.echo()

    windows.community_refresh()
    windows.input_refresh()
    windows.print_board(hand, name)

    windows.input_write("> ")
    query = windows.input_read().lower()
    
    # try:
    while query != None: 
        sio.emit("test", {"parameter": "Starting loop"})
        windows.error_refresh()
        if len(query) == 0: 
            windows.error_write("Usage: m <card> <pile> | m <ace> cp | d | s | nertz")
        else: 
            query = query.split()
            if query[0] == 'm' and len(query) == 3:
                if validate_card(query[1]) == Status.INVALID_CARD:
                    windows.error_write("Invalid move")
                else:
                    if "cp" in query[2]:
                        origin = hand.find_og_location(Card.card_with_name(query[1]), "CP")
                        if origin != Origin.NOT_FOUND:
                            cp_move_done.clear()
                            sio.emit("cp_move", {'card': query[1], 'pile': query[2], "name": name, "origin": origin.name})
                            cp_move_done.wait()
                        else:
                            windows.error_write("Invalid move")
                    elif "wp" in query[2]: 
                        result = hand.move_to_wp(query[1], query[2])
                        if result == Status.INVALID_MOVE: 
                            windows.error_write("Invalid move")
                    else: 
                        windows.error_write("Usage: m <card> <pile> | m <ace> cp | d | s | nertz")
            elif query == ['d']: 
                hand.draw()
            elif query == ['s']:
                hand.shuffle()
                # TODO 
            elif query == ['nertz']:
                if hand.has_nertz():
                    sio.emit("has_nertz")
                else: 
                    windows.error_write("Your nertz pile is not empty. Keep playing.")
            else: 
                windows.error_write("Usage: m <card> <pile> | m <ace> cp | d | s | nertz")

        windows.print_board(hand, name)
        windows.input_write("> ")
        query = None
        threading.Thread(target=input_thread, args=(event,)).start()
        event.wait()
        event.clear()
            # query = windows.input_read().lower()
        # else:
        #     query = "exit"
    # except Terminate:
    sio.emit("test", {"parameter": "After loop"})
    #     signal.alarm(0)
    #     return
    



def validate_card(card_name):
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

@sio.on("cs_updated")
def update_cs(data):
    global windows
    board = data.get("board")
    windows.print_cs(board)

curses.wrapper(main)


if __name__ == "__main__":
    main()