import pickle


def load_win_rate_data(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def find_highest_win_rate_position(turn_data, piece, excluded_positions):
    highest_win_rate = 0
    chosen_position = None

    for piece_position, win_rate in turn_data.items():
        if piece in piece_position and piece_position[2:] not in excluded_positions:
            if win_rate > highest_win_rate:
                highest_win_rate = win_rate
                chosen_position = piece_position[2:]  

    return chosen_position, highest_win_rate

def print_turn_info(turn, selector, placer, piece, position, piece_win_rate, position_win_rate):
    print(f"\n==== Turn {turn} ====")
    print(f"{selector}가 선택한 기물: '{piece}' (기물 승률: {piece_win_rate:.6f})")
    print(f"{placer}가 배치한 위치: '{position}' (위치 승률: {position_win_rate:.6f})")
    print("=================")

def simulate_game(location_win_rate_data, piece_win_rate_data, max_turns=16):
    excluded_pieces = set()      
    excluded_positions = set()   

    for turn in range(max_turns):
        if turn not in location_win_rate_data:
            print("\n게임 종료: 남은 턴 데이터가 없습니다.")
            break

        if turn % 2 == 0:
            selector = "Player 2"
            placer = "Player 1"
        else:
            selector = "Player 1"
            placer = "Player 2"

        lowest_piece = None
        lowest_piece_win_rate = float('inf')
        for piece, win_rate in piece_win_rate_data.get(turn, {}).items():
            if piece not in excluded_pieces and win_rate < lowest_piece_win_rate:
                lowest_piece = piece
                lowest_piece_win_rate = win_rate

        if not lowest_piece:
            print(f"\n{selector}가 선택할 수 있는 기물이 없습니다. 게임 종료.")
            break

        turn_data = location_win_rate_data[turn]
        chosen_position, highest_position_win_rate = find_highest_win_rate_position(
            turn_data, lowest_piece, excluded_positions
        )

        if not chosen_position:
            print(f"\n{placer}가 배치할 위치가 없습니다. 게임 종료.")
            break

        print_turn_info(turn + 1, selector, placer, lowest_piece, chosen_position, lowest_piece_win_rate, highest_position_win_rate)


        excluded_pieces.add(lowest_piece)  
        excluded_positions.add(chosen_position)  

location_file_path = 'location_based_win_rate.pickle'
piece_file_path = 'piece_based_win_rate.pickle'

location_win_rate_data = load_win_rate_data(location_file_path)
piece_win_rate_data = load_win_rate_data(piece_file_path)


simulate_game(location_win_rate_data, piece_win_rate_data)
