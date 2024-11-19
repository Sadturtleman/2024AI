import pickle

def load_win_rate_data(file_path):
    with open(file_path, 'rb') as file:
        win_rate_data = pickle.load(file)
    return win_rate_data


def print_turn_data(win_rate_data, turn):
    if turn not in win_rate_data:
        print(f"턴 {turn+1}에 대한 데이터가 없습니다.")
        return
    
    print(f"---- 턴 {turn+1} ----")

    for move, win_rate in win_rate_data[turn].items():
        piece = move[:2]
        position = move[2:]
        print(f"기물: {piece}, 위치: {position}")
        print(f"  승률: {win_rate:.4f}\n")
        
    print("-----------------------------\n")

def interactive_turn_view(win_rate_data):
    while True:
        turn = input("보고 싶은 턴 번호를 입력하세요 (종료하려면 'q' 입력): ")
        if turn.lower() == 'q':
            break
        if not turn.isdigit():
            print("유효한 숫자를 입력하세요.")
            continue
        
        turn = int(turn) - 1 
        print_turn_data(win_rate_data, turn)


file_path = 'location_based_win_rate.pickle' 
win_rate_data = load_win_rate_data(file_path)


interactive_turn_view(win_rate_data)
