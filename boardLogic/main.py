# import adafruit_blinka
# import board
# import digitalio
# import busio


class ChessBoard:
    def __init__(self):
        # Sets up the board state as the default starting state
        last_scan_status = "a1:rook;b1:knight;c1:bishop;"

        # These two lines are how all squares will be set up
        # a1 = digitalio.DigitalInOut(board.G1)
        # a1.direction = digitalio.Direction.INPUT

        board_matrix = [[0 for i in range(8)] for j in range(8)]

        for j in range(2):
            for i in range(8):
                board_matrix[j][i] = True

        for j in range(2, 6):
            for i in range(8):
                board_matrix[j][i] = False

        for j in range(6, 8):
            for i in range(8):
                board_matrix[j][i] = True

        print("Testing the matrix")
        for row in board_matrix:
            print(row)


    def check_for_pick_up(self):
        # Checks the squares that were True and sees if they are still true
        # Alternate implementation is looking at the serialized board state and looking for differences
        pass

    # ian implements
    def serialize_state(self):
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

    def move_knight(self, location):
        pass

    def move_rook(self, location):
        pass

    def move_bishop(self, location):
        pass

    def move_king(self, location):
        pass

    def move_queen(self, location):
        pass

    def move_pawn(self, location):
        pass


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
