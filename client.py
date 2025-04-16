from hand import Hand
import threading
import socketio
from enums import Status, Origin
from card import Card
import curses 

# TODO add to cp double digits - DONE
# TODO extra line between lines of cps - DONE

# TODO starting the next game doesn't work 
# TODO shuffle
# TODO make ncurses class, and others
# TODO make sure terminal is big enough
# TODO colors 
# TODO alert player when the draw deck is turned over 
# TODO indicate which card you are allowed to take from top3 and wps 
# TODO mouse is moved to cp after someone updates that, shouldn't happen 
# TODO make name a member variable of Hand, with a getter and a setter func
# TODO say who got nertz

sio = socketio.Client()

cp_move_done = threading.Event()

server_url = "http://localhost:5000"

hand = Hand()
name = "" 

print_mutex = threading.Lock()
input_win = None
community_win = None 
hand_win = None
error_win = None

continue_loop = True #TODO this needs a mutex 

def main(stdscr):
    global input_win, community_win, hand_win, error_win, hand
    
    stdscr.clear()
    curses.curs_set(1) # show cursor ? 
    curses.echo()
    height, width = stdscr.getmaxyx()
    input_height = 3
    output_height = height - input_height * 2
    hand_win = curses.newwin(output_height, int(width / 2), 0, 0)
    community_win = curses.newwin(output_height, int(width / 2), 0, int(width / 2))
    input_win = curses.newwin(input_height, width, output_height + 3, 0)
    error_win = curses.newwin(input_height, width, output_height, 0)

    with print_mutex:
        input_win.border()
        input_win.refresh()

        community_win.border()
        community_win.refresh()

        hand_win.border()
        hand_win.refresh()

        error_win.border()
        error_win.addstr(1, 1, "Errors:")
        error_win.refresh()

    sio.connect(server_url)

    establish_player()

def establish_player():
    global name, input_win, hand
    input_win.addstr(1, 1, "Welcome to Nertz! Enter your name: ")
    name = input_win.getstr().decode("utf-8")
    input_win.clear()
    input_win.border()
    with print_mutex:
        input_win.refresh()
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
    global error_win, hand
    if Status[data.get("status")] == Status.SUCCESS:
        remove_location = data.get("origin")
        card = Card.card_with_name(data.get("card")) 
        hand.remove_from_origin(Origin[remove_location])
    else: 
        error_win.addstr(1, 1, "Move failed. RIPPPPP that sucks.")
        with print_mutex:
            error_win.refresh()

    cp_move_done.set()

@sio.on("cs_updated")
def update_cs(data):
    global community_win, print_mutex

    community_win.clear()
    community_win.border()
    
    board = data.get("board").split("\n")
    for i, line in enumerate(board): 
        community_win.addstr(i + 1, 1, line)
    
    with print_mutex:  
        community_win.refresh()

@sio.on("reset")
def reset(data): 
    global continue_loop
    continue_loop = False
    scores = data.get("scores")
    print_scores(scores)
    hand.reset_hand()
    
    input_win.clear()
    input_win.border()
    hand_win.clear()
    hand_win.border()
    input_win.addstr(1, 1, "Enter any key to start the next round: ")
    with print_mutex:
        input_win.refresh() 
        hand_win.refresh()
    input_win.getstr().decode("utf-8").lower()
    sio.emit("player_rejoin")
           
@sio.on("game_over")
def game_over(data): 
    global continue_loop
    continue_loop = False
    scores = data.get("scores")
    print_scores(scores)
    winner = min(scores, key=scores.get)
    community_win.clear()
    community_win.border()
    community_win.addstr(len(scores) + 1, 1, f"{winner} is the winner!")
    with print_mutex: 
        community_win.refresh()

def print_scores(scores):
    global community_win, print_mutex
    community_win.clear()
    community_win.border()
    for i, player in enumerate(scores):
        community_win.addstr(i + 1, 1, f"{player}: {scores[player]}")
    with print_mutex: 
        community_win.refresh()

@sio.on("start_game")
def query_loop(): 
    global error_win, input_win, name, hand, print_mutex, continue_loop

    continue_loop = True

    community_win.clear()
    community_win.border()
    with print_mutex: 
        community_win.refresh()
        
    print_board(print_mutex)
    input_win.clear()
    input_win.border()
    input_win.addstr(1, 1, "> ")

    with print_mutex:
        input_win.refresh()
    query = input_win.getstr().decode("utf-8").lower()
    while query != "exit" and continue_loop: 
        error_win.clear()
        error_win.border()
        with print_mutex:
            error_win.refresh()
        if len(query) == 0: 
            error_win.addstr(1, 1, "Usage: m <card> <pile> | m <ace> cp | d | s | nertz")
        else: 
            query = query.split()
            if query[0] == 'm' and len(query) == 3:
                if validate_card(query[1]) == Status.INVALID_CARD:
                    error_win.addstr(1, 1, "Invalid Card")
                else:
                    if "cp" in query[2]:
                        origin = hand.find_og_location(Card.card_with_name(query[1]), "CP")
                        if origin != Origin.NOT_FOUND:
                            cp_move_done.clear()
                            sio.emit("cp_move", {'card': query[1], 'pile': query[2], "name": name, "origin": origin.name})
                            cp_move_done.wait()
                        else:
                            error_win.addstr(1, 1, "Invalid move")
                    elif "wp" in query[2]: 
                        hand.move_to_wp(query[1], query[2])
                    else: 
                        error_win.addstr(1, 1, "Usage: m <card> <pile> | m <ace> cp | d | s | nertz")
            elif query == ['d']: 
                hand.draw()
            elif query == ['s']:
                hand.shuffle()
                # TODO 
            elif query == ['nertz']:
                if hand.has_nertz():
                    sio.emit("has_nertz")
                else: 
                    error_win.addstr(1, 1, "Your nertz pile is not empty. Keep playing.")
            else: 
                error_win.addstr(1, 1, "Usage: m <card> <pile> | m <ace> cp | d | s | nertz")
                # error_win.refresh()

        print_board(print_mutex)  
        with print_mutex:
            error_win.refresh()
        input_win.clear()
        input_win.border()
        input_win.addstr(1, 1, "> ")
        with print_mutex:
            input_win.refresh()         

        query = input_win.getstr().decode("utf-8").lower()
    
    sio.emit("test")

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

def print_board(print_mutex):
    global hand_win, hand

    hand_win.clear()
    hand_win.border()

    hand_win.addstr(1, 1, f"{name}'s HAND:")
    hand_win.addstr(3, 1, f"nertz:  [{hand.top_nertz()}]")
    hand_win.addstr(4, 1, f"         {hand.count_nertz()}")
    hand_win.addstr(6, 1, f"wp1:    {hand.get_wp(0)}")
    hand_win.addstr(7, 1, f"wp2:    {hand.get_wp(1)}")
    hand_win.addstr(8, 1, f"wp3:    {hand.get_wp(2)}")
    hand_win.addstr(9, 1, f"wp4:    {hand.get_wp(3)}")
    hand_win.addstr(11, 1, f"draw pile:   {hand.get_top3()}")

    with print_mutex:
        hand_win.refresh()         

curses.wrapper(main)

if __name__ == "__main__":
    main()