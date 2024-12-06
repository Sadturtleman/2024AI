import random
from itertools import product
import tool

NUMBER = 11

class P2():
    def __init__(self, board, available_pieces):
        self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]  # All 16 pieces
        self.board = board # Include piece indices. 0:empty / 1~16:piece
        self.available_pieces = available_pieces # Currently available pieces in a tuple type (e.g. (1, 0, 1, 0))

    def select_piece(self):

        available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

        notcheckmateposition = tool.find_notcheckmate_piece(self.board, self.available_pieces, available_locs)

        if bool(notcheckmateposition):
            self.available_pieces = notcheckmateposition
        else:
            return random.choice(self.available_pieces)
        
        #기보가 level 6(16 - 8) 전까진 랜덤으로 진행        
        if len(available_locs) >= NUMBER:
            return random.choice(self.available_pieces)

        piece, _ = tool.minimax(self.board, self.available_pieces, available_locs, flag = 2)

        if piece  == None:
            return random.choice(self.available_pieces)
        
        return piece

    def place_piece(self, selected_piece):
        available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]


        checkmate_position = tool.find_checkmate_place(self.board, selected_piece, available_locs)
        if bool(checkmate_position):
            return checkmate_position[0]


        # 기보가 level (16 - 10) 전까진 랜덤으로 진행
        if len(available_locs) >= NUMBER:
            return random.choice(available_locs)

    
        place, _ = tool.minimax(self.board, self.available_pieces, available_locs, selected_piece, type = 'place', flag = 2)
        
        return place

