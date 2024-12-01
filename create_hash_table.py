import csv
import pickle

input_csv = "finaltree.csv"
output_hash = "hash_table.pkl"

max_turns = 8

def parse_play_log(log):
    return log.strip().split()

def create_hash_table(input_csv, max_turns):
    hash_table = {}
    
    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            level = int(row['Level'])
            if level > max_turns:
                continue 
            
            play_log = parse_play_log(row['Play Log'])
            if len(play_log) < 2:
                continue 
            
            parent_node = " ".join(play_log[:-1]) 
            current_node = play_log[-1]  
            wins = int(row['Wins'])
            total_games = int(row['Total Games'])
            win_rate = wins / total_games if total_games > 0 else 0
            
            if parent_node not in hash_table:
                hash_table[parent_node] = {"best_child": current_node, "best_win_rate": win_rate}
            else:
                if win_rate > hash_table[parent_node]["best_win_rate"]:
                    hash_table[parent_node] = {"best_child": current_node, "best_win_rate": win_rate}
    
    return {key: value["best_child"] for key, value in hash_table.items()}

hash_table = create_hash_table(input_csv, max_turns)

with open(output_hash, 'wb') as f:
    pickle.dump(hash_table, f)

print(f"해시 테이블 생성 완료: {len(hash_table)}개의 부모 노드")
print(f"파일 저장 완료: {output_hash}")
