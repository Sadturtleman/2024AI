import pickle

with open('pickle_files/merged_dict.pickle', 'rb') as file:
    data = pickle.load(file)

dp = {}

for key, value in data.items():
    moves = [key[i:i+4] for i in range(0, len(key), 4)]
    
    for i, move in enumerate(moves):
        piece = move[:2]
        position = move[2:]
        
        if (i, piece, position) not in dp:
            dp[(i, piece, position)] = [0, 0, 0, 0]
        
        if i % 2 == 0: 
            if value == 1:
                dp[(i, piece, position)][0] += 1 
            dp[(i, piece, position)][1] += 1  
        else:  
            if value == -1:
                dp[(i, piece, position)][2] += 1
            dp[(i, piece, position)][3] += 1  

turn_win_rate = {}

for (turn, piece, position), (p1_wins, p1_total, p2_wins, p2_total) in dp.items():
    p1_win_rate = p1_wins / p1_total if p1_total > 0 else 0
    p2_win_rate = p2_wins / p2_total if p2_total > 0 else 0

    if turn not in turn_win_rate:
        turn_win_rate[turn] = [(p1_win_rate, piece, position), (p2_win_rate, piece, position)]
    else:
        if p1_win_rate > turn_win_rate[turn][0][0]:
            turn_win_rate[turn][0] = (p1_win_rate, piece, position)
        
        if p2_win_rate > turn_win_rate[turn][1][0]:
            turn_win_rate[turn][1] = (p2_win_rate, piece, position)

for turn, ((p1_win_rate, p1_piece, p1_position), (p2_win_rate, p2_piece, p2_position)) in turn_win_rate.items():
    if (turn % 2 == 0):
        print(f"Turn {turn+1:2d}에서 Player 1의 승률이 가장 높은 선택: piece {p1_piece}, position {p1_position}, 승률: {p1_win_rate:.4f}")
    else:
        print(f"Turn {turn+1:2d}에서 Player 2의 승률이 가장 높은 선택: piece {p2_piece}, position {p2_position}, 승률: {p2_win_rate:.4f}")
