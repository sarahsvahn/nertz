
from working_pile import WorkingPile
from card import Card
from enums import Suit, Color, Status

def main(): 
    test_card()
    test_working_pile()

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
    wp = WorkingPile(card1)
    assert(wp.get_cards() == [card1])
    assert(wp.put_card(card2) == Status.SUCCESS)
    assert(wp.get_cards() == [card1, card2])
    assert(wp.put_card(card3) == Status.INVALID_MOVE)

    # todo test remove_cards
    # todo test remove_top_card


if __name__ == "__main__":
    main()