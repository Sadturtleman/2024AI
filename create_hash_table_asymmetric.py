import pickle
import csv
from itertools import permutations

input_csv = "finaltree.csv"
output_hash = "hash_table_less30_more70_short_asymmetric_lv6.pkl"

max_turns = 6

append_count = 0  # hash table에 추가된 데이터 개수
skipped_count = 0  # hash table에 추가되지 않고 skip 된 데이터 개수

def sort_parent_node_by_piece(parent_node):
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

def create_hash_table_from_tree(input_csv, max_turns):
    global append_count, skipped_count
    hash_table = {}

    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            level = int(row['Level'])  # Level
            if level > max_turns:
                continue

            play_log = row['Play Log'].strip().split()  # Play Log
            if len(play_log) < 2:
                continue

            parent_node = " ".join(play_log[:-1])
            current_node = play_log[-1]

            # 승률 정보
            wins = int(row['Wins'])  # Wins
            total_games = int(row['Total Games'])  # Total Games
            win_rate = wins / total_games if total_games > 0 else 0

            sorted_parent_node = sort_parent_node_by_piece(parent_node)

            # 해시 테이블에 sorted_parent_node가 없다면 새로 추가
            if sorted_parent_node not in hash_table:
                hash_table[sorted_parent_node] = {"bc": None, "bwr": -1, "wc": None, "wwr": 2}
                print(f"Append new parent node: {sorted_parent_node} -> Current node: {current_node} ( Win rate: {win_rate:.4f} )")
                append_count = append_count + 1
            # 해시 테이블에 sorted_parent_node가 이미 있다면 Skip 
            else:
                print(f"******** Skipped Parent node: {parent_node} -> Current node: {current_node} ( Win rate: {win_rate:.4f} )")
                skipped_count = skipped_count + 1
                continue

            # 해시 테이블에 데이터 저장
            if win_rate >= 0.7 and win_rate > hash_table[sorted_parent_node]["bwr"]:
                hash_table[sorted_parent_node]["bc"] = current_node
                hash_table[sorted_parent_node]["bwr"] = round(win_rate, 4)

            if win_rate <= 0.3 and win_rate < hash_table[sorted_parent_node]["wwr"]:
                hash_table[sorted_parent_node]["wc"] = current_node
                hash_table[sorted_parent_node]["wwr"] = round(win_rate, 4)

    return hash_table

hash_table = create_hash_table_from_tree(input_csv, max_turns)

with open(output_hash, 'wb') as f:
    pickle.dump(hash_table, f)

print(f"해시 테이블 생성 완료: {len(hash_table)}개의 부모 노드")
print(f"해시 테이블 저장 완료: {output_hash}")
print(f"Append count: {append_count}")
print(f"Skipped count: {skipped_count}")
