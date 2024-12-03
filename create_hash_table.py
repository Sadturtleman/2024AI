import pickle
import csv

input_csv = "finaltree.csv"
output_hash = "hash_table.pkl"

max_turns = 8

piece_dict = {
    "00": "0", "01": "1", "02": "2", "03": "3",
    "04": "4", "05": "5", "06": "6", "07": "7",
    "08": "8", "09": "9", "10": "A", "11": "B",
    "12": "C", "13": "D", "14": "E", "15": "F"
}

place_dict = {
    "00": "0", "01": "1", "02": "2", "03": "3",
    "10": "4", "11": "5", "12": "6", "13": "7",
    "20": "8", "21": "9", "22": "A", "23": "B",
    "30": "C", "31": "D", "32": "E", "33": "F"
}
def create_hash_table_from_tree(input_csv, max_turns):
    hash_table = {}

    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            level = int(row['Level'])
            if level > max_turns:
                continue

            play_log = row['Play Log'].strip().split()
            if len(play_log) < 2:
                continue

            parent_node = " ".join(play_log[:-1])
            current_node = play_log[-1]

            wins = int(row['Wins'])
            total_games = int(row['Total Games'])
            win_rate = wins / total_games if total_games > 0 else 0

            # 수정한 부분
            if parent_node not in hash_table:
                hash_table[parent_node] = {"best_child": None, "best_win_rate": -1,
                                           "worst_child": None, "worst_win_rate": 2}

            if win_rate >= 0.7 and win_rate > hash_table[parent_node]["best_win_rate"]:
                hash_table[parent_node]["best_child"] = current_node
                hash_table[parent_node]["best_win_rate"] = win_rate

            if win_rate <= 0.3 and win_rate < hash_table[parent_node]["worst_win_rate"]:
                hash_table[parent_node]["worst_child"] = current_node
                hash_table[parent_node]["worst_win_rate"] = win_rate

    return hash_table

hash_table = create_hash_table_from_tree(input_csv, max_turns)

with open(output_hash, 'wb') as f:
    pickle.dump(hash_table, f)

print(f"해시 테이블 생성 완료: {len(hash_table)}개의 부모 노드")
print(f"해시 테이블 저장 완료: {output_hash}")
