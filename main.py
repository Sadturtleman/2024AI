import sys
import pygame
import numpy as np

from machines_p1 import P1
from machines_p2 import P2
import time

players = {
    1: P1,
    2: P2
}

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Highlight color for selected piece

# Proportions & Sizes
WIDTH = 400
HEIGHT = 700  # Increased height to display all 16 pieces
LINE_WIDTH = 5
BOARD_ROWS = 4
BOARD_COLS = 4
SQUARE_SIZE = WIDTH // BOARD_COLS
PIECE_SIZE = SQUARE_SIZE // 2  # Size for the available pieces

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MBTI Quarto')
screen.fill(BLACK)

# Initialize board and pieces
board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)

# MBTI Pieces (Binary Encoding: I/E = 0/1, N/S = 0/1, T/F = 0/1, P/J = 0/1)
pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]  # All 16 pieces
available_pieces = pieces[:]

# Global variable for selected piece
selected_piece = None

# Helper functions
def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, WIDTH), LINE_WIDTH)

def draw_pieces():
    font = pygame.font.Font(None, 40)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] != 0:
                piece_idx = board[row][col] - 1
                piece = pieces[piece_idx]
                piece_text = f"{'I' if piece[0] == 0 else 'E'}{'N' if piece[1] == 0 else 'S'}{'T' if piece[2] == 0 else 'F'}{'P' if piece[3] == 0 else 'J'}"
                text_surface = font.render(piece_text, True, WHITE)
                screen.blit(text_surface, (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 10))

def draw_available_pieces():
    global selected_piece  # Declare that we are using the global variable
    font = pygame.font.Font(None, 30)
    # Clear the area where available pieces are displayed
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, WIDTH, WIDTH, HEIGHT - WIDTH))
    
    for idx, piece in enumerate(available_pieces):
        col = idx % 4
        row = idx // 4
        piece_text = f"{'I' if piece[0] == 0 else 'E'}{'N' if piece[1] == 0 else 'S'}{'T' if piece[2] == 0 else 'F'}{'P' if piece[3] == 0 else 'J'}"
        if selected_piece == piece:
            text_surface = font.render(piece_text, True, YELLOW)
        else:
            text_surface = font.render(piece_text, True, BLUE)
        x_pos = col * SQUARE_SIZE + 10
        y_pos = WIDTH + (row * PIECE_SIZE) + 10
        screen.blit(text_surface, (x_pos, y_pos))

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
    characteristics = np.array([pieces[piece_idx - 1] for piece_idx in line])
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
    screen.fill(BLACK)
    draw_lines()
    board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)
    available_pieces = pieces[:]
    selected_piece = None  # Reset selected piece
    draw_available_pieces()
    display_message(f"Player {player}'s turn")

def display_message(message, color=WHITE):
    font = pygame.font.Font(None, 50)
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text_surface, text_rect)

def second2hhmmss(seconds):
    if seconds >= 3600:
        hh = seconds//3600
        mm = (seconds-(hh*3600))//60
        ss = seconds-(hh*3600)-(mm*60)
        return f"{hh:.0f}h {mm:.0f}m {ss:.1f}s"
    elif seconds >= 60:
        mm = seconds//60
        ss = seconds-(mm*60)
        return f"{mm:.0f}m {ss:.1f}s"
    else:
        return f"{seconds:.1f}s"

def display_time(total_time_consumption, color=GRAY):
    font = pygame.font.Font(None, 30)
    message = f"Player1: {second2hhmmss(total_time_consumption[1])} / Player2: {second2hhmmss(total_time_consumption[2])}"
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 90))
    screen.blit(text_surface, text_rect)

# Game loop
turn = 1 
flag = "select_piece"
game_over = False
selected_piece = None

total_time_consumption = {
    1: 0,
    2: 0
}

draw_lines()
draw_available_pieces()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and flag=="select_piece" and not game_over:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_SPACE]:
                begin = time.time()
                player = players[3-turn](board=board, available_pieces=available_pieces)
                selected_piece = player.select_piece()
                finish = time.time()
                total_time_consumption[3-turn]+=(finish-begin)
                flag = "place_piece"

        elif event.type == pygame.KEYDOWN and flag=="place_piece" and not game_over:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_SPACE]:
                begin = time.time()
                player = players[turn](board=board, available_pieces=available_pieces)
                (board_row, board_col) = player.place_piece(selected_piece)
                finish = time.time()
                total_time_consumption[turn]+=(finish-begin)

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                turn = 1 
                flag = "select_piece"
                total_time_consumption[1] = total_time_consumption[2] = 0

        if not game_over:
            draw_pieces()
            draw_available_pieces()
            if selected_piece:
                display_message(f"P{turn} placing pieces")
                display_time(total_time_consumption)
            else:
                display_message(f"P{3-turn} selecting pieces")
                display_time(total_time_consumption)
        else:
            draw_pieces()
            draw_available_pieces()
            if winner:
                display_message(f"Player {winner} Wins!", GREEN)
                display_time(total_time_consumption)
            elif is_board_full():
                display_message("Draw!", GRAY)
                display_time(total_time_consumption)

        pygame.display.update()