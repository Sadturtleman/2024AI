import pickle
import pandas as pd
import gc

input_csv = "finaltree_lv8.csv"
output_hash = "hash_table_less45_more55_short_asymmetric_lv8.pkl"
max_turns = 9
batch_size = 10000  # 일정 개수마다 저장 및 해제

append_count = 0  # 해시 테이블에 추가된 데이터 개수
skipped_count = 0  # 해시 테이블에 추가되지 않고 skip 된 데이터 개수

opposite_piece_map = {
    "0": "F", "1": "E", "2": "D", "3": "C", 
    "4": "B", "5": "A", "6": "9", "7": "8", 
    "8": "7", "9": "6", "A": "5", "B": "4", 
    "C": "3", "D": "2", "E": "1", "F": "0"
}

def convert_to_opposite_and_sort(parent_node):
    parent_node = parent_node.split()
    remaining = parent_node[-1:] if len(parent_node) % 2 != 0 else []  # parent_node 구성 요소가 홀수 개일 때

    pieces_positions = [(opposite_piece_map[piece], place) for piece, place 
                        in zip(parent_node[::2], parent_node[1::2])]

    sorted_opposite_pieces_positions = sorted(pieces_positions, key=lambda x: x[0])
    sorted_opposite_node = " ".join(
        [" ".join(pair) for pair in sorted_opposite_pieces_positions] + remaining
    )
    return sorted_opposite_node

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

def handle_missing_values(df):
    # 각 열의 결측값 처리
    df['Level'] = df['Level'].fillna(0).astype(int)  # Level 열은 0으로 채우고 정수형 변환
    df['Wins'] = df['Wins'].fillna(0).astype(int)  # Wins 열은 0으로 채움
    df['Total Games'] = df['Total Games'].fillna(0).astype(int)  # Total Games 열은 0으로 채움
    df['Play Log'] = df['Play Log'].fillna("").astype(str)  # Play Log는 빈 문자열로 채움
    return df

def create_hash_table_from_tree(input_csv, max_turns, batch_size):
    global append_count, skipped_count
    hash_table = {}
    batch_counter = 0

    # CSV 파일을 판다스로 읽어오기
    df = pd.read_csv(input_csv)
    print("CSV 로드 완료")

    # 결측값 처리
    df = handle_missing_values(df)
    print("결측값 처리 완료")
    
    for _, row in df.iterrows():
        level = int(row['Level'])
        if level > max_turns:
            continue

        play_log = row['Play Log'].strip().split()
        if len(play_log) < 2:
            continue

        parent_node = " ".join(play_log[:-1])
        current_node = play_log[-1]

        # 승률 정보 계산
        wins = int(row['Wins'])
        total_games = int(row['Total Games'])
        win_rate = wins / total_games if total_games > 0 else 0

        sorted_parent_node = sort_parent_node_by_piece(parent_node)
        sorted_opposite_node = convert_to_opposite_and_sort(sorted_parent_node)
        
        if sorted_parent_node not in hash_table and sorted_opposite_node not in hash_table:
            # 새로운 노드 추가
            hash_table[sorted_parent_node] = {"bc": None, "bwr": -1, "wc": None, "wwr": 2}
            append_count += 1
        else:
            skipped_count += 1

        if sorted_parent_node in hash_table:
            # 승률에 따라 업데이트
            if win_rate > 0.55 and win_rate > hash_table[sorted_parent_node]["bwr"]:
                hash_table[sorted_parent_node]["bc"] = current_node
                hash_table[sorted_parent_node]["bwr"] = round(win_rate, 4)

            if win_rate <= 0.45 and win_rate < hash_table[sorted_parent_node]["wwr"]:
                hash_table[sorted_parent_node]["wc"] = current_node
                hash_table[sorted_parent_node]["wwr"] = round(win_rate, 4)        
            
        batch_counter += 1

        # 일정 개수마다 해시 테이블 저장 및 메모리 해제
        if batch_counter >= batch_size:
            save_partial_hash_table(hash_table, output_hash)
            hash_table.clear()
            gc.collect()
            batch_counter = 0
            print(f"Batch 저장 완료. Append count: {append_count}, Skipped count: {skipped_count}")

    # 마지막 남은 데이터를 저장
    if hash_table:
        save_partial_hash_table(hash_table, output_hash)

def save_partial_hash_table(hash_table, output_hash):
    try:
        with open(output_hash, 'ab') as f:
            pickle.dump(hash_table, f)
        print(f"Partial hash table saved. Current size: {len(hash_table)}")
    except Exception as e:
        print(f"Error saving hash table: {e}")

# 해시 테이블 생성
create_hash_table_from_tree(input_csv, max_turns, batch_size)

# 메모리 해제
gc.collect()

print(f"해시 테이블 생성 완료")
print(f"최종 해시 테이블 저장 완료: {output_hash}")
print(f"Append count: {append_count}")
print(f"Skipped count: {skipped_count}")
