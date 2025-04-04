
from working_pile import WorkingPile
from card import Card
from enums import Suit, Color, Status
from draw_pile import DrawPile

def main(): 
    test_card()
    test_working_pile()
    test_draw_pile()

def test_card():
    card1 = Card(Suit.DIAMONDS, 3)
    assert(Card.get_value(card1) == 3)
    assert(Card.get_suit(card1) == Suit.DIAMONDS)
    assert(Card.get_color(card1) == Color.RED)
    
    card2 = Card(Suit.HEARTS, 10)
    assert(Card.get_value(card2) == 10)
    assert(Card.get_suit(card2) == Suit.HEARTS)
    assert(Card.get_color(card2) == Color.RED)
    
    card3 = Card(Suit.CLUBS, 8)
    assert(Card.get_value(card3) == 8)
    assert(Card.get_suit(card3) == Suit.CLUBS)
    assert(Card.get_color(card3) == Color.BLACK)
    
    card4 = Card(Suit.SPADES, 9)
    assert(Card.get_value(card4) == 9)
    assert(Card.get_suit(card4) == Suit.SPADES)
    assert(Card.get_color(card4) == Color.BLACK)

def test_working_pile():
    card1 = Card(Suit.CLUBS, 10)
    card2 = Card(Suit.HEARTS, 9)
    card3 = Card(Suit.HEARTS, 8)
    card4 = Card(Suit.SPADES, 8)
    card5 = Card(Suit.HEARTS, 7)
    card6 = Card(Suit.SPADES, 6)
    card7 = Card(Suit.HEARTS, 5)

    wp = WorkingPile(card1)
    wp2 = WorkingPile(card5)

    assert(wp.get_cards() == [card1])
    assert(wp.put_cards([card2]) == Status.SUCCESS)
    assert(wp.get_cards() == [card1, card2])
    assert(wp.put_cards([card3]) == Status.INVALID_MOVE)
    assert(wp.put_cards([card4]) == Status.SUCCESS)
    # assert(wp.remove_cards(card2) == [card2, card4])
    # assert(wp.remove_top_card() == card1)
    # assert(wp.get_cards() == [])
    assert(wp2.get_cards() == [card5])
    assert(wp2.put_cards([card6, card7]) == Status.SUCCESS)
    assert(wp2.get_cards() == [card5, card6, card7])
    assert(wp.put_cards(wp2.remove_cards(card5)) == Status.SUCCESS)
    assert(wp.get_cards() == [card1, card2, card4, card5, card6, card7])



def test_draw_pile():
    cards = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    pile = DrawPile(cards)
    assert(pile.take_card() == Status.EMPTY)
    assert(pile.get_card() == Status.EMPTY)
    assert(pile.draw_three() == [11,12,13])
    assert(pile.draw_three() == [8,9,10])
    assert(pile.draw_three() == [5,6,7])
    assert(pile.draw_three() == [2,3,4])
    assert(pile.draw_three() == [1,2,3])
    assert(pile.take_card() == (1, [2,3,4]))
    # print(pile.shuffle_cards())
    
if __name__ == "__main__":
    main()