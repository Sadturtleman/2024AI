import pickle
import numpy as np
import time

from machines_p1 import P1
from machines_p2 import P2

dic = dict()
key = str()

players = {
    1: P1,
    2: P2
}

BOARD_ROWS = 4
BOARD_COLS = 4

# Initialize board and pieces
board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)

# MBTI Pieces (Binary Encoding: I/E = 0/1, N/S = 0/1, T/F = 0/1, P/J = 0/1)
pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]  # All 16 pieces
available_pieces = pieces[:]

# Global variable for selected piece
selected_piece = None

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

def check_line(line):
    if 0 in line:
        return False  # Incomplete line
    characteristics = np.array([pieces[piece_idx - 1] for piece_idx in line], dtype=object)
    for i in range(4):  # Check each characteristic (I/E, N/S, T/F, P/J)
        if len(set(characteristics[:, i])) == 1:  # All share the same characteristic
            return True
    return False

def check_2x2_subgrid_win():
    for r in range(BOARD_ROWS - 1):
        for c in range(BOARD_COLS - 1):
            subgrid = [board[r][c], board[r][c+1], board[r+1][c], board[r+1][c+1]]
            if 0 not in subgrid:  # All cells must be filled
                characteristics = [pieces[idx - 1] for idx in subgrid]
                for i in range(4):  # Check each characteristic (I/E, N/S, T/F, P/J)
                    if len(set(char[i] for char in characteristics)) == 1:  # All share the same characteristic
                        return True
    return False

def check_win():
    # Check rows, columns, and diagonals
    for col in range(BOARD_COLS):
        if check_line([board[row][col] for row in range(BOARD_ROWS)]):
            return True
    
    for row in range(BOARD_ROWS):
        if check_line([board[row][col] for col in range(BOARD_COLS)]):
            return True
        
    if check_line([board[i][i] for i in range(BOARD_ROWS)]) or check_line([board[i][BOARD_ROWS - i - 1] for i in range(BOARD_ROWS)]):
        return True

    # Check 2x2 sub-grids
    if check_2x2_subgrid_win():
        return True
    
    return False

def restart_game():
    global board, available_pieces, selected_piece, player

    board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)
    available_pieces = pieces[:]
    selected_piece = None  # Reset selected piece

# Game loop
turn = 1 
flag = "select_piece"
game_over = False
selected_piece = None

def piece_to_oct(piece):
    p = 0
    for i in range(1, 5):
        p += piece[4 - i] * (2 ** (i - 1))
    
    return str(p) if p >= 10 else '0' + str(p)




# 시뮬레이션 시행회수
t = 0
while t < 100000000000:

    if flag=="select_piece" and not game_over:

        player = players[3-turn](board=board, available_pieces=available_pieces)
        selected_piece = player.select_piece()

        flag = "place_piece"

        #추가 코드
        key += piece_to_oct(selected_piece)

    elif flag=="place_piece" and not game_over:

        player = players[turn](board=board, available_pieces=available_pieces)
        pos = player.place_piece(selected_piece)
        board_row = pos[0]
        board_col = pos[1]


        if available_square(board_row, board_col):
            # Place the selected piece on the board
            board[board_row][board_col] = pieces.index(selected_piece) + 1
            available_pieces.remove(selected_piece)
            selected_piece = None

            if check_win():
                game_over = True
                winner = turn
            elif is_board_full():
                game_over = True
                winner = None
            else:
                turn = 3 - turn
                flag = "select_piece"
        else:
            print(f"P{turn}; wrong selection")
        
        #추가 코드

        key += str(board_row) + str(board_col)


    if game_over:

        if winner:
            #추가 코드(player 1이 이기면 1점 2가 이기면 -1)

            dic[key] = 1 if winner == 1 else -1

        elif is_board_full():
            
            #추가 코드(무승부면 0점)
            dic[key] = 0
            
        restart_game()
        game_over = False
        turn = 1
        flag = 'select_piece'
        key = str()

        t += 1

        if t % 100000 == 0:  # 10만 회마다 저장
            print(t)
            with open(f'tuning{t // 100000 + 753}.pickle', 'wb') as file:
                pickle.dump(dic, file)
            
            dic.clear()
    
        time.sleep(0.0001)
        print(t)


    '''
    0312 형태로 key가 구성됨

    03은 03번 piece를 선택했다는 뜻
    12는 1,2위치에 배치했다는 뜻

    '''

