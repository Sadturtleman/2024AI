import pickle
from itertools import product
import os
import numpy as np
import random

HASH_TABLE_PATH = "hash_table.pkl"

global_hash_table = None

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
            with open(file_path, 'rb') as f:
                global_hash_table = pickle.load(f)
                print(f"해시 테이블 로드 완료: {len(global_hash_table)}개의 부모 노드")
                return global_hash_table
        except Exception as e:
            raise Exception(f"해시 테이블 파일을 읽는 중 오류 발생: {e}")
    else:
        raise FileNotFoundError(f"해시 테이블 파일을 찾을 수 없습니다: {file_path}")

def place_hex_to_tuple(hex_char, place_dict=place_dict):
    for key, value in place_dict.items():
        if value == hex_char:
            return tuple(map(int, key))

def piece_hex_to_binary(hex_char, piece_dict=piece_dict):
    key = next(key for key, value in piece_dict.items() if value == hex_char)
    return tuple(int(bit) for bit in format(int(key), '04b'))

class P1:
    def __init__(self, board, available_pieces, use_simulation_turns=4):
        self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]
        self.board = board
        self.available_pieces = available_pieces
        self.hash_table = load_global_hash_table(HASH_TABLE_PATH)
        self.simulation_turns = use_simulation_turns
        self.current_turn = 1

    def generate_play_log(self):
        play_log = []
        for row in range(4):
            for col in range(4):
                if self.board[row][col] != 0:
                    hex_value = piece_dict[f"{self.board[row][col] - 1:02}"]
                    play_log.append(hex_value)
        play_log_str = ' '.join(play_log)
        print(f"Generated play_log (16진수): {play_log_str}")  # 디버깅용 출력
        return play_log_str


    def select_best_child(self, play_log):
        best_win_rate = -1
        best_child = None
        for key, value in self.hash_table.items():
            if play_log in key and self.current_turn % 2 == 1:  # 홀수 턴만 선택
                win_rate = value["win_rate"]
                if win_rate > best_win_rate:
                    best_win_rate = win_rate
                    best_child = value["best_child"]
        return best_child


    def select_piece(self):
        play_log = self.generate_play_log()
        if self.current_turn <= self.simulation_turns:
            best_child_piece_hex = self.select_best_child(play_log)
            if best_child_piece_hex:
                try:
                    return piece_hex_to_binary(best_child_piece_hex)
                except ValueError:
                    raise ValueError(f"Invalid piece hex value: {best_child_piece_hex}")
       
        #return random.choice(self.available_pieces)

    def place_piece(self, selected_piece):
        play_log = self.generate_play_log()
        if self.current_turn <= self.simulation_turns:
            best_child_place_hex = self.select_best_child(play_log)
            if best_child_place_hex:
                try:
                    self.current_turn += 1
                    return place_hex_to_tuple(best_child_place_hex)
                except ValueError:
                    raise ValueError(f"Invalid place hex value: {best_child_place_hex}")

        # 이후 minimax로 진행
        available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col] == 0]
        self.current_turn += 1
        #return random.choice(available_locs)
        
    # (1) 한 라인에 같은 속성이 3개 있는지 확인 및 반환
    def find_lines_with_three(self):
        lines_with_three = []
        for i in range(4):
            row = self.board[i, :]
            if list(row).count(0) == 1 and self.check_line(row):
                lines_with_three.append((i, list(row).index(0)))

            col = self.board[:, i]
            if list(col).count(0) == 1 and self.check_line(col):
                lines_with_three.append((list(col).index(0), i))

        main_diag = [self.board[i, i] for i in range(4)]
        anti_diag = [self.board[i, 3 - i] for i in range(4)]
        if main_diag.count(0) == 1 and self.check_line(main_diag):
            lines_with_three.append((main_diag.index(0), main_diag.index(0)))
        if anti_diag.count(0) == 1 and self.check_line(anti_diag):
            lines_with_three.append((anti_diag.index(0), 3 - anti_diag.index(0)))
        return lines_with_three
    
    # (2) 3개짜리 라인을 만들지 않고 둘 수 있는 최대의 개수 반환        
    def find_safe_positions(self):
        safe_positions = []
        for row, col in product(range(4), range(4)):
            if self.board[row][col] == 0:
                self.board[row][col] = 1
                if not self.find_lines_with_three():
                    safe_positions.append((row, col))
                self.board[row][col] = 0
        return safe_positions
    
    # (3) 체크메이트 기물 확인 및 반환
    def find_checkmate_positions(self):
        checkmate_positions = []
        for piece in self.available_pieces:
            for row, col in product(range(4), range(4)):
                if self.board[row][col] == 0:
                    self.board[row][col] = self.pieces.index(piece) + 1
                    if self.find_lines_with_three():
                        checkmate_positions.append((row, col))
                    self.board[row][col] = 0
        return checkmate_positions

    def check_line(self, line):
        if 0 in line:
            return False
        characteristics = np.array([self.pieces[piece - 1] for piece in line])
        for i in range(4):
            if len(set(characteristics[:, i])) == 1:
                return True
        return False
