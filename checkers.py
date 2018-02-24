from abc import ABCMeta, abstractmethod
import itertools
# TODO Abstract base class for Square / Checker?

class CheckersGame:
    def get_checker_at_board_coord(self):
        pass


class GameComponent(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord


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
        self.initial_checker_placement()

    def initial_checker_placement(self):
        for row in self.board:
            for square in row:
                if ( square.color == "BLACK"):
                    if ( square.coord[1] in range(3) ):
                        square.checker = Checker("RED", square.coord)
                    elif ( square.coord[1] in range(len(self.board)-3, len(self.board)) ):
                        square.checker = Checker("BLACK", square.coord)

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

    # board_coord in format of 2 character string 'A3'
    def get_checker_at_board_coord(self, board_coord):
        row = self.rows.index(board_coord[1])
        column = self.columns.index(board_coord[0])
        square = self.board[row][column]
        if ( square.checker ):
            return square.checker
        else:
            print("No checker found at coordinate " + board_coord)
            return None


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
        self.set_board_coord()
        self.is_king = False
        self.needs_graphic_refresh = False
        self.set_move_direction()
        self.dimensions = (7, 3)
        self.update_graphic()

    def set_board_coord(self):
        column = GameBoard.columns[self.coord[0]]
        row = GameBoard.rows[self.coord[1]]
        self.board_coord = (column, row)

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
