import requests
from hand import Hand
import threading

def main():
    hand = Hand()
    print_mutex = threading.Lock()
    query_loop(hand, print_mutex)

    # server_url = "http://localhost:5000/message"
    # message_data = {"message": "Hello, Flask!"}

    # response = requests.post(server_url, json=message_data)
    # print("Server response:", response.json())

def query_loop(hand, print_mutex): 
    print_board(hand, print_mutex)
    query = input("> ").lower()
    while query != "exit": 
        # commands:
        # m [Card] [location]  // moves card to location
        #   m 2D cp1
        #   m 2D wp3
        #   m 4D wp2 // this moves multiple cards if 4D isn't top card
        # d  // flips next top 3 from draw pile
        # s  // says "i want to shuffle"

        # put query loop and waiting for print loop in two threads (#concurrency)
        if len(query) == 0: 
            print("Invalid query. USAGE: todo") 
        else: 
            query = query.split()
            if query[0] == 'm' and len(query) == 3 and ("cp" in query[2] or "wp" in query[2]): 
                print("MOVE")
                result = hand.move(query[1], query[2])
                print(result)
                #todo print 
            elif query == ['d']: 
                hand.draw()
            elif query == ['s']:
                hand.shuffle()
            else: 
                print("Invalid query. USAGE: todo") 
        
        print_board(hand, print_mutex)           
        query = input("> ").lower()
    
def print_board(hand, print_mutex):
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
        print("[Name]'s Hand:")
        print(f"nertz:  {hand.top_nertz()}")
        print(f"wp1:    {hand.get_wp(0)}")
        print(f"wp2:    {hand.get_wp(1)}")
        print(f"wp3:    {hand.get_wp(2)}")
        print(f"wp4:    {hand.get_wp(3)}")
        print(f"top3:   {hand.get_top3()}")

if __name__ == "__main__":
    main()