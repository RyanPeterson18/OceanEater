import sys
import chess
from ocean_eater_network import create_model
from decision_tree import make_decision


ENGINE_NAME = 'Ocean Eater 0.1'
AUTHOR_NAME = 'Ryan Peterson and Joshua Marsh'

# TODO: currently this doesn't actually search cap
DEFAULT_STATE_CAP = 1000
MIN_STATE_CAP = 50
MAX_STATE_CAP = 10000000

# initialize to empty string
# wait for uci command to be provided
while input().strip() != 'uci':
    pass  # do nothing


# Now, identify
print('id name ' + ENGINE_NAME)
print('id author ' + AUTHOR_NAME)

# Specify options
# State Cap is number of states
print('option name state_cap type spin default ' + str(DEFAULT_STATE_CAP) +
      ' min ' + str(MIN_STATE_CAP) +
      ' max ' + str(MAX_STATE_CAP))

# Done specifying options
print('uciok')

# get next command
command = input().strip()
state_cap = DEFAULT_STATE_CAP
ready = False
while not ready:
    if command.startswith('quit'):
        sys.exit()

    elif command.startswith('setoption'):
        # check what the 3rd word is
        if command.split()[2].strip() == 'state_cap':
            # 4th word is the value
            state_cap = int(command.split()[3].strip())

    elif command.startswith('isready'):
        ready = True
        print('readyok')

    command = input().strip()

have_board = False

board = chess.Board()
while not have_board:
    if command.startswith('quit'):
        sys.exit()

    elif command.startswith('setoption'):
        # check what the 3rd word is
        if command.split()[2].strip() == 'state_cap':
            # 4th word is the value
            state_cap = int(command.split()[4].strip())

    elif command.startswith('ucinewgame'):
        pass

    elif command.startswith('position'):
        # if second word is startpos
        if command.split()[1].strip() == 'startpos':
            have_board = True
            # if it has a list of moves
            if 'moves' in command:
                moves = command.split(' moves')[1]
                # apply moves to board
                for move in moves.split():
                    board.push(chess.Move.from_uci(move))

        # set from fen, command will be 'position fen <FEN> moves <MOVES>
        elif command.split()[1].strip() == 'fen':
            # get everything after 'fen' and before 'moves'
            fen = command[13:].split(' moves')[0]
            have_board = True
            board.set_fen(fen)  # set starting position
            # if it has a list of moves
            if 'moves' in command:
                moves = command.split(' moves')[1]
                # apply moves to board
                for move in moves.split():
                    board.push(chess.Move.from_uci(move))

    command = input().strip()

model = create_model()  # TODO: Later this should import a model
# TODO: for now, we can only play as white. Expand to black by mirroring.

while True:
    if command.startswith('quit'):
        sys.exit()

    elif command.startswith('setoption'):
        # check what the 3rd word is
        if command.split()[2].strip() == 'state_cap':
            # 4th word is the value
            state_cap = int(command.split()[4].strip())

    elif command.startswith('ucinewgame'):
        pass

    elif command.startswith('position'):
        # if second word is startpos
        if command.split()[1].strip() == 'startpos':
            have_board = True
            # if it has a list of moves
            if 'moves' in command:
                moves = command.split(' moves')[1]
                # apply moves to board
                for move in moves.split():
                    board.push(chess.Move.from_uci(move))

        # set from fen, command will be 'position fen <FEN> moves <MOVES>
        elif command.split()[1].strip() == 'fen':
            # get everything after 'fen' and before 'moves'
            fen = command[13:].split(' moves')[0]
            have_board = True
            board.set_fen(fen)  # set starting position
            # if it has a list of moves
            if 'moves' in command:
                moves = command.split(' moves')[1]
                # apply moves to board
                for move in moves.split():
                    board.push(chess.Move.from_uci(move))

    elif command.startswith('go'):
        move = chess.Move.uci(make_decision(model, board))
        print('bestmove' + move)

    command = input().strip()
