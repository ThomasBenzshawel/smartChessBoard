# import adafruit_blinka
# import board
# import digitalio
# import busio

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
        self.last_scan_status = "a1:rook;b1:knight;c1:bishop;"

        # These two lines are how all squares will be set up
        # a1 = digitalio.DigitalInOut(board.G1)
        # a1.direction = digitalio.Direction.INPUT

        # Initial board state
        self.state = {
            self.WHITE_PAWN: [],  # added in following loops
            self.WHITE_ROOK: [(0, 0), (0, 7)],
            self.WHITE_KNIGHT: [(0, 1), (0, 6)],
            self.WHITE_BISHOP: [(0, 2), (0, 5)],
            self.WHITE_QUEEN: [(0, 3)],  # If a pawn travels the length of the board, multiple queens can be on board
            self.WHITE_KING: (0, 4),  # However, there can only be one king of each color, so no list is used
            self.BLACK_PAWN: [],  # added in following loops
            self.BLACK_ROOK: [(7, 0), (7, 7)],
            self.BLACK_KNIGHT: [(7, 1), (7, 6)],
            self.BLACK_BISHOP: [(7, 2), (7, 5)],
            self.BLACK_QUEEN: [(7, 3)],
            self.BLACK_KING: (7, 4)
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

        self.serialized_game_state = self.serialize_state()  # store serialized state for faster access

        print("Testing the matrix")
        for row in self.board_matrix:
            print(row)

    def check_for_pick_up(self):
        # Checks the squares that were True and sees if they are still true
        # Alternate implementation is looking at the serialized board state and looking for differences
        pass

    def serialize_state(self) -> bytearray:
        # | 1 bit | 3 bits | 3 bits | 3 bits |
        # | color |  type  |   x    |    y   |
        ret = bytearray()
        for key, pieces in self.state.items():
            if not (key == self.BLACK_KING or key == self.WHITE_KING):
                for piece in pieces:
                    x_mask = piece[0] << 3
                    y_mask = piece[1]
                    ret.append(key | x_mask | y_mask)
            elif type(pieces) == tuple:  # piece is a king, so only one for each color (no list of tuples)
                x_mask = pieces[0] << 3
                y_mask = pieces[1]
                ret.append(key | x_mask | y_mask)
            else:
                raise ValueError("Unexpected type for King")
        return ret

    def load_state(self, state: bytearray):
        pass

    def user_move_piece(self, location, piece_type):
        # displays the correct moves the piece can make
        print(piece_type, "can move", self.find_legal_moves(location, piece_type))

        # Wait for any change in board state
        # If legal move, re-serialize the board state
        # If illegal move, alarm user and continue waiting until they make a legal move

    @staticmethod
    def find_legal_moves(location, piece_type):
        legal_moves = []
        # insert logic to calc legal moves
        print("Legal moves are:", legal_moves)
        return legal_moves

    def move_knight(self, loc0: tuple, loc1: tuple):
        pass

    def move_rook(self, loc0: tuple, loc1: tuple):
        pass

    def move_bishop(self, loc0: tuple, loc1: tuple):
        # validate starting and ending locations
        if not (self.validate_location(loc0) and self.validate_location(loc1)):
            raise ValueError("One or both of the given locations were invalid: " + str(loc0) + str(loc1))
        # verify that there is in fact a rook at this location
        if not (loc0 in self.state[self.WHITE_BISHOP] or loc0 in self.state[self.BLACK_BISHOP]):
            raise ValueError("Cannot move bishop from a location that does not have one")
        # verify that the move is legal for a rook
        slope = (loc0[1] - loc1[1]) / (loc0[0] - loc1[0])
        if slope != 1:
            raise ValueError("Bishop can only move diagonally")

        # since we've gotten to this point, we know that the move is legal
        self.board_matrix[loc0[1]][loc0[0]] = False
        self.board_matrix[loc1[1]][loc1[0]] = True

        if loc0 in self.state[self.WHITE_BISHOP]:
            key = self.WHITE_BISHOP
        else:  # Because of previous validation, we know that it must be contained in BLACK_BISHOP
            key = self.BLACK_BISHOP
        i = self.state[key].index(loc0)
        self.state[key].pop(i)
        self.state[key].insert(i, loc1)  # insert new location at same index as old location

    def move_king(self, loc0: tuple, loc1: tuple):
        # validate starting and ending locations
        if not (self.validate_location(loc0) and self.validate_location(loc1)):
            raise ValueError("One or both of the given locations were invalid: " + str(loc0) + str(loc1))
        # verify that there is in fact a rook at this location
        if not (loc0 in self.state[self.WHITE_KING] or loc0 in self.state[self.BLACK_KING]):
            raise ValueError("Cannot move bishop from a location that does not have one")
        # verify that the move is legal for a king
        dx = loc0[0] - loc1[0]
        dy = loc1[1] - loc1[1]
        if abs(dx) != 1 or abs(dy) != 1:  # TODO - implement castle procedure
            raise ValueError("Bishop can only move diagonally")

        # since we've gotten to this point, we know that the move is legal
        self.board_matrix[loc0[1]][loc0[0]] = False
        self.board_matrix[loc1[1]][loc1[0]] = True

        if loc0 in self.state[self.WHITE_KING]:
            key = self.WHITE_KING
        else:  # Because of previous validation, we know that it must be contained in BLACK_KING
            key = self.BLACK_KING
        i = self.state[key].index(loc0)
        self.state[key].pop(i)
        self.state[key].insert(i, loc1)  # insert new location at same index as old location

    def move_queen(self, loc0: tuple, loc1: tuple):
        pass

    def move_pawn(self, loc0: tuple, loc1: tuple):
        pass

    def validate_location(self, loc: tuple) -> bool:
        ret = True
        if len(loc) != 2:
            ret = False
        elif loc[0] < 0 or loc[0] > 7:
            ret = False
        elif loc[1] < 0 or loc[1] > 7:
            ret = False
        elif self.state[self.WHITE_KING] == loc or self.state[self.BLACK_KING] == loc:  # cannot capture a king
            ret = False
        return ret


def sim_input():
    answer = input("Type '1' for on, '0' for off")
    if int(answer) == 1:
        var = True
    else:
        var = False
    return var


def run_board():
    # run = digitalio.DigitalInOut(board.D21)
    # run.direction = digitalio.Direction.INPUT
    run = False

    run = True

    print("Starting board")
    chess_board = ChessBoard()

    while run:
        chess_board.check_for_pick_up()


if __name__ == '__main__':
    run_board()
