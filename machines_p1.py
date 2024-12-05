import pickle
from itertools import product
import os
import numpy as np
import random
import gzip
import ast

HASH_TABLE_PATH = "hash_table.msgpack.gz"

global_hash_table = None

play_log = []
previous_place_log = []

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
                hash_table_df = pickle.load(f)
                global_hash_table = dict(zip(hash_table_df['Key'], hash_table_df['Value']))
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
            self.previous_place_log = []
            self.initialized = True
    
    def generate_place_log(self):
        # 현재 턴에서 기물이 이미 올라가 있는 위치만 뽑아서 current_place_log에 기록
        current_place_log = [(row, col) for row in range(4) for col in range(4) 
                                                if self.board[row][col] != 0]

        s1 = set(current_place_log)
        s2 = set(self.previous_place_log)          
        diff = list(s1 - s2)  # current place가 previous place보다 더 많이 차 있음.
        print(f"[DEBUG] S1: s1={s1}")
        print(f"[DEBUG] S2: s2={s2}")
        print(f"[DEBUG] diff: diff={diff}")

        if diff:  # 차집합이 비어 있지 않으면
            place_str = ''.join([f"{x}{y}" for x, y in diff])  
            pair = diff[0] 
            hex_value = binary_place_tuple_to_hex((pair[0], pair[1]))  
            if hex_value:
                self.play_log.append(hex_value)
                play_log_str = " ".join(map(str, self.play_log))
                print(f"[DEBUG] place_piece: play_log_str={play_log_str}")
                print(f"[DEBUG] Hash table lookup result: {self.hash_table.get(play_log_str, 'Not Found')}")
            else:
                print(f"place_str에 맵핑되는 것이 없음.: {place_str}")
        else:
            print("current_place와 previous_state 간의 차집합이 비어있음.")
            available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col] == 0]
            self.play_log.append(binary_place_tuple_to_hex(random.choice(available_locs)))
            play_log_str = ' '.join(map(str, self.play_log))
            print(f"[DEBUG] place_piece: play_log_str={play_log_str}")
            print(f"[DEBUG] Hash table lookup result: {self.hash_table.get(play_log_str, 'Not Found')}")

        self.previous_place_log = current_place_log
        return list(s2 - s1)
    
    def select_piece(self):
        play_log_str = ' '.join(map(str, self.play_log))

        if play_log_str in self.hash_table:
            key_to_check = play_log_str
            value = self.hash_table.get(key_to_check)
            if isinstance(value, str):
                value = ast.literal_eval(value)  # 문자열을 딕셔너리로 변환
                self.hash_table[key_to_check] = value  # 변환된 값 업데이트
            worst_child_piece_hex = self.hash_table.get(play_log_str).get("worst_child")  
            try:
                piece_tuple = piece_hex_to_binary(worst_child_piece_hex)
                self.play_log.append(binary_piece_tuple_to_hex(piece_tuple))  # 상대방에게 골라준 worst 기물을 로그에 기록

                print(f"[DEBUG] place_piece: play_log_str={play_log_str}")
                print(f"[DEBUG] Hash table lookup result: {self.hash_table.get(play_log_str, 'Not Found')}")
                
                return piece_tuple
            except ValueError:
                raise ValueError(f"Invalid piece hex value: {worst_child_piece_hex}")
        else:
            print(f"해시 테이블에 해당 play_log가 없음: {play_log_str}")

            random_piece = random.choice(self.available_pieces)

            self.play_log.append(binary_piece_tuple_to_hex(random_piece)) 
            print(f"[DEBUG] place_piece: play_log_str={play_log_str}")
            print(f"[DEBUG] Hash table lookup result: {self.hash_table.get(play_log_str, 'Not Found')}")

            return random_piece
        
    def place_piece(self, selected_piece):
        # P2가 놓은 위치만 아래 함수로 호출할 방법 생각 
        if (self.current_turn % 2 == 0):
            self.generate_place_log()
            self.current_turn += 1

        self.play_log.append(binary_piece_tuple_to_hex(selected_piece)) # 상대방이 골라준 기물을 로그에 추가
        play_log_str = " ".join(map(str, self.play_log))
        print(f"[DEBUG] place_piece: play_log_str={play_log_str}")
        print(f"[DEBUG] Hash table lookup result: {self.hash_table.get(play_log_str, 'Not Found')}")

        if play_log_str in self.hash_table:
            value = self.hash_table.get(play_log_str)
            if isinstance(value, str):
                value = ast.literal_eval(value)  # 문자열을 딕셔너리로 변환
                self.hash_table[play_log_str] = value  # 변환된 값 업데이트
            best_child_place_hex = self.hash_table.get(play_log_str).get("best_child")
            try:
                place_tuple = place_hex_to_tuple(best_child_place_hex) 
                if place_tuple:
                    self.play_log.append(best_child_place_hex)  # 상대방이 골라준 기물을 놓는 위치를 로그에 기록

                    play_log_str = " ".join(map(str, self.play_log))
                    print(f"[DEBUG] place_piece: play_log_str={play_log_str}")
                    print(f"[DEBUG] Hash table lookup result: {self.hash_table.get(play_log_str, 'Not Found')}")
                    
                    # 이전 턴에서 P1이 놓은 기물 위치까지 기록된 로그에서 위치 로그만 뽑아서 튜플로 변환 
                    self.previous_place_log = list(map(place_hex_to_tuple, self.play_log))  # [start:end:stop]

                    self.current_turn += 1
                    return place_tuple
            except ValueError:
                raise ValueError(f"Invalid place hex value: {best_child_place_hex}")
        else:
            # 해시 테이블 데이터 자체에 best child node가 None인 데이터가 있음.
            # 그래서 아래처럼 else에 랜덤 place를 선택하는 코드를 써야 된다고 생각.
            available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col] == 0]
            random_place = random.choice(available_locs)
            self.play_log.append(binary_place_tuple_to_hex(random_place))
            
            play_log_str = " ".join(map(str, self.play_log))
            print(f"[DEBUG] place_piece: play_log_str={play_log_str}")
            print(f"[DEBUG] Hash table lookup result: {self.hash_table.get(play_log_str, 'Not Found')}")
            
            # 이전 턴에서 P1이 놓은 기물 위치까지 기록된 로그에서 위치 로그만 뽑아서 튜플로 변환 
            self.previous_place_log = list(map(place_hex_to_tuple, self.play_log))  # [start:end:stop]

            self.current_turn += 1
            return random_place

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
