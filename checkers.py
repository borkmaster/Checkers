# TODO Abstract base class for Square / Checker?

class CheckersGame:
    pass


class GameBoard:
    valid_colors = ["red","black"]
    


class Square:

    def __init__(self, color, coord):
        self.color = color
        self.coord = coord
        self.checker = None


class Checker:
    
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord
        self.is_king = false
