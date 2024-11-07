import numpy as np
import random
from itertools import product

import time

class P2():
    def __init__(self, board, available_pieces):
        self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]  # All 16 pieces
        self.board = board # Include piece indices. 0:empty / 1~16:piece
        self.available_pieces = available_pieces # Currently available pieces in a tuple type (e.g. (1, 0, 1, 0))
    
    def select_piece(self):
        # Make your own algorithm here
 # Check time consumption (Delete when you make your algorithm)

        return random.choice(self.available_pieces)

    def place_piece(self, selected_piece):
        # selected_piece: The selected piece that you have to place on the board (e.g. (1, 0, 1, 0)).
        
        # Available locations to place the piece
        available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

        # Make your own algorithm here
 # Check time consumption (Delete when you make your algorithm)
        
        return random.choice(available_locs)