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
            
            if value == 1:
                cache[i][(piece, position)][0] += 1
                cache[i][(piece, position)][1] += 1
            elif value == -1:
                cache[i][(piece, position)][2] += 1
                cache[i][(piece, position)][3] += 1
            else:
                cache[i][(piece, position)][1] += 1
                cache[i][(piece, position)][3] += 1
    return cache

def find_best_move_each_turn(turn_cache, excluded_pieces, excluded_positions):
    best_move = None
    best_win_rate = 0
    winning_player = None

    for (piece, position), (p1_wins, p1_total, p2_wins, p2_total) in turn_cache.items():
        if piece in excluded_pieces or position in excluded_positions:
            continue
        
        p1_win_rate = p1_wins / p1_total if p1_total > 0 else 0
        p2_win_rate = p2_wins / p2_total if p2_total > 0 else 0
        win_rate = max(p1_win_rate, p2_win_rate)
        
        if win_rate > best_win_rate:
            best_win_rate = win_rate
            best_move = (piece, position, win_rate)
            winning_player = "Player 1" if p1_win_rate > p2_win_rate else "Player 2"
    
    return best_move, winning_player

def build_optimal_move_sequence(turn_cache, max_turns=16):
    optimal_sequence = []
    excluded_pieces = set()
    excluded_positions = set()
    
    for turn in range(max_turns):
        best_move, winning_player = find_best_move_each_turn(turn_cache[turn], excluded_pieces, excluded_positions)
        
        if not best_move:
            break
        
        optimal_sequence.append((best_move, winning_player))
        
        piece, position, win_rate = best_move
        excluded_pieces.add(piece)
        excluded_positions.add(position)
    
    return optimal_sequence

def print_optimal_sequence(optimal_sequence):
    print("\nOptimal Move Sequence:")
    for turn, (move, winning_player) in enumerate(optimal_sequence):
        piece, position, win_rate = move
        print(f"Turn {turn + 1}: Piece: {piece}, Position: {position}, Win Rate: {win_rate:.2f}, Predicted Winner: {winning_player}")

file_path = 'merged_dict.pickle'  
data = load_data(file_path)
turn_based_cache = calculate_turn_based_cache(data)
optimal_sequence = build_optimal_move_sequence(turn_based_cache)
print_optimal_sequence(optimal_sequence)
