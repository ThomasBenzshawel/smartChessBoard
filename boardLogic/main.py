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

        # These two lines are how all squares will be set up
        # a1 = digitalio.DigitalInOut(board.G1)
        # a1.direction = digitalio.Direction.INPUT

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

        if len(checked_dict) != 32:
            # get the piece not on the board
            original_set = set(self.state1.items())
            checked_set = set(checked_dict.items())
            difference = original_set ^ checked_set
            picked_up_piece = list(difference)[0]  #Provides a list where the 0th term is the cords, and the 1st is type
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
        making_move = True
        print(piece_type, "can move to ", self.find_legal_moves(location, piece_type))

        # Wait for any change in board state
        while(making_move):
            pass
        # If legal move, re-serialize the board state

        # If illegal move, alarm user and continue waiting until they make a legal move


    def find_legal_moves(self, location, piece_type):
        legal_moves = []
        # insert logic to calc legal moves white pieces
        # todo need to add logic to check if somethin is there
        if piece_type == self.WHITE_PAWN:
            legal_moves.append((location[0] + 2, location[1]))
            legal_moves.append((location[0] + 1, location[1]))
        elif piece_type == self.WHITE_KNIGHT:
            legal_moves.append((location[0] + 2, location[1] + 1))
            legal_moves.append((location[0] + 2, location[1] - 1))
            legal_moves.append((location[0] - 2, location[1] + 1))
            legal_moves.append((location[0] - 2, location[1] - 1))
            legal_moves.append((location[0] - 1, location[1] + 2))
            legal_moves.append((location[0] + 1, location[1] + 2))
            legal_moves.append((location[0] - 1, location[1] - 2))
            legal_moves.append((location[0] + 1, location[1] - 2))
        elif piece_type == self.WHITE_ROOK:
            pass
        return legal_moves

    def find_piece_type(self, location):
        return self.state1.get(location)

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
