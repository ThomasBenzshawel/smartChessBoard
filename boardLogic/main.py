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

        # "a" column of squares
        a1 = True
        a2 = True
        a3 = False
        a4 = False
        a5 = False
        a6 = False
        a7 = False
        a8 = False
        a_column = [a1, a2, a3, a4, a5, a6, a7, a8]

        b1 = True

        c1 = True

        d1 = True

        e1 = True

        f1 = True

        g1 = True

        h1 = True

    def check_for_pick_up(self):
        # Checks the squares that were True and sees if they are still true
        # Alternate implementation is looking at the serialized board state and looking for differences
        print("Checking for picked up piece")

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

    print("Sim run")
    run = sim_input()

    chess_board = ChessBoard()

    while run:
        chess_board.check_change()
        print("Running")


if __name__ == '__main__':
    run_board()
