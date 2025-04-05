
from working_pile import WorkingPile
from card import Card
from enums import Suit, Color, Status
from draw_pile import DrawPile
from community_section import CommunitySection

def main(): 
    test_card()
    test_working_pile()
    test_draw_pile()
    test_community_section()

def test_card():
    card1 = Card("D", 3)
    assert(Card.get_value(card1) == 3)
    assert(Card.get_suit(card1) == Suit.D)
    assert(Card.get_color(card1) == Color.RED)
    
    card2 = Card("H", 10)
    assert(Card.get_value(card2) == 10)
    assert(Card.get_suit(card2) == Suit.H)
    assert(Card.get_color(card2) == Color.RED)
    
    card3 = Card("C", 8)
    assert(Card.get_value(card3) == 8)
    assert(Card.get_suit(card3) == Suit.C)
    assert(Card.get_color(card3) == Color.BLACK)
    
    card4 = Card("S", 9)
    assert(Card.get_value(card4) == 9)
    assert(Card.get_suit(card4) == Suit.S)
    assert(Card.get_color(card4) == Color.BLACK)

def test_working_pile():
    card1 = Card("C", 10)
    card2 = Card("H", 9)
    card3 = Card("H", 8)
    card4 = Card("S", 8)
    card5 = Card("H", 7)
    card6 = Card("S", 6)
    card7 = Card("H", 5)

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
    # print(pile.take_card())
    assert(pile.take_card() == 1)
    # print(pile.shuffle_cards())

def test_community_section():
    print("test")
    card1 = Card("C", 1)
    card2 = Card("S", 1)
    card3 = Card("H", 1)
    card4 = Card("D", 1)
    card5 = Card("D", 2)
    card6 = Card("D", 3)
    card7 = Card("D", 4)
    card8 = Card("D", 5)
    card9 = Card("D", 6)
    card10 = Card("D", 7)
    card11 = Card("D", 8)
    card12 = Card("D", 9)
    card13 = Card("D", 10)
    card14 = Card("D", 11)

    cs = CommunitySection(3)
    cs.add_to_pile(card2)
    cs.add_to_pile(card3)
    cs.add_to_pile(card4)
    cs.add_to_pile(card1)
    cs.add_to_pile(card5, "cp3")
    cs.add_to_pile(card6, "cp3")
    cs.add_to_pile(card7, "cp3")
    cs.add_to_pile(card8, "cp3")
    cs.add_to_pile(card9, "cp3")
    cs.add_to_pile(card10, "cp3")
    cs.add_to_pile(card11, "cp3")
    cs.add_to_pile(card12, "cp3")
    cs.add_to_pile(card13, "cp3")
    cs.add_to_pile(card14, "cp3")
    cs.add_to_pile(card1)
    print(cs.get_board())
    
if __name__ == "__main__":
    main()