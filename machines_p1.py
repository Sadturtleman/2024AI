import numpy as np
import random
from itertools import product
import tool

class P1():
    def __init__(self, board, available_pieces):
        self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]  # All 16 pieces
        self.board = board # Include piece indices. 0:empty / 1~16:piece
        self.available_pieces = available_pieces # Currently available pieces in a tuple type (e.g. (1, 0, 1, 0))


    def select_piece(self):

        available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

        notcheckmateposition = tool.find_notcheckmate_piece(self.board, self.available_pieces, available_locs)

        if bool(notcheckmateposition):
            self.available_pieces = notcheckmateposition

        #기보가 level 6(16 - 8) 전까진 랜덤으로 진행        
        if len(available_locs) >= 12:
            return random.choice(self.available_pieces)

        piece, _ = tool.minimax(self.board, self.available_pieces, available_locs)
        
        return piece

    def place_piece(self, selected_piece):

        available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

        checkmate_position = tool.find_checkmate_place(self.board, selected_piece, available_locs)
        if bool(checkmate_position):
            return checkmate_position[0]

        # 기보가 level (16 - 10) 전까진 랜덤으로 진행
        if len(available_locs) >= 12:
            return random.choice(available_locs)
        
        data = tool.find_three(self.board)

        for index, (r, c) in enumerate(available_locs):
            self.board[r][c] = self.pieces.index(selected_piece) + 1
            if tool.check_win(self.board):
                for temp in data:
                    if temp[1][0] == r and temp[1][1] == c:
                        num = tool.find_piece_by_point(self.board, self.available_pieces)[index]

                        if num % 2 == 0:
                            return (r, c)
                        
                        else:
                            available_locs[index] = (None, None)

            self.board[r][c] = 0

        # N이 3개 있을 때 S를 받은 경우 S가 짝수개 있으면 N을 막는 위치
        # N이 3개 있을 때 S를 받은 경우 S가 홀수개 있으면 N을 여는 위치
        
        available_locs = [item for item in available_locs if None not in item]

    
        place, _ = tool.minimax(self.board, self.available_pieces, available_locs, selected_piece, type = 'place')

        return place

