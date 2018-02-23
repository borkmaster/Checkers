from abc import ABCMeta, abstractmethod
import itertools
# TODO Abstract base class for Square / Checker?

class CheckersGame:
    pass


class GameBoard:
    
    valid_colors = ["RED","BLACK"]
    dimensions = (8, 8)
    rows = ['1','2','3','4','5','6','7','8']
    columns = ['A','B','C','D','E','F','G','H']
    
    def __init__(self):
        self.create_new_game_board()

    def create_new_game_board(self):
        self.board = []
        width = self.dimensions[0]
        height = self.dimensions[1]
        first_square_color = "BLACK"
        for row in range(height):
            square_color = first_square_color
            row_of_squares = []
            for column in range(width):
                color = square_color
                coord = (column, row)
                row_of_squares.append(Square(color, coord))
                square_color = "BLACK" if square_color=="RED" else "RED"
            first_square_color = "BLACK" if first_square_color=="RED" else "RED"
            self.board.append(row_of_squares)

    def refresh_board(self):
        for row in self.board:
            for square in row:
                square.refresh_graphic()

    def print_board(self):
        gameboard.refresh_board()
        left_buffer = '     '
        print (left_buffer + ' ' + ('_' * self.dimensions[0] * Square.dimensions[0]) + ' ')
        for row_index in reversed(range(len(gameboard.board))):
            row = gameboard.board[row_index]
            for g_row in range(Square.dimensions[1]):
                pixel_row = '  ' + GameBoard.rows[row_index] + '  ' if g_row == 2 else left_buffer
                for square in row:
                    pixel_row += square.graphic[g_row]
                pixel_row += '|'
                print(pixel_row)
        column_row = left_buffer
        for column in GameBoard.columns:
            column_row += "     " + column + "    "
        print(column_row)

    


# Practicing making use of Abstract Base Classes
class GameComponent(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord


class Square(GameComponent):

    dimensions = (10, 5)

    def __init__(self, color, coord):
        super().__init__(color, coord)
        self.checker = None

    # Updates this square's graphic based on this square's current checker properties
    def refresh_graphic(self):
        # F = background fill
        F = " " if self.color == "RED" else "X"
        width = self.dimensions[0]
        height = self.dimensions[1]
        self.graphic = [("|" + ( 9 * F ))]
        for row in range(height-2):
            row_graphic = "|"
            if ( self.checker ):
                row_graphic += F + self.checker.graphic[row] + F
            else:
                if ( row == 1 ):
                    # row_graphic += str(self.coord).center(9, F)
                    board_coord = " " + str(GameBoard.columns[self.coord[0]]) + str(GameBoard.rows[self.coord[1]]) + " "
                    row_graphic += str(board_coord).center(9, F)
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
        

    


gameboard = GameBoard()
gameboard.print_board()
