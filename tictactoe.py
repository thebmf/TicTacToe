import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):

    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == 'X':
                x_count += 1
            elif cell == 'O':
                o_count += 1

    if x_count > o_count:
        return 'O'
    else:
        return 'X'



def actions(board):

    possible_actions = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell not in ['X', 'O']:
                possible_actions.add((i, j))

    return possible_actions

def result(board, action):
    new_board = copy.deepcopy(board)
    i, j = action
    current_player = player(board)

    if board[i][j] not in ['X', 'O']:
        new_board[i][j] = current_player
    else:
        raise Exception("Invalid action")
    
    return new_board



def winner(board):
    def check_line(line):
        if line[0] is not EMPTY and all(element == line[0] for element in line):
            return line[0]
        return None


    # Check rows for a winner
    for row in board:
        row_winner = check_line(row)
        if row_winner:
            return row_winner

    # Check columns for a winner
    for col in range(len(board)):
        column = [board[row][col] for row in range(len(board))]
        col_winner = check_line(column)
        if col_winner:
            return col_winner

    # Check diagonals for a winner
    diagonal1 = [board[i][i] for i in range(len(board))]
    diagonal2 = [board[i][len(board)-i-1] for i in range(len(board))]
    diag1_winner = check_line(diagonal1)
    if diag1_winner:
        return diag1_winner
    diag2_winner = check_line(diagonal2)
    if diag2_winner:
        return diag2_winner

    return None


def terminal(board):
    if winner(board) is not None:
        return True

    for row in board:
        if any(cell is EMPTY for cell in row):
            return False

    return True



def utility(board):
    win = winner(board)
    if win == 'X':
        return 1
    elif win == 'O':
        return -1
    else:
        return 0



def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)

    def max_value(board):
        if terminal(board):
            return utility(board)
        v = float('-inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    if current_player == 'X':
        best_val = float('-inf')
        best_move = None
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_val:
                best_val = value
                best_move = action
    else:
        best_val = float('inf')
        best_move = None
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_val:
                best_val = value
                best_move = action

    return best_move