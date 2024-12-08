import pickle
import csv

input_csv = "finaltree.csv"
# output_hash = "hash_table_less30_more70.pkl"
output_hash = "hash_table_less30_more70_short.pkl"

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
            level = int(row['Level'])  # Level
            if level > max_turns:
                continue

            play_log = row['Play Log'].strip().split()  # Play Log
            if len(play_log) < 2:
                continue

            parent_node = " ".join(play_log[:-1])
            current_node = play_log[-1]

            wins = int(row['Wins'])  # Wins
            total_games = int(row['Total Games'])  # Total Games
            win_rate = wins / total_games if total_games > 0 else 0

            # best_child (bc), best_win_rate(bwr), worst_child(wc), worst_win_rate(wwr)
            if parent_node not in hash_table:
                hash_table[parent_node] = {"bc": None, "bwr": -1,
                                           "wc": None, "wwr": 2}

            if win_rate >= 0.7 and win_rate > hash_table[parent_node]["bwr"]:
                hash_table[parent_node]["bc"] = current_node
                hash_table[parent_node]["bwr"] = round(win_rate, 4)

            if win_rate <= 0.3 and win_rate < hash_table[parent_node]["wwr"]:
                hash_table[parent_node]["wc"] = current_node
                hash_table[parent_node]["wwr"] = round(win_rate, 4)

    return hash_table

hash_table = create_hash_table_from_tree(input_csv, max_turns)

with open(output_hash, 'wb') as f:
    pickle.dump(hash_table, f)

print(f"해시 테이블 생성 완료: {len(hash_table)}개의 부모 노드")
print(f"해시 테이블 저장 완료: {output_hash}")
