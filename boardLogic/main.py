# import adafruit_blinka
# import board
# import digitalio
# import busio
import copy

class Masks:
    BLACK = 0b0000000000
    WHITE = 0b1000000000
    PAWN = 0b0001000000
    ROOK = 0b0010000000
    KNIGHT = 0b0011000000
    BISHOP = 0b0100000000
    QUEEN = 0b0101000000
    KING = 0b0110000000


class ChessBoard:
    WHITE_PAWN = Masks.WHITE | Masks.PAWN
    WHITE_ROOK = Masks.WHITE | Masks.ROOK
    WHITE_KNIGHT = Masks.WHITE | Masks.KNIGHT
    WHITE_BISHOP = Masks.WHITE | Masks.BISHOP
    WHITE_QUEEN = Masks.WHITE | Masks.QUEEN
    WHITE_KING = Masks.WHITE | Masks.KING
    BLACK_PAWN = Masks.BLACK | Masks.PAWN
    BLACK_ROOK = Masks.BLACK | Masks.ROOK
    BLACK_KNIGHT = Masks.BLACK | Masks.KNIGHT
    BLACK_BISHOP = Masks.BLACK | Masks.BISHOP
    BLACK_QUEEN = Masks.BLACK | Masks.QUEEN
    BLACK_KING = Masks.BLACK | Masks.KING

    def __init__(self):
        # Sets up the board state as the default starting state

        # These two lines are how all squares will be set up
        # a1 = digitalio.DigitalInOut(board.G1)
        # a1.direction = digitalio.Direction.INPUT

        self.pieces_in_play = 32

        # Initial board state
        self.state = {
            self.WHITE_PAWN: [],
            self.WHITE_ROOK: [(0, 0), (0, 7)],
            self.WHITE_KNIGHT: [(0, 1), (0, 6)],
            self.WHITE_BISHOP: [(0, 2), (0, 5)],
            self.WHITE_QUEEN: [(0, 3)],  # If a pawn travels the length of the board, multiple queens can be on board
            self.WHITE_KING: (0, 4),  # However, there can only be one king of each color, so no list is used
            self.BLACK_PAWN: [],
            self.BLACK_ROOK: [(7, 0), (7, 7)],
            self.BLACK_KNIGHT: [(7, 1), (7, 6)],
            self.BLACK_BISHOP: [(7, 2), (7, 5)],
            self.BLACK_QUEEN: [(7, 3)],
            self.BLACK_KING: (7, 4)
        }

        self.state1 = {
            (1, 0): self.WHITE_PAWN,
            (1, 1): self.WHITE_PAWN,
            (1, 2): self.WHITE_PAWN,
            (1, 3): self.WHITE_PAWN,
            (1, 4): self.WHITE_PAWN,
            (1, 5): self.WHITE_PAWN,
            (1, 6): self.WHITE_PAWN,
            (1, 7): self.WHITE_PAWN,
            (0, 0): self.WHITE_ROOK,
            (0, 7): self.WHITE_ROOK,
            (0, 1): self.WHITE_KNIGHT,
            (0, 6): self.WHITE_KNIGHT,
            (0, 2): self.WHITE_BISHOP,
            (0, 5): self.WHITE_BISHOP,
            (0, 3): self.WHITE_QUEEN,  # If a pawn travels the length of the board, multiple queens can be on board
            (0, 4): self.WHITE_KING,  # However, there can only be one king of each color, so no list is used

            (6, 0): self.BLACK_PAWN,
            (6, 1): self.BLACK_PAWN,
            (6, 2): self.BLACK_PAWN,
            (6, 3): self.BLACK_PAWN,
            (6, 4): self.BLACK_PAWN,
            (6, 5): self.BLACK_PAWN,
            (6, 6): self.BLACK_PAWN,
            (6, 7): self.BLACK_PAWN,
            (7, 0): self.BLACK_ROOK,
            (7, 7): self.BLACK_ROOK,
            (7, 1): self.BLACK_KNIGHT,
            (7, 6): self.BLACK_KNIGHT,
            (7, 2): self.BLACK_BISHOP,
            (7, 5): self.BLACK_BISHOP,
            (7, 3): self.BLACK_QUEEN,
            (7, 4): self.BLACK_KING,
        }

        # set pawns
        for i in range(8):
            self.state[self.WHITE_PAWN].append((i, 1))
            self.state[self.BLACK_PAWN].append((i, 6))

        self.board_matrix = [[0 for i in range(8)] for j in range(8)]

        for j in range(2):
            for i in range(8):
                self.board_matrix[j][i] = True

        for j in range(2, 6):
            for i in range(8):
                self.board_matrix[j][i] = False

        for j in range(6, 8):
            for i in range(8):
                self.board_matrix[j][i] = True

    def print_matrix(self):
        count = 0
        print("Printing matrix")
        for row in self.board_matrix:
            print(count, row)
            count += 1

    def check_for_pick_up(self):
        # Checks the squares that were True and sees if they are still true
        # Alternate implementation is looking at the serialized board state and looking for differences
        checked_dict = {}

        # Checks the array to ensure there are no pieces picked up
        for j in range(8):
            for i in range(8):
                if self.board_matrix[i][j]:
                    checked_dict[(i, j)] = self.state1[(i, j)]

        if len(checked_dict) != self.pieces_in_play:
            # get the piece not on the board
            original_set = set(self.state1.items())
            checked_set = set(checked_dict.items())
            difference = original_set ^ checked_set
            picked_up_piece = list(difference)[0]
            # Provides a list where the 0th term is the cords, and the 1st is type
            self.user_move_piece(picked_up_piece[0], picked_up_piece[1])
            return False
        else:
            return True

    def serialize_state(self) -> bytes:
        # | 1 bit | 3 bits | 3 bits | 3 bits |
        # | color |  type  |   x    |    y   |
        pass

    def user_move_piece(self, location, piece_type):
        # displays the correct moves the piece can make
        previous_state = copy.deepcopy(self.state1)
        making_move = True
        legal_moves = self.find_legal_moves(location, piece_type)

        # Wait for any change in board state
        while making_move:


            print(piece_type, "can move to ", legal_moves)

            # TODO will need to scan for input here (ie. update board matrix)
            sim_input(self.board_matrix)

            # todo temporary fix to a major problem that needs a meeting to discuss
            self.state1.pop(location, None)

            count = 0

            for j in range(8):
                for i in range(8):
                    if self.board_matrix[i][j]:
                        count += 1
                    if self.board_matrix[i][j] and self.state1.get((i, j)) is None:
                        # TODO "or" part is a temp along fix with popping near line 158
                        if (i, j) in legal_moves:
                            making_move = False
                            print("You made a legal move!")
                            self.move_piece(location, (i, j), piece_type)
                            # todo this is just to make playing the game simpler in command prompt
                            self.print_matrix()

                        else:
                            making_move = True
                            print("You made an illegal move! Try again")

                    if not self.board_matrix[i][j] and (i, j) in self.state1.keys():
                        print("capturing piece")

                        if (i, j) in legal_moves:
                            # todo this will run into problems on physical board, needs testing
                            wait = True
                            while wait:
                                # todo check for updates
                                sim_input(self.board_matrix)
                                # this will only execute the capture if the piece is put on the square
                                # todo make this be something you can change your mind on
                                if self.board_matrix[i][j]:
                                    wait = False
                                    making_move = False
                                    print("You made a legal move!")
                                    self.capture_piece(location, (i, j), piece_type)
                                    self.print_matrix()

                        else:
                            making_move = True
                            print("You made an illegal move! Try again")

        # todo If legal move, re-serialize the board state

    def find_legal_moves(self, location, piece_type):
        legal_moves = []
        confirmed_legal_moves = []

        # todo replace with ternary
        color = None
        enemy_color = None
        if piece_type & Masks.WHITE == Masks.WHITE:
            color = Masks.WHITE
            enemy_color = Masks.BLACK
        else:
            color = Masks.BLACK
            enemy_color = Masks.WHITE

        # todo this can be converted down to just COLORED PAWN logic IF we find an easy way to
        #  discern piece type ie. "it is a bishop". Since only pawns have a movement limitation based on color.
        # logic to calc legal moves white pieces
        if piece_type == self.WHITE_PAWN:
            piece_1 = self.state1.get((location[0] + 1, location[1]), None)
            if piece_1 is None:
                legal_moves.append((location[0] + 1, location[1]))

            piece_2 = self.state1.get((location[0] + 2, location[1]), None)
            if piece_2 is None and piece_1 is None:
                legal_moves.append((location[0] + 2, location[1]))

            piece = self.state1.get((location[0] + 1, location[1] + 1), None)
            if piece is not None and piece <= 384:
                legal_moves.append((location[0] + 1, location[1] + 1))

            piece = self.state1.get((location[0] + 1, location[1] - 1), None)
            if piece is not None and piece <= 384:
                legal_moves.append((location[0] + 1, location[1] - 1))
        elif piece_type == self.WHITE_KNIGHT:
            legal_moves.append((location[0] + 2, location[1] + 1))
            legal_moves.append((location[0] + 2, location[1] - 1))
            legal_moves.append((location[0] - 2, location[1] + 1))
            legal_moves.append((location[0] - 2, location[1] - 1))
            legal_moves.append((location[0] - 1, location[1] + 2))
            legal_moves.append((location[0] + 1, location[1] + 2))
            legal_moves.append((location[0] - 1, location[1] - 2))
            legal_moves.append((location[0] + 1, location[1] - 2))
        elif piece_type == self.WHITE_BISHOP:
            # calc-ing moving down to right
            can_move_further = True
            for line in range(7):
                move = (location[0] + line, location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up to right
            for line in range(7):
                move = (location[0] - line, location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving down and left
            for line in range(7):
                move = (location[0] + line, location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up and left
            for line in range(7):
                move = (location[0] - line, location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
        elif piece_type == self.WHITE_ROOK:
            # calc-ing moving down
            can_move_further = True
            for line in range(7):
                move = (location[0] + line, location[1])
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up
            for line in range(7):
                move = (location[0] - line, location[1])
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving right
            for line in range(7):
                move = (location[0], location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving left
            for line in range(7):
                move = (location[0], location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
        elif piece_type == self.WHITE_QUEEN:
            # calc-ing moving down to right
            can_move_further = True
            for line in range(7):
                move = (location[0] + line, location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up to right
            for line in range(7):
                move = (location[0] - line, location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving down and left
            for line in range(7):
                move = (location[0] + line, location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up and left
            for line in range(7):
                move = (location[0] - line, location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving down
            can_move_further = True
            for line in range(7):
                move = (location[0] + line, location[1])
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up
            for line in range(7):
                move = (location[0] - line, location[1])
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving right
            for line in range(7):
                move = (location[0], location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving left
            for line in range(7):
                move = (location[0], location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
        elif piece_type == self.WHITE_KING:
            # todo double check logic
            legal_moves.append((location[0] + 1, location[1]))
            legal_moves.append((location[0] + 1, location[1] + 1))
            legal_moves.append((location[0] + 1, location[1] - 1))
            legal_moves.append((location[0], location[1] + 1))
            legal_moves.append((location[0] - 1, location[1] + 1))
            legal_moves.append((location[0], location[1] - 1))
            legal_moves.append((location[0] - 1, location[1] - 1))
            legal_moves.append((location[0] - 1, location[1]))

        # logic to calc legal moves black pieces
        if piece_type == self.BLACK_PAWN:
            piece_1 = self.state1.get((location[0] - 1, location[1]), None)
            if piece_1 is None:
                legal_moves.append((location[0] - 1, location[1]))

            piece_2 = self.state1.get((location[0] - 2, location[1]), None)
            if piece_2 is None and piece_1 is None:
                legal_moves.append((location[0] - 2, location[1]))

            piece = self.state1.get((location[0] - 1, location[1] + 1), None)
            if piece is not None and piece > 384:
                legal_moves.append((location[0] - 1, location[1] + 1))

            piece = self.state1.get((location[0] - 1, location[1] - 1), None)
            if piece is not None and piece > 384:
                legal_moves.append((location[0] - 1, location[1] - 1))

        elif piece_type == self.BLACK_KNIGHT:
            legal_moves.append((location[0] + 2, location[1] + 1))
            legal_moves.append((location[0] + 2, location[1] - 1))
            legal_moves.append((location[0] - 2, location[1] + 1))
            legal_moves.append((location[0] - 2, location[1] - 1))
            legal_moves.append((location[0] - 1, location[1] + 2))
            legal_moves.append((location[0] + 1, location[1] + 2))
            legal_moves.append((location[0] - 1, location[1] - 2))
            legal_moves.append((location[0] + 1, location[1] - 2))
        elif piece_type == self.BLACK_BISHOP:
            # calc-ing moving down to right
            can_move_further = True
            for line in range(7):
                move = (location[0] + line, location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up to right
            for line in range(7):
                move = (location[0] - line, location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving down and left
            for line in range(7):
                move = (location[0] + line, location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up and left
            for line in range(7):
                move = (location[0] - line, location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False

        elif piece_type == self.BLACK_ROOK:
            # calc-ing moving down
            can_move_further = True
            for line in range(7):
                move = (location[0] + line, location[1])
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up
            for line in range(7):
                move = (location[0] - line, location[1])
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving right
            for line in range(7):
                move = (location[0], location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving left
            for line in range(7):
                move = (location[0], location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False

        elif piece_type == self.BLACK_QUEEN:
            # calc-ing moving down to right
            can_move_further = True
            for line in range(7):
                move = (location[0] + line, location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up to right
            for line in range(7):
                move = (location[0] - line, location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving down and left
            for line in range(7):
                move = (location[0] + line, location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up and left
            for line in range(7):
                move = (location[0] - line, location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving down
            can_move_further = True
            for line in range(7):
                move = (location[0] + line, location[1])
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving up
            for line in range(7):
                move = (location[0] - line, location[1])
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving right
            for line in range(7):
                move = (location[0], location[1] + line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
            # calc-ing moving left
            for line in range(7):
                move = (location[0], location[1] - line)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    piece = self.state1.get(move)
                    # if there is not a piece at the location it is a valid move
                    if piece is None and can_move_further:
                        legal_moves.append(move)
                    elif not move == location:
                        can_move_further = False
        elif piece_type == self.BLACK_KING:
            # todo double check logic
            legal_moves.append((location[0] + 1, location[1]))
            legal_moves.append((location[0] + 1, location[1] + 1))
            legal_moves.append((location[0] + 1, location[1] - 1))
            legal_moves.append((location[0], location[1] + 1))
            legal_moves.append((location[0] - 1, location[1] + 1))
            legal_moves.append((location[0], location[1] - 1))
            legal_moves.append((location[0] - 1, location[1] - 1))
            legal_moves.append((location[0] - 1, location[1]))

        for move in legal_moves:
            # if the move is on the board (no negative values) it will be checked for legality
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                piece = self.state1.get(move)
                # if there is not a piece at the location it is a valid move
                if piece is None:
                    confirmed_legal_moves.append(move)
                # if there is a piece of the opposite color at the location it is a valid move
                # todo THIS WILL CAUSE PROBLEMS WITH PAWNS
                # todo this will also cause problems with bishops, queens
                elif (piece > 384 and color == Masks.BLACK) or (piece <= 384 and color == Masks.WHITE):
                    confirmed_legal_moves.append(move)

        confirmed_legal_moves.append(location)
        return confirmed_legal_moves

    def find_piece_type(self, location):
        return self.state1.get(location)

    # Attempting to make a private helper method to simplify rook, bishop, queen logic
    def calc_line_based_move(self, location, legal_moves):
        for line in range(7):
            move = (location[0], location[1] + line)
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                piece = self.state1.get(move)
                # if there is not a piece at the location it is a valid move
                if piece is None and can_move_further:
                    legal_moves.append(move)
                elif not move == location:
                    can_move_further = False

    def move_knight(self, loc0: tuple, loc1: tuple):
        pass

    def move_rook(self, loc0: tuple, loc1: tuple):
        pass

    def move_bishop(self, loc0: tuple, loc1: tuple):
        pass

    def move_king(self, loc0: tuple, loc1: tuple):
        pass

    def move_queen(self, loc0: tuple, loc1: tuple):
        pass

    def move_pawn(self, loc0: tuple, loc1: tuple):
        pass

    def move_piece(self, loc0: tuple, loc1: tuple, piece_type):
        self.state1.pop(loc0, None)
        self.state1[loc1] = piece_type

    def capture_piece(self, loc0: tuple, loc1: tuple, piece_type):
        self.state1.pop(loc0, None)
        self.state1[loc1] = piece_type
        self.pieces_in_play -= 1


def sim_input(board_matrix):
    i = int(input("enter desired matrix row "))
    j = int(input("enter desired matrix column "))
    answer = input("Type '1' for on, '0' for off ")
    if int(answer) == 1:
        board_matrix[i][j] = True
    else:
        board_matrix[i][j] = False


def run_board():
    # run = digitalio.DigitalInOut(board.D21)
    # run.direction = digitalio.Direction.INPUT

    run = True

    print("Starting board")
    chess_board = ChessBoard()

    while run:
        chess_board.print_matrix()
        chess_board.check_for_pick_up()
        sim_input(chess_board.board_matrix)


if __name__ == '__main__':
    run_board()
