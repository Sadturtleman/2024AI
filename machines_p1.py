import numpy as np
from itertools import product
import random

class P1:
    def __init__(self, board, available_pieces):
        self.board = board
        self.available_pieces = available_pieces
        self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]

    #3개짜리 같은 속성을 가진 라인을 완성할 수 있는 위치를 찾음
    def find_possible_line_positions(self):
        positions = []
        size = self.board.shape[0]

        for row in range(size):
            if list(self.board[row, :]).count(0) == 1: 
                empty_idx = list(self.board[row, :]).index(0)
                attributes = [
                    self.pieces[self.board[row, col] - 1] for col in range(size) if self.board[row, col] != 0
                ]
                for i in range(4):
                    if len(set(attr[i] for attr in attributes)) == 1:  
                        positions.append((row, empty_idx))
                        break

        for col in range(size):
            if list(self.board[:, col]).count(0) == 1:
                empty_idx = list(self.board[:, col]).index(0)
                attributes = [
                    self.pieces[self.board[row, col] - 1] for row in range(size) if self.board[row, col] != 0
                ]
                for i in range(4):
                    if len(set(attr[i] for attr in attributes)) == 1:
                        positions.append((empty_idx, col))
                        break

        return positions

       #특정 위치에서 플레이어에게 유리한지, 상대방에게 유리한지 평가.
    def evaluate_line_advantage(self, positions):
        advantage = {"P1": False, "P2": False}
        for pos in positions:
            row, col = pos
            temp_board = self.board.copy()
            temp_board[row][col] = self.pieces.index(self.available_pieces[0]) + 1
            if self.check_win(temp_board):
                advantage["P1"] = True
            else:
                opponent_piece = random.choice(self.available_pieces)
                temp_board[row][col] = self.pieces.index(opponent_piece) + 1
                if self.check_win(temp_board):
                    advantage["P2"] = True
        return advantage

    #주어진 기물이 3개의 같은 속성을 만족하는 라인을 완성할 수 있는 위치를 찾음.
    def find_completing_line(self, selected_piece):
        
        completing_positions = []
        size = self.board.shape[0]

        for row, col in product(range(size), range(size)):
            if self.board[row, col] == 0:
                temp_board = self.board.copy()
                temp_board[row, col] = self.pieces.index(selected_piece) + 1
                if self.check_win(temp_board):
                    completing_positions.append((row, col))

        return completing_positions
    
    #상대방의 승리를 막기 위해 최선의 방어 위치와 기물을 선택.
    def determine_best_defense(self):
        for piece in self.available_pieces:
            for row, col in product(range(self.board.shape[0]), range(self.board.shape[1])):
                if self.board[row, col] == 0: 
                    temp_board = self.board.copy()
                    temp_board[row, col] = self.pieces.index(piece) + 1

                    opponent = 2  
                    if self.can_opponent_win(temp_board, opponent):
                        return {"piece": piece, "position": (row, col)}
        return None
    
    #특정 상태에서 상대방이 승리할 수 있는지 확인.
    def can_opponent_win(self, temp_board):
        for row, col in product(range(temp_board.shape[0]), range(temp_board.shape[1])):
            if temp_board[row, col] == 0:
                future_board = temp_board.copy()
                future_board[row, col] = self.pieces.index(self.available_pieces[0]) + 1
                if self.check_win(future_board):
                    return True
        return False

    def check_win(self, board):
        def check_line(line):
            if 0 in line:
                return False
            characteristics = np.array([self.pieces[piece_idx - 1] for piece_idx in line if piece_idx > 0])
            for i in range(4):
                if len(set(characteristics[:, i])) == 1:
                    return True
            return False

        # 가로, 세로, 대각선 확인
        for col in range(board.shape[1]):
            if check_line(board[:, col]):
                return True
        for row in range(board.shape[0]):
            if check_line(board[row, :]):
                return True
        if check_line([board[i, i] for i in range(board.shape[0])]) or check_line(
            [board[i, board.shape[0] - i - 1] for i in range(board.shape[0])]
        ):
            return True

        return False

    def select_piece(self):
       
        if not self.available_pieces:
            raise ValueError("No available pieces to select")
        selected_piece = random.choice(self.available_pieces)
        return selected_piece

    def place_piece(self, selected_piece):
        
        available_positions = [
            (row, col)
            for row, col in product(range(self.board.shape[0]), range(self.board.shape[1]))
            if self.board[row][col] == 0
        ]
        if not available_positions:
            raise ValueError("No available positions to place the piece")
        
        selected_position = random.choice(available_positions)
        return selected_position
