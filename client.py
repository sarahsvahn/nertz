# import requests
from hand import Hand
import threading
import socketio
from enums import Status, Origin
from card import Card
import curses 

sio = socketio.Client()

cp_move_done = threading.Event()

server_url = "http://localhost:5000"

hand = Hand()
print_mutex = threading.Lock()

name = ""
input_win = None
community_win = None 
hand_win = None

def main(stdscr):
    global input_win, community_win, hand_win
    
    stdscr.clear()
    curses.curs_set(1) # show cursor ? 
    curses.echo()
    height, width = stdscr.getmaxyx()
    input_height = 3
    output_height = height - input_height
    hand_win = curses.newwin(output_height, int(width / 2), 0, 0)
    community_win = curses.newwin(output_height, int(width / 2), 0, int(width / 2))
    input_win = curses.newwin(input_height, width, output_height, 0)

    input_win.border()
    input_win.refresh()

    community_win.border()
    community_win.refresh()

    hand_win.border()
    hand_win.refresh()


    # query_loop(hand, print_mutex)

    # message_data = {"message": "player_join"}
    # response = requests.post(server_url, json=message_data)
    # print("Server response:", response.json())

    sio.connect(server_url)
    # print("Connected to server")

    establish_player()

    # query_loop(hand, print_mutex)

# curses.wrapper(main)


def establish_player():
    global name, input_win
    input_win.addstr(1, 1, "Welcome to Nertz! Enter your name: ")
    name = input_win.getstr().decode("utf-8")
    input_win.clear()
    input_win.border()
    input_win.refresh()
    # name = input_win.getstr(1, 8, 60) #decode("utf-8")
    # name = input("Welcome to Nertz!\nEnter your name: ")
    sio.emit("player_join", {"name": name})
    sio.wait()

@sio.on("game_joined")
def handle_game_joined(data):
    # input_win.addstr(1, 1, f"Hello {data.get('name')}")
    sio.wait()

@sio.on("cp_move_result")
def cp_move_result(data):
    if Status[data.get("status")] == Status.SUCCESS:
        remove_location = data.get("origin")
        card = Card.card_with_name(data.get("card")) # TODO make this a function in card class 
        hand.remove_from_origin(card, Origin[remove_location])
    else: 
        print("Move failed. RIPPPPP that sucks.")

    cp_move_done.set()

@sio.on("cs_updated")
def update_cs(data):
    global community_win
    
    community_win.clear()
    community_win.border()
    
    board = data.get("board").split("\n")
    for i, line in enumerate(board): 
        community_win.addstr(i + 1, 1, line)
    
    community_win.refresh()

@sio.on("start_game")
def query_loop(): 
    print_board(hand, print_mutex)
    input_win.addstr(1, 1, "> ")
    query = input_win.getstr().decode("utf-8").lower()
    # query = input("> ").lower()
    while query != "exit": 
        if len(query) == 0: 
            hand_win.addstr("Invalid query. USAGE: todo") 
        else: 
            query = query.split()
            if query[0] == 'm' and len(query) == 3:
                # TODO validate card, make sure 1D not D1 (maybe here?)
                if "cp" in query[2]:
                    # origin = hand.find_og_location(Card(query[1][-1], int(query[1][:-1])), "CP")
                    # hand_win.addstr(query[1])
                    origin = hand.find_og_location(Card.card_with_name(query[1]), "CP")
                    if origin != Origin.NOT_FOUND:
                        cp_move_done.clear()
                        sio.emit('cp_move', {'card': query[1], 'pile': query[2], "origin": origin.name})
                        cp_move_done.wait()
                    else:
                        print("Invalid move")
                elif "wp" in query[2]: 
                    # hand_win.addstr("MOVE WP")
                    # result = hand.move_to_wp(query[1], query[2])
                    hand.move_to_wp(query[1], query[2])
                    # hand_win.addstr(result)
                else: 
                    hand_win.addstr("Invalid query. USAGE: todo") 
                #todo print 
            elif query == ['d']: 
                hand.draw()
            elif query == ['s']:
                hand.shuffle()
                # todo 
            else: 
                hand_win.addstr("Invalid query. USAGE: todo") 

        # sio.wait()
        print_board(hand, print_mutex)  
        
        input_win.clear()
        input_win.border()
        input_win.refresh()         
        
        input_win.addstr(1, 1, "> ")
        query = input_win.getstr().decode("utf-8").lower()
 
    # input_win.clrtoeol() TODO 


def print_board(hand, print_mutex):
    global hand_win
    # [name] added 1D to cp2
    # COMMUNITY SECTION
    # [ 1D , Card, Card] // these are top cards
    #   cp1   cp2   cp3
    # [Card, Card, Card]
    #  cp4   cp5   cp6

    # [name]'s HAND:
    # nertz: Card
    # wp1: [Cards]
    # wp2: [Cards]
    # wp3: [Cards]
    # wp4: [Cards]
    # top3: [Card, Card, Card]

    with print_mutex:
        hand_win.clear()
        hand_win.border()

        hand_win.addstr(1, 1, f"{name}'s HAND:")
        hand_win.addstr(2, 1, f"nertz:  {hand.top_nertz()}")
        hand_win.addstr(3, 1, f"wp1:    {hand.get_wp(0)}")
        hand_win.addstr(4, 1, f"wp2:    {hand.get_wp(1)}")
        hand_win.addstr(5, 1, f"wp3:    {hand.get_wp(2)}")
        hand_win.addstr(6, 1, f"wp4:    {hand.get_wp(3)}")
        hand_win.addstr(7, 1, f"top3:   {hand.get_top3()}")

        hand_win.refresh()         

curses.wrapper(main)

if __name__ == "__main__":
    main()