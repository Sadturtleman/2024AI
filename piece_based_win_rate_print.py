import pickle


def load_data(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def display_turn_based_win_rate(file_path):
    turn_win_rate_data = load_data(file_path)
    
    print("각 턴별 기물 승률:")
    for turn_num, pieces in turn_win_rate_data.items():
        print(f"턴 {turn_num + 1}:")
        for piece, win_rate in pieces.items():
            print(f"  {piece}: {win_rate:.2f}")
        print()  

win_rate_file_path = 'piece_based_win_rate.pickle'
display_turn_based_win_rate(win_rate_file_path)
