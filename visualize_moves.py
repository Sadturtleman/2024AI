#지정한 범위에 해당하는 승률을 가진 기보들을 출력하는 프로구램
# 지정한 범위에 해당하는 승률을 가진 기물을 선택한 후, 
#해당 기물에서 확장 가능한 경우들 중 다시 지정한 범위에 해당하는 기물들을 출력하는 형식

import pickle
from collections import defaultdict
import matplotlib.pyplot as plt
import random
import time

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


def filter_and_plot_possible_moves(turn_cache, turn, win_rate_thresholds=[0.5, 0.55, 0.6, 0.7]):
    pieces = []
    positions = []
    p1_win_rates = []
    p2_win_rates = []

    for (piece, position), (p1_wins, p1_total, p2_wins, p2_total) in turn_cache[turn].items():
        p1_win_rate = p1_wins / p1_total if p1_total > 0 else 0
        p2_win_rate = p2_wins / p2_total if p2_total > 0 else 0

        for threshold in win_rate_thresholds:
            if threshold <= p1_win_rate <= threshold + 0.05 or threshold <= p2_win_rate <= threshold + 0.05:
                pieces.append(piece)
                positions.append(position)
                p1_win_rates.append(p1_win_rate)
                p2_win_rates.append(p2_win_rate)
                break  

    fig, ax = plt.subplots(figsize=(10, 6))


    ax.scatter(range(len(p1_win_rates)), p1_win_rates, color='blue', label='Player 1 Win Rate', alpha=0.7, s=50)
    ax.scatter(range(len(p2_win_rates)), p2_win_rates, color='orange', label='Player 2 Win Rate', alpha=0.7, s=50)


    for i, (piece, position) in enumerate(zip(pieces, positions)):
        ax.text(i, p1_win_rates[i], f'{piece} {position}', fontsize=8, ha='center', rotation=45)
        ax.text(i, p2_win_rates[i], f'{piece} {position}', fontsize=8, ha='center', rotation=45, color='gray')

    ax.set_xlabel('Selected Object')
    ax.set_ylabel('Win Rate')
    ax.set_title(f'Turn {turn + 1} Possible Moves Win Rates')
    ax.legend()
    ax.grid(alpha=0.3)


    ax.set_ylim(0.45, 1)

    plt.tight_layout()
    plt.show(block=False)
    plt.pause(1)



def interactive_filtered_turn_visualization(turn_cache):
    
    while True:
        turn = input("시각화할 턴 번호를 입력(종료하려면 'q' 입력): ")
        if turn.lower() == 'q':
            break
        if not turn.isdigit() or int(turn) < 1 or int(turn) > 16:
            print("1~16까지의 정수 입력")
            continue

        turn = int(turn) - 1  
        filter_and_plot_possible_moves(turn_cache, turn)
        time.sleep(1)


file_path = 'merged_dict.pickle'
data = load_data(file_path)

turn_based_cache = calculate_turn_based_cache(data)

interactive_filtered_turn_visualization(turn_based_cache)
