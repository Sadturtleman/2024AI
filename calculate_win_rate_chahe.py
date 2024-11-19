import pickle
from collections import defaultdict

def load_data(file_path):

    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def calculate_turn_cache(data):
   
    piece_based_cache = defaultdict(lambda: defaultdict(lambda: [0, 0]))  
    location_based_cache = defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0]))  

    for key, value in data.items():
        moves = [key[i:i+4] for i in range(0, len(key), 4)]  

        for turn_num, move in enumerate(moves):
            piece = move[:2]
            position = move[2:]

            
            if value == 1:  
                piece_based_cache[turn_num][piece][0] += 1
            piece_based_cache[turn_num][piece][1] += 1

            
            if turn_num % 2 == 0:  
                if value == 1:
                    location_based_cache[turn_num][(piece, position)][0] += 1
                location_based_cache[turn_num][(piece, position)][1] += 1
            else:  
                if value == -1:
                    location_based_cache[turn_num][(piece, position)][2] += 1
                location_based_cache[turn_num][(piece, position)][3] += 1

    return piece_based_cache, location_based_cache

def save_win_rate_data(piece_cache, location_cache, piece_save_path, location_save_path):
   
    piece_win_rate_data = defaultdict(dict)
    for turn_num, pieces in piece_cache.items():
        for piece, (wins, total) in pieces.items():
            win_rate = wins / total if total > 0 else 0
            piece_win_rate_data[turn_num][piece] = win_rate

    with open(piece_save_path, 'wb') as file:
        pickle.dump(piece_win_rate_data, file)
    print(f"기물 기반 승률 데이터를 '{piece_save_path}'에 저장했습니다.")

   
    location_win_rate_data = defaultdict(dict)
    for turn_num, moves in location_cache.items():
        for (piece, position), (p1_wins, p1_total, p2_wins, p2_total) in moves.items():
            if turn_num % 2 == 0:  
                win_rate = p1_wins / p1_total if p1_total > 0 else 0
            else:  
                win_rate = p2_wins / p2_total if p2_total > 0 else 0
            location_win_rate_data[turn_num][f"{piece}{position}"] = win_rate

    with open(location_save_path, 'wb') as file:
        pickle.dump(location_win_rate_data, file)
    print(f"위치 기반 승률 데이터를 '{location_save_path}'에 저장했습니다.")

file_path = 'merged_dict.pickle'
piece_save_path = 'piece_based_win_rate.pickle'
location_save_path = 'location_based_win_rate.pickle'

data = load_data(file_path)
piece_cache, location_cache = calculate_turn_cache(data)

save_win_rate_data(piece_cache, location_cache, piece_save_path, location_save_path)
