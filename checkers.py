from abc import ABCMeta, abstractmethod
import itertools

# TODO make a king_me function for Checker class

class CheckersGame:

    def play(self):
        self.players_turn = "BLACK"
        self.gameboard = self.GameBoard()
        while ( self.gameboard.checker_counts['RED'] > 0 and self.gameboard.checker_counts['BLACK'] > 0 ):
            self.new_turn()
        self.winner = "RED" if self.gameboard.checker_counts["BLACK"] == 0 else "RED"
        print( self.winner + " WINS!" )
        input()

    def new_turn(self):
        game.gameboard.print_board()
        print('New Turn')
        turn_complete = False
        from_square_selected = False
        while ( not from_square_selected ):
            from_square = self.get_from_square()
            from_square_selected = True
            to_square = None
            while ( not to_square or not self.is_checker_move_allowed ( from_square, to_square ) ):
                to_square = self.get_to_square()
                if ( to_square == None ):
                    from_square_selected = False
                    break
        vertical_distance = abs(to_square.coord[1] - from_square.coord[1])
        if ( vertical_distance == 2 ):
            while ( not turn_complete ):
                self.move_checker_to_square(from_square, to_square)
                jumped_square = self.get_jumped_square(from_square, to_square)
                self.remove_jumped_piece(jumped_square)
                self.gameboard.print_board()
                from_square = to_square
                if ( self.gameboard.checker_counts["RED"] < 1 or self.gameboard.checker_counts["BLACK"] < 1 ):
                    break
                while (abs(to_square.coord[1] - from_square.coord[1]) != 2 or not self.is_checker_move_allowed(from_square, to_square)):
                    to_square = self.get_to_square()
                    if ( to_square == None ):
                        turn_complete = True
                        break
                    elif (abs(to_square.coord[1] - from_square.coord[1]) != 2):
                        print('You may only make consective jump moves following a jump')
        else:
            self.move_checker_to_square(from_square, to_square)
        self.players_turn = "BLACK" if self.players_turn == "RED" else "RED"

    def get_from_square(self):
        from_board_coord = ''
        from_square = None
        while ( not from_square ):
            while ( len(from_board_coord) != 2 or ( from_board_coord[0] not in self.gameboard.columns and from_board_coord[1] not in self.gameboard.rows ) ):
                print( 'Current player\'s turn: ' + self.players_turn )
                from_board_coord = input('Please provide the coordinate of a piece you would like to move:\n').upper()
            from_square = self.get_square_at_board_coord(from_board_coord)
            if ( not from_square.checker or from_square.checker.color != self.players_turn ):
                print( 'Invalid checker selection' )
                from_board_coord = ''
                from_square = None
        return from_square

    def get_to_square(self):
        to_board_coord = ''
        to_square = None
        while ( len(to_board_coord) != 2 or ( to_board_coord[0] not in self.gameboard.columns and to_board_coord[1] not in self.gameboard.rows ) ):
            to_board_coord = input('Please provide the coordinate of the square you would like to move your piece to:  (or type \'back\' to select a different checker to move / end your turn if you\'ve already moved)\n').upper()
            if ( to_board_coord == 'BACK' ):
                return None
            if ( len(to_board_coord) != 2 or ( to_board_coord[0] not in self.gameboard.columns and to_board_coord[1] not in self.gameboard.rows ) ):
                print( 'Invalid input' )
        to_square = self.get_square_at_board_coord(to_board_coord)
        return to_square

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
        if ( to_square.checker.coord[1] == to_square.checker.king_row ):
            to_square.checker.king_me()

    def get_jumped_square(self, from_square, to_square):
        vertical_direction = to_square.coord[1] - from_square.coord[1]
        horizontal_direction = to_square.coord[0] - from_square.coord[0]
        print('vertical direction: ' + str(vertical_direction))
        print('horizontal direction: ' + str(horizontal_direction))
        if ( abs(vertical_direction) == 2 ):
            jumped_square = game.gameboard.board[from_square.coord[1] + int(vertical_direction/2)][from_square.coord[0] + int(horizontal_direction/2)]
            return jumped_square
        else:
            return None


    def remove_jumped_piece(self, jumped_square):
        if (jumped_square):
            self.gameboard.checker_counts[jumped_square.checker.color] -= 1
            jumped_square.checker = None
        else:
            print('jumped_square is empty')
        

    def is_checker_move_allowed(self, from_square, to_square):
        # Get movement direction and distance info
        vertical_direction = to_square.coord[1] - from_square.coord[1]
        vertical_distance = abs(vertical_direction)
        horizontal_direction = to_square.coord[0] - from_square.coord[0]
        horizontal_distance = abs(horizontal_direction)

        # Verify checker exists at start square
        if ( not from_square.checker ):
            print( 'No checker to move at ' + str(from_square.board_coord) )
            return False
        # Verify checker in selected start square belongs to player
        if ( not from_square.checker.color == self.players_turn ):
            print( 'The checker at ' + str(from_square.board_coord) + ' belongs to ' + from_square.checker.color + '. It is currently ' + self.players_turn + '\'S turn.' )
            return False
        # Verify a checker doesn't already exist at the destination
        if ( to_square.checker ):
            print( 'There is already a checker at ' + str(to_square.board_coord) )
            return False
        # Verify attempted movement is diagonal
        if ( horizontal_distance != vertical_distance ):
             print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. Must move diagonally')
             return False
        # Verify player is moving in the correct direction
        if ( not from_square.checker.is_king and vertical_direction / vertical_distance != from_square.checker.move_direction):
            print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. Attempting to move checker in the wrong direction' )
            return False
        # Verify player is attempting to move up to a max of two squares diagonally
        if ( vertical_distance not in range(1, 3) ):
             print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. If jumping multiple pieces, please move one jump at a time.' )
             return False
        # Verify that, if player is attempting to "jump" a square, a checker of the opposite color exists in the jumped square
        if ( vertical_distance == 2 ):
            jumped_square = game.gameboard.board[from_square.coord[1] + int(vertical_direction/2)][from_square.coord[0] + int(horizontal_direction/2)]
            if ( not jumped_square.checker or not jumped_square.checker.color != game.players_turn ):
                 print( 'Invalid move ' + str(from_square.board_coord) + ' -> ' + str(to_square.board_coord) + '. No checker of the opposite color at ' + str(jumped_square.board_coord))
                 return False
        # WHEW if none of that stuff happened then YOU ALLOWED BOI
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
            self.set_row_to_king()
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

        def set_row_to_king(self):
            self.king_row = 7 if self.coord[1] in range(3) else 0

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

        def king_me(self):
            self.is_king = True
            self.update_graphic()
        

    


game = CheckersGame()
game.play()
