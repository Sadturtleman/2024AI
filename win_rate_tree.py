import pickle
from collections import defaultdict
from tqdm import tqdm
from collections import deque
import csv

queue = deque()

# 트리를 구성하는 각 노드 클래스
class Node: 
    def __init__(self):
        self.children = {}  # 자식 노드를 저장하는 딕셔너리
        self.total_games = 0  # 노드를 거친 총 게임 횟수
        self.wins = 0  # 해당 노드에서 총 이긴 횟수

def build_tree(data):  # 트리 생성
    '''
    Usage: 트리 생성
    Params: data (딕셔너리 데이터)
    '''
    root = Node()  # 루트 노드 생성
    # tick rate = 0.001
    for key, value in tqdm(data.items(), desc="Building Tree", unit="entry"):  # 데이터를 순회하며 트리 구축
        node = root  # 트리의 루트부터 시작
        for i in range(0, len(key), 4):  # key를 4자씩 끊어서 노드 생성
            part = key[i:i+4]  # 4자리씩 자른 문자열
            if part not in node.children:  # 현재 노드의 자식 노드에 part가 없는 경우
                node.children[part] = Node()  # 새로운 자식 노드 생성
            # node 처리
            if value == 1:  # player 1이 이긴 경우
                node.wins += 1
            node.total_games += 1  # 노드의 총 게임 횟수 증가
            node = node.children[part]  # 현재 노드를 자식 노드로 이동
        
        if value == 1:  # player 1이 이긴 경우
            node.wins += 1
        node.total_games += 1  # 노드의 총 게임 횟수 증가
        
    return root  # 완성된 트리 반환

def piece_dex_to_hex(dex_num):
    if (int(dex_num) < 10):
        return str(int(dex_num))
    else:
        return chr(int(dex_num) + 55)
    
def place_dex_to_hex(two_digit_num):
    if int(two_digit_num) < 10:
        return f"0{int(two_digit_num)}"  
    else:
        return chr(int(two_digit_num) + 55) 
    
def save_tree_to_file(node, writer, level=0, parent_key=""):
    if level == 0:  # 헤더 출력
        writer.writerow(['Level', 'Wins', 'Total Games', 'Play Log'])
    writer.writerow(
        [level, node.wins, node.total_games, parent_key]
    )
    for key, child in node.children.items():  # 자식 노드 순회
        piece_hex = piece_dex_to_hex(key[:2])
        place_hex = place_dex_to_hex(key[2:])
        updated_key = parent_key + piece_hex + place_hex + " "
        save_tree_to_file(child, writer, level + 1, updated_key)
    
# 1. 데이터 로드
with open('pickle_files/merged_dict_1to488.pickle', 'rb') as f:
    data = pickle.load(f)

# 2. 트리 생성
tree = build_tree(data)

# 3. 트리를 텍스트 파일로 저장
output_file_path = "./tree_merged_1to488_table.csv"
f = open(output_file_path, 'w')
writer = csv.writer(f)
save_tree_to_file(tree, writer)

print(f"트리 구조가 '{output_file_path}' 파일에 저장되었습니다.")
