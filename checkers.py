from abc import ABCMeta, abstractmethod
import itertools
# TODO Abstract base class for Square / Checker?

class CheckersGame:
    pass


class GameBoard:
    valid_colors = ["RED","BLACK"]
    def __init__(self):
        self.dimensions = (8, 8)
        self.rows = ['1','2','3','4','5','6','7','8']
        self.columns = ['A','B','C','D','E','F','G','H']

    def create_new_game_board(self):
        self.game_board = []
        width = self.dimensions[0]
        height = self.dimensions[1]
        first_square = ""
        for row in range(height):
            
            row_of_squares = []
            for square in range(width):
                row_of_squares.append(Square)


# Practicing making use of Abstract Base Classes
class GameComponent(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord


class Square(GameComponent):

    def __init__(self, color, coord):
        super().__init__(color, coord)
        self.checker = None
        self.dimensions = (10, 5)

    # Updates this square's graphic based on this square's current checker properties
    def refresh_graphic(self):
        # F = background fill
        if self.color == "RED":
            F = " "
        elif self.color == "BLACK":
            F = "X"
        width = self.dimensions[0]
        height = self.dimensions[1]
        self.graphic = [("|" + ( 9 * F ))]
        for row in range(height-2):
            row_graphic = "|"
            if ( self.checker ):
                row_graphic += F + self.checker.graphic[row] + F
            else:
                row_graphic += F * 9
            self.graphic.append(row_graphic)
        if ( self.color == "RED" ):
            self.graphic.append(("|" + ("_" * 9)))
        else:
            self.graphic.append(("|" + ( 9 * F )))
            
        

    def print_graphic(self):
        for row in self.graphic:
            print(row)


class Checker(GameComponent):
    
    def __init__(self, color, coord):
        super().__init__(color, coord)
        self.is_king = False
        self.needs_graphic_refresh = False
        self.set_move_direction()
        self.dimensions = (7, 3)

    def set_move_direction(self):
        if ( self.color == "RED" ):
            self.move_direction = 1
        elif ( self.color == "BLACK" ):
            self.move_direction = -1
        else:
            raise Exception("Invalid checker color: " + self.color + ". Must be RED or BLACK.")

    def update_graphic(self):
        self.graphic = []
        width = self.dimensions[0]
        height = self.dimensions[1]
        for row in range(height):
            row_graphic = "|"
            if ( row == 0 ):
                if ( self.is_king ):
                    row_graphic += self.color.center(5, " ")
                else:
                    row_graphic += " " * 5
            elif ( row == 1 ):
                if ( self.is_king ):
                    row_graphic += " KING"
                else:
                    row_graphic += self.color.center(5, " ")
            else:
                row_graphic += "_" * 5
            row_graphic += "|"
            self.graphic.append(row_graphic)
        

    


square = Square("RED", (1, 2))
checker = Checker("RED", (3, 1))
checker.is_king = True
checker.update_graphic()
square.checker = checker
square.refresh_graphic()
for row in square.graphic:
    print (row)
