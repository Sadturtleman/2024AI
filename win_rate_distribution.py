#턴별 승률 도수분포
import pickle
from collections import defaultdict


def load_data(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data



def calculate_turn_based_cache(data):
    cache = defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0]))  
    
    for key, value in data.items():
        moves = [key[i:i+4] for i in range(0, len(key), 4)]
        
        for i, move in enumerate(moves):
            piece = move[:2]
            position = move[2:]
            
        
            if i % 2 == 0:  
                if value == 1:
                    cache[i][(piece, position)][0] += 1  
                cache[i][(piece, position)][1] += 1 
            else:  
                if value == -1:
                    cache[i][(piece, position)][2] += 1 
                cache[i][(piece, position)][3] += 1 

    return cache

def print_turn_data(turn_cache, turn):
    if turn not in turn_cache:
        print(f"턴 {turn+1}에 대한 데이터가 없습니다.")
        return
    
    print(f"---- 턴 {turn+1} ----")

    for (piece, position), (p1_wins, p1_total, p2_wins, p2_total) in turn_cache[turn].items():
        if turn % 2 == 0:
            p1_win_rate = p1_wins / p1_total if p1_total > 0 else 0
            print(f"Player 1 선택 - 기물: {piece}, 위치: {position}")
            print(f"  승률: {p1_win_rate:.4f} (승리 도수: {p1_wins}, 총 도수: {p1_total})")
        else:
            p2_win_rate = p2_wins / p2_total if p2_total > 0 else 0
            print(f"Player 2 선택 - 기물: {piece}, 위치: {position}")
            print(f"  승률: {p2_win_rate:.4f} (승리 도수: {p2_wins}, 총 도수: {p2_total})")
        
        print("\n-----------------------------\n")

def interactive_turn_view(turn_cache):
    
    while True:
        turn = input("보고 싶은 턴 번호를 입력하세요 (종료하려면 'q' 입력): ")
        if turn.lower() == 'q':
            break
        if not turn.isdigit():
            print("유효한 숫자를 입력하세요.")
            continue
        
        turn = int(turn)  
        print_turn_data(turn_cache, turn - 1)  

file_path = 'merged_dict.pickle'
data = load_data(file_path)


turn_based_cache = calculate_turn_based_cache(data)
interactive_turn_view(turn_based_cache)

