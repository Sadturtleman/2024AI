import pickle
from itertools import product
import os
import numpy as np
import random
import gzip

HASH_TABLE_PATH = "hash_table.msgpack.gz"

global_hash_table = None

play_log = []

place_dict = {
    "00": "0", "01": "1", "02": "2", "03": "3",
    "10": "4", "11": "5", "12": "6", "13": "7",
    "20": "8", "21": "9", "22": "A", "23": "B",
    "30": "C", "31": "D", "32": "E", "33": "F"
}

piece_dict = {
    "00": "0", "01": "1", "02": "2", "03": "3",
    "04": "4", "05": "5", "06": "6", "07": "7",
    "08": "8", "09": "9", "10": "A", "11": "B",
    "12": "C", "13": "D", "14": "E", "15": "F"
}
        
def load_global_hash_table(file_path):
    global global_hash_table
    if global_hash_table is not None:
        return global_hash_table

    if os.path.exists(file_path):
        try:
            with gzip.open(file_path, 'rb') as f:
                global_hash_table = pickle.load(f)
                print(f"해시 테이블 로드 완료: {len(global_hash_table)}개의 부모 노드")
        except Exception as e:
            raise Exception(f"해시 테이블 파일을 읽는 중 오류 발생: {e}")
    else:
        raise FileNotFoundError(f"해시 테이블 파일을 찾을 수 없습니다: {file_path}")
    
    return global_hash_table
    
def place_hex_to_tuple(hex_char):
    for key, value in place_dict.items():
        if value == hex_char:
            return tuple(map(int, key))

def piece_hex_to_binary(hex_char):
    key = next(key for key, value in piece_dict.items() if value == hex_char)
    return tuple(int(bit) for bit in format(int(key), '04b'))

def binary_place_tuple_to_hex(binary_tuple):
    hex_key = ''.join(map(str, binary_tuple))
    return place_dict[hex_key]

def binary_piece_tuple_to_hex(binary_tuple):
    decimal_value = int(''.join(map(str, binary_tuple)), 2)
    hex_value = hex(decimal_value)[2:].upper() 
    return hex_value

class P1():
    _instance = None

    def __new__(cls, *args, **kwargs):  # 싱글톤
        if not cls._instance:
            cls._instance = super(P1, cls).__new__(cls)
        return cls._instance

    def __init__(self, board, available_pieces, use_simulation_turns=4):
        if not hasattr(self, "initialized"):
            self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]  
            self.board = board  
            self.available_pieces = available_pieces          
            self.hash_table = load_global_hash_table(HASH_TABLE_PATH)
            
            self.simulation_turns = use_simulation_turns
            self.current_turn = 1
            self.play_log = []
            self.initialized = True
    
    def generate_place_log(self):
        currentPlace = [] 
        for row in range(4):
            for col in range(4):
                if self.board[row][col] != 0:
                    currentPlace.append((row, col))
        if play_log:  
            previous_state = list(map(place_hex_to_tuple, play_log))
        else:
            previous_state = []

        s1 = set(currentPlace)
        s2 = set(previous_state)  
        
        diff = list(s1 - s2)
        if diff:  # 차집합이 비어 있지 않으면
            place_str = ''.join([f"{x}{y}" for x, y in diff])  
            hex_value = binary_place_tuple_to_hex(place_str)  
            if hex_value:
                play_log.append(hex_value)
            else:
                print(f"Warning: No mapping found for place_str: {place_str}")
        else:
            print("Warning: No difference between currentPlace and previous_state.")
        
        return list(s2 - s1)
    
    def select_piece(self):
        play_log_str = ' '.join(map(str, play_log))

        if play_log_str in self.hash_table:
            best_child_piece_hex = self.hash_table[play_log_str]["best_child"]  
            try:
                piece_tuple = piece_hex_to_binary(best_child_piece_hex)
                return piece_tuple
            except ValueError:
                raise ValueError(f"Invalid piece hex value: {best_child_piece_hex}")
        else:
            print(f"해시 테이블에 해당 play_log가 없음: {play_log_str}.")
        # return random.choice(self.available_pieces) 
        
    def place_piece(self, selected_piece):
        play_log.append(binary_piece_tuple_to_hex(selected_piece)) 
        self.generate_place_log()

        play_log_str = ' '.join(map(str, play_log))

        if play_log_str in self.hash_table:
            best_child_place_hex = self.hash_table[play_log_str]["best_child"]
            try:
                place_tuple = place_hex_to_tuple(best_child_place_hex) 
                if place_tuple:
                    play_log.append(best_child_place_hex)
                    self.current_turn += 1 
                    return place_tuple
                else:
                    # 해시 테이블 데이터 자체에 best child node가 None인 데이터가 있음.
                    # 그래서 아래처럼 else에 랜덤 place를 선택하는 코드를 써야 된다고 생각.
                    available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col] == 0]
                    self.current_turn += 1
                    return random.choice(available_locs)
            except ValueError:
                raise ValueError(f"Invalid place hex value: {best_child_place_hex}")

        # 이후 minimax로 진행

    # jy 수정 코드 반영
    # 3개짜리 같은 속성을 가진 라인을 완성할 수 있는 위치를 찾음
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
