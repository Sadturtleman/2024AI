import pickle
from itertools import product
import os
import random
import ast
import tool
import zstandard as zstd
import pandas as pd

# csv_to_gzip
# HASH_TABLE_PATH = "hash_table_less30_more70.msgpack.gz"

# csv_to_zstd
# HASH_TABLE_PATH = 'hash_table_less30_more70.pickle.zst'
# HASH_TABLE_PATH = 'hash_table_less30_more70_short.pickle.zst'
HASH_TABLE_PATH = 'hash_table_less45_more55_short_asymmetric_lv8.pickle.zst'
# HASH_TABLE_PATH = 'hash_table_less45_more55_short_asymmetric_lv8.pickle.zst'

# csv_to_parquet
# HASH_TABLE_PATH = 'hash_table_less30_more70.parquet'

NUMBER = 13

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

opposite_piece_map = {
    "0": "F", "1": "E", "2": "D", "3": "C", 
    "4": "B", "5": "A", "6": "9", "7": "8", 
    "8": "7", "9": "6", "A": "5", "B": "4", 
    "C": "3", "D": "2", "E": "1", "F": "0"
}
        
def load_global_hash_table(file_path):
    global global_hash_table
    if global_hash_table is not None:
        return global_hash_table

    if os.path.exists(file_path):
        try:
            # csv_to_zstd
            with open(file_path, 'rb') as f:
                decompressor = zstd.ZstdDecompressor()
                decompressed_data = decompressor.decompress(f.read())
                hash_table_df = pickle.loads(decompressed_data)
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
            # self.hash_table = load_global_hash_table(HASH_TABLE_PATH)
            self.hash_table = hash_table
            
            self.simulation_turns = use_simulation_turns
            self.current_turn = 1
            self.play_log = []
            self.previous_place_log = []
            self.initialized = True

    def convert_to_opposite_and_sort(self, parent_node):
        parent_node = parent_node.split()
        remaining = parent_node[-1:] if len(parent_node) % 2 != 0 else []  # parent_node 구성 요소가 홀수 개일 때

        pieces_positions = [(opposite_piece_map[piece], place) for piece, place 
                            in zip(parent_node[::2], parent_node[1::2])]

        sorted_opposite_pieces_positions = sorted(pieces_positions, key=lambda x: x[0])
        sorted_opposite_node = " ".join(
            [" ".join(pair) for pair in sorted_opposite_pieces_positions] + remaining
        )
        return sorted_opposite_node

    def sort_parent_node_by_piece(self, parent_node):
        parent_node = parent_node.split()
        remaining = [] 
        if len(parent_node) % 2 != 0:  # parent_node 구성 요소가 홀수 개일 때
            remaining = [parent_node.pop()]  # 마지막 요소를 저장

        # parent_node 를 piece-place 쌍으로 분리
        pieces_positions = [(parent_node[i], parent_node[i + 1]) for i in range(0, len(parent_node), 2)]
        # piece 기준으로 sorting
        sorted_pieces_positions = sorted(pieces_positions, key=lambda x: x[0])
        # sorting 된 결과를 다시 문자열로 변환
        sorted_node = " ".join([" ".join(pair) for pair in sorted_pieces_positions] + remaining)
        return sorted_node

    def get_piece_and_log(self, piece):
        hex_piece = binary_piece_tuple_to_hex(piece)
        self.play_log.append(hex_piece)

        play_log_str = ' '.join(self.play_log)
        sorted_play_log_str = self.sort_parent_node_by_piece(play_log_str)
        print(f"[P1 DEBUG] select_piece: play_log_str={play_log_str}")
        print(f"[P1 DEBUG] Hash table lookup result: {self.hash_table.get(sorted_play_log_str, 'Not Found')}")


    def get_place_and_log(self, place):
        hex_place = binary_place_tuple_to_hex(place)
        self.play_log.append(hex_place)

        play_log_str = ' '.join(self.play_log)
        sorted_play_log_str = self.sort_parent_node_by_piece(play_log_str)
        print(f"[P1 DEBUG] place_piece: play_log_str={play_log_str}")
        print(f"[P1 DEBUG] Hash table lookup result: {self.hash_table.get(sorted_play_log_str, 'Not Found')}")


    def generate_place_log(self):
        # 현재 턴에서 기물이 이미 올라가 있는 위치만 뽑아서 current_place_log에 기록
        current_place_log = [(row, col) for row in range(4) for col in range(4) 
                                                if self.board[row][col] != 0]

        s1 = set(current_place_log)
        s2 = set(self.previous_place_log)          
        diff = list(s1 - s2)  # current place가 previous place보다 더 많이 차 있음.
        print(f"[P1 DEBUG] S1: s1={s1}")
        print(f"[P1 DEBUG] S2: s2={s2}")
        print(f"[P1 DEBUG] diff: diff={diff}")

        if diff:  # 차집합이 비어 있지 않으면
            pair = diff[0] 
            if pair not in self.previous_place_log: 
                self.get_place_and_log(pair)
            
        else:
            print("current_place와 previous_state 간의 차집합이 비어있음.")
            available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col] == 0]
            random_place = random.choice(available_locs)
            self.get_place_and_log(random_place)

        self.previous_place_log = current_place_log
        return list(s2 - s1)
    
    def select_piece(self):
        play_log_str = ' '.join(map(str, self.play_log))
        sorted_play_log_str = self.sort_parent_node_by_piece(play_log_str)
        opposite_sorted_play_log_str = self.convert_to_opposite_and_sort(play_log_str)
        available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]
                
        notcheckmatepiece = tool.find_notcheckmate_piece(self.board, self.available_pieces, available_locs)
        
        if len(available_locs) >= NUMBER:
            if sorted_play_log_str in self.hash_table:
                value = self.hash_table.get(sorted_play_log_str)
                if isinstance(value, str):
                    value = ast.literal_eval(value)  # 문자열을 딕셔너리로 변환
                    self.hash_table[sorted_play_log_str] = value  # 변환된 값 업데이트
                worst_child_piece_hex = self.hash_table.get(sorted_play_log_str).get("wc")  # worst_child
                
                if worst_child_piece_hex is None:
                    available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

                    random_piece = random.choice(notcheckmatepiece)
                    self.get_piece_and_log(random_piece)
                    return random_piece
                else:
                    try:
                        piece_tuple = piece_hex_to_binary(worst_child_piece_hex)
                        self.get_piece_and_log(piece_tuple)
                        return piece_tuple
                    except ValueError:
                        raise ValueError(f"Invalid piece hex value: {worst_child_piece_hex}")
            elif opposite_sorted_play_log_str in self.hash_table:
                value = self.hash_table.get(opposite_sorted_play_log_str)
                if isinstance(value, str):
                    value = ast.literal_eval(value)  # 문자열을 딕셔너리로 변환
                    self.hash_table[opposite_sorted_play_log_str] = value  # 변환된 값 업데이트
                worst_child_piece_hex = self.hash_table.get(opposite_sorted_play_log_str).get("wc")  # worst_child
                
                if worst_child_piece_hex is None:
                    available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

                    random_piece = random.choice(notcheckmatepiece)
                    self.get_piece_and_log(random_piece)
                    return random_piece
                else:
                    try:
                        piece_tuple = piece_hex_to_binary(worst_child_piece_hex)
                        self.get_piece_and_log(piece_tuple)
                        return piece_tuple
                    except ValueError:
                        raise ValueError(f"Invalid piece hex value: {worst_child_piece_hex}")
            else:
                    random_piece = random.choice(notcheckmatepiece)
                    self.get_piece_and_log(random_piece)
                    return random_piece
        # len(available_locs) < NUMBER (Min-Max)
        else:
            available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]
            
            print("*** minmax select 수행.")
            piece, _ = tool.minimax(self.board, self.available_pieces, available_locs)

            if piece is None:
                random_piece = random.choice(notcheckmatepiece)
                self.get_piece_and_log(random_piece)
                return random_piece

            self.get_piece_and_log(piece)
            return piece 
        
    def place_piece(self, selected_piece):
        # P2가 놓은 위치만 아래 함수로 호출할 방법 생각 
        if (self.current_turn % 2 == 0):
            self.generate_place_log()
            self.current_turn += 1

        self.get_piece_and_log(selected_piece)

        play_log_str = ''.join(self.play_log)
        sorted_play_log_str = self.sort_parent_node_by_piece(play_log_str)
        opposite_sorted_play_log_str = self.convert_to_opposite_and_sort(play_log_str)
        available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

        checkmate_position = tool.find_checkmate_place(self.board, selected_piece, available_locs)
        if bool(checkmate_position):
            self.get_place_and_log(checkmate_position[0])
            self.previous_place_log = list(map(place_hex_to_tuple, self.play_log))  # [start:end:stop]
            self.current_turn += 1
            return checkmate_position[0]
        
        if len(available_locs) >= NUMBER:
            if sorted_play_log_str in self.hash_table:
                value = self.hash_table.get(sorted_play_log_str)
                if isinstance(value, str):
                    value = ast.literal_eval(value)  # 문자열을 딕셔너리로 변환
                    self.hash_table[sorted_play_log_str] = value  # 변환된 값 업데이트
                best_child_place_hex = self.hash_table.get(sorted_play_log_str).get("bc")  # best_child
                
                if best_child_place_hex is None:
                    available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

                    random_place = random.choice([item for item in available_locs if None not in item])
                    self.get_place_and_log(random_place)

                    # 이전 턴에서 P1이 놓은 기물 위치까지 기록된 로그에서 위치 로그만 뽑아서 튜플로 변환 
                    self.previous_place_log = list(map(place_hex_to_tuple, self.play_log))  # [start:end:stop]
                    self.current_turn += 1
                    return random_place
                else:
                    try:
                        place_tuple = place_hex_to_tuple(best_child_place_hex) 
                        if place_tuple:
                            self.get_place_and_log(place_tuple)

                            # 이전 턴에서 P1이 놓은 기물 위치까지 기록된 로그에서 위치 로그만 뽑아서 튜플로 변환 
                            self.previous_place_log = list(map(place_hex_to_tuple, self.play_log))  # [start:end:stop]

                            self.current_turn += 1
                            return place_tuple
                    except ValueError:
                        raise ValueError(f"Invalid place hex value: {best_child_place_hex}")
            elif opposite_sorted_play_log_str in self.hash_table:
                value = self.hash_table.get(opposite_sorted_play_log_str)
                if isinstance(value, str):
                    value = ast.literal_eval(value)  # 문자열을 딕셔너리로 변환
                    self.hash_table[opposite_sorted_play_log_str] = value  # 변환된 값 업데이트
                best_child_place_hex = self.hash_table.get(opposite_sorted_play_log_str).get("bc")  # best_child
                
                if best_child_place_hex is None:
                    available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

                    random_place = random.choice([item for item in available_locs if None not in item])
                    self.get_place_and_log(random_place)

                    # 이전 턴에서 P1이 놓은 기물 위치까지 기록된 로그에서 위치 로그만 뽑아서 튜플로 변환 
                    self.previous_place_log = list(map(place_hex_to_tuple, self.play_log))  # [start:end:stop]
                    self.current_turn += 1
                    return random_place
                else:
                    try:
                        place_tuple = place_hex_to_tuple(best_child_place_hex) 
                        if place_tuple:
                            self.get_place_and_log(place_tuple)

                            # 이전 턴에서 P1이 놓은 기물 위치까지 기록된 로그에서 위치 로그만 뽑아서 튜플로 변환 
                            self.previous_place_log = list(map(place_hex_to_tuple, self.play_log))  # [start:end:stop]

                            self.current_turn += 1
                            return place_tuple
                    except ValueError:
                        raise ValueError(f"Invalid place hex value: {best_child_place_hex}")
        # len(available_locs) < NUMBER (Min-Max)
        else:
            available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

            print("*** minmax place 수행.")
            place, _ = tool.minimax(self.board, self.available_pieces, available_locs, selected_piece, type = 'place')

            if place is not None:  # Minimax 결과가 유효한 경우
                self.get_place_and_log(place)
                self.previous_place_log = list(map(place_hex_to_tuple, self.play_log))
                self.current_turn += 1
                return place  
                         
        random_place = random.choice([item for item in available_locs if None not in item])
        self.get_place_and_log(random_place)

        # 이전 턴에서 P1이 놓은 기물 위치까지 기록된 로그에서 위치 로그만 뽑아서 튜플로 변환 
        self.previous_place_log = list(map(place_hex_to_tuple, self.play_log))  # [start:end:stop]
        self.current_turn += 1
        return random_place

print("게임에 필요한 해시 테이블 로드 중입니다. 로드 완료 메시지가 나올 때까지 잠시 기다려주세요.")
hash_table = load_global_hash_table(HASH_TABLE_PATH)
print("헤시 테이블 로그가 완료되었습니다. 게임 시작!")