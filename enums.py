from enum import Enum

class Color(Enum):
    RED = 0
    BLACK = 1

class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

class Status(Enum):
    SUCCESS = 0
    EMPTY = 1
    INVALID_MOVE = 2
