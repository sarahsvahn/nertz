from enum import Enum

class Color(Enum):
    RED = 0
    BLACK = 1

class Suit(Enum):
    C = 0
    D = 1
    H = 2
    S = 3

class Status(Enum):
    SUCCESS = 0
    EMPTY = 1
    INVALID_MOVE = 2
    INVALID_CARD = 3

class Origin(Enum):
    WP1 = 0
    WP2 = 1
    WP3 = 2
    WP4 = 3
    NERTZ = 4
    DRAW = 5
    NOT_FOUND = 6
