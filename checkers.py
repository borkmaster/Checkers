from abc import ABCMeta, abstractmethod
import itertools
# TODO Abstract base class for Square / Checker?

# TODO currently able to move checkers 2 spaces without a checker of opposite color in the middle

class CheckersGame:

    def play(self):
        self.players_turn = "BLACK"
        self.gameboard = self.GameBoard()

    def get_checker_at_board_coord(self, board_coord):
            row = self.gameboard.rows.index(board_coord[1])
            column = self.gameboard.columns.index(board_coord[0])
            square = self.gameboard.board[row][column]
            if ( square.checker ):
                return square.checker
            else:
                print("No checker found at coordinate " + board_coord)
                return None

    def get_square_at_board_coord(self, board_coord):
        row = self.gameboard.rows.index(board_coord[1])
        column = self.gameboard.columns.index(board_coord[0])
        square = self.gameboard.board[row][column]
        return square


    def move_checker_to_square(self, from_square, to_square):
        to_square.checker = from_square.checker
        to_square.checker.coord = to_square.coord
        from_square.checker = None
        

    def is_checker_move_allowed(self, from_square, to_square):
        # Weed out the ignant moves
        # No checker in selected square
        if ( not from_square.checker ):
            print( 'No checker to move at ' + str(from_square.board_coord) )
            return False
        # Selected checker doesn't belong to the player
        if ( not from_square.checker.color == self.players_turn ):
            print( 'The checker at ' + str(from_square.board_coord) + ' belongs to ' + from_square.checker.color + '. It is currently ' + self.players_turn + '\'S turn.' )
            return False
        # There's already a checker where player is trying to move the checker
        if ( to_square.checker ):
            print( 'There is already a checker at ' + str(to_square.board_coord) )
            return False

        # Okay down to business. Need some vectors and magnitudes
        vertical_direction = to_square.coord[1] - from_square.coord[1]
        vertical_distance = abs(vertical_direction / from_square.checker.move_direction)
        horizontal_direction = to_square.coord[0] - from_square.coord[0]
        horizontal_distance = abs(horizontal_direction)

        # If player tries to move checker piece the wrong direction
        if ( not from_square.checker.is_king and vertical_direction / vertical_distance != from_square.checker.move_direction):
            print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. Attempting to move checker in the wrong direction' )
            return False
        # If player tries to move a distance that is not 1 or 2 squares away
        if ( vertical_distance not in range(1, 3) ):
             print(str(vertical_distance))
             print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. If jumping multiple pieces, please move one jump at a time.' )
             return False
        # If movement is not diagonal
        if ( horizontal_distance != vertical_distance ):
             print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. Must move diagonally')
             return False
        # If player is trying to make a jump but an appropriate checker doesn't exist in the jumped square
        if ( vertical_distance == 2 ):
            print("hello")
            jumped_square = game.gameboard.board[from_square.coord[0] + int(vertical_direction/2)][from_square.coord[1] + int(horizontal_direction/2)]
            if ( not jumped_square.checker or not jumped_square.checker.color != game.players_turn ):
                 print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. No checker of the opposite color at ' + str(jumped_square.board_coord))
                 return False
        # WHEW if none of that stuff happened then return True
        return True
             


        
        if ( not from_square.checker.is_king ):
##            if ( to_square.coord[1] - from_square.coord[1] not in range(from_square.checker.move_direction, from_square.checker.move_direction * 2 + from_square.checker.move_direction) ):
##                print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. If jumping multiple pieces, please move one jump at a time.' )
##                return False
            if ( to_square.coord[1] - from_square.coord[1] == square.checker.move_direction ):
                pass
            elif ( to_square.coord[1] - from_square.coord[1] == square.checker.move_direction * 2 ):
                pass
            else:
                print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. If jumping multiple pieces, please move one jump at a time.' )
                return False
        return True


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
            self.checker_counts = {'RED': 0, 'BLACK': 0}
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
                    row_of_squares.append(CheckersGame.Square(color, coord))
                    square_color = "BLACK" if square_color=="RED" else "RED"
                first_square_color = "BLACK" if first_square_color=="RED" else "RED"
                self.board.append(row_of_squares)
            self.initial_checker_placement()

        def initial_checker_placement(self):
            for row in self.board:
                for square in row:
                    if ( square.color == "BLACK"):
                        if ( square.coord[1] in range(3) ):
                            square.checker = CheckersGame.Checker("RED", square.coord)
                        elif ( square.coord[1] in range(len(self.board)-3, len(self.board)) ):
                            square.checker = CheckersGame.Checker("BLACK", square.coord)
                        if ( square.checker ):
                            self.checker_counts[square.checker.color] += 1

        def refresh_board(self):
            for row in self.board:
                for square in row:
                    square.refresh_graphic()

        def print_board(self):
            self.refresh_board()
            left_buffer = '     '
            print (left_buffer + ' ' + ('_' * self.dimensions[0] * CheckersGame.Square.dimensions[0]) + ' ')
            for row_index in reversed(range(len(self.board))):
                row = self.board[row_index]
                for g_row in range(CheckersGame.Square.dimensions[1]):
                    pixel_row = '  ' + CheckersGame.GameBoard.rows[row_index] + '  ' if g_row == 2 else left_buffer
                    for square in row:
                        pixel_row += square.graphic[g_row]
                    pixel_row += '|'
                    print(pixel_row)
            column_row = left_buffer
            for column in CheckersGame.GameBoard.columns:
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
            self.set_board_coord()

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
                        board_coord = " " + str(CheckersGame.GameBoard.columns[self.coord[0]]) + str(CheckersGame.GameBoard.rows[self.coord[1]]) + " "
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

        def set_board_coord(self):
            column = CheckersGame.GameBoard.columns[self.coord[0]]
            row = CheckersGame.GameBoard.rows[self.coord[1]]
            self.board_coord = (column, row)


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
            column = CheckersGame.GameBoard.columns[self.coord[0]]
            row = CheckersGame.GameBoard.rows[self.coord[1]]
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
        

    


game = CheckersGame()
game.play()
game.gameboard.print_board()
