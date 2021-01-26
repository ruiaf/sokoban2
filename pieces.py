from enum import Enum


class Piece(object):
    def __init__(self, piece: str):
        if piece not in ["#", "X", "O", " ", "P", "@"] and not piece.isdigit():
            raise Exception("Invalid Piece \"%s\"" % piece)
        self.value: str = piece

    def __eq__(self, other: 'Piece'):
        if self.value.isdigit() and other == Pieces.PLAYER:
            return True
        if other is None:
            return False
        return self.value == other.value

    def __str__(self):
        return self.value


class Pieces(object):
    WALL = Piece("#")
    BOX = Piece("X")
    TARGET = Piece("O")
    EMPTY = Piece(" ")
    PLAYER = Piece("P")
    BOX_AT_TARGET = Piece("@")
