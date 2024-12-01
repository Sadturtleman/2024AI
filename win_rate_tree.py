import pickle
from collections import defaultdict
from tqdm import tqdm
from collections import deque
import csv
import time

queue = deque()

piece_dict = {"00":"0", "01":"1", "02":"2", "03":"3",
              "04":"4", "05":"5", "06":"6", "07":"7",
              "08":"8", "09":"9", "10":"A", "11":"B",
              "12":"C", "13":"D", "14":"E", "15":"F"}
              
place_dict = {"00":"0", "01":"1", "02":"2", "03":"3", 
              "10":"4", "11":"5", "12":"6", "13":"7",
              "20":"8", "21":"9", "22":"A", "23":"B",
              "30":"C", "31":"D", "32":"E", "33":"F"}

def piece_dex_to_hex(dex_num):
    return piece_dict[dex_num]
    
def place_dex_to_hex(two_digit_num):
    return place_dict[two_digit_num]

def piece_dex_to_hex_reverse(hex_num):
    return [key for key, value in piece_dict.items() 
            if value == hex_num][0]

def place_dex_to_hex_reverse(two_digit_hex_num):
    return [key for key, value in place_dict.items() 
            if value == two_digit_hex_num][0]

# 트리를 구성하는 각 노드 클래스
class Node: 
    def __init__(self):
        self.children = {}  # 자식 노드를 저장하는 딕셔너리
        self.total_games = 0  # 노드를 거친 총 게임 횟수
        self.wins = 0  # 해당 노드에서 총 이긴 횟수

    def __repr__(self):
        return f"Node(wins={self.wins}, total_games={self.total_games}, children={len(self.children)})"

def build_tree(data):  # 트리 생성
    '''
    Usage: 트리 생성
    Params: data (딕셔너리 데이터)
    '''
    root = Node()  # 루트 노드 생성
    # tick rate = 0.001
    for key, value in tqdm(data.items(), desc="Building Tree", unit="entry"):  # 데이터를 순회하며 트리 구축
        node = root  # 트리의 루트부터 시작
        for i in range(0, len(key), 2):  # key를 2자씩 끊어서 노드 생성
            part = key[i:i+2]  # 2자리씩 자른 문자열
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
    
def save_tree_to_file(node, writer, level=0, parent_key="", flag=0):
    writer.writerow(
        [level, node.wins, node.total_games, parent_key]
    )
    for key, child in node.children.items():  # 자식 노드 순회
        # print(f"Key: {key}, Child: {repr(child)}")
        if flag == 0:  
            hex_key = piece_dex_to_hex(key)
            next_flag = 1
        else:  
            hex_key = place_dex_to_hex(key)
            next_flag = 0
        
        updated_key = parent_key + hex_key + " "
        save_tree_to_file(child, writer, level + 1, updated_key, next_flag)

start = time.time()
   
# 1. 데이터 로드
with open('pickle_files/merged_dict_951to1000.pickle', 'rb') as f:
# with open('pickle_files/tuning1.pickle', 'rb') as f:
    data = pickle.load(f)

# 2. 트리 생성
tree = build_tree(data)
print("트리 생성이 완료되었습니다.")

# 3. 트리를 텍스트 파일로 저장
output_file_path = "merged_csv/tree_merged_951to1000_table.csv"
# output_file_path = "./tuning1.csv"
with open(output_file_path, 'w', newline='') as f: 
    writer = csv.writer(f)
    writer.writerow(['Level', 'Wins', 'Total Games', 'Play Log'])
    save_tree_to_file(tree, writer)

print(f"트리 구조가 '{output_file_path}' 파일에 저장되었습니다.")

end = time.time()
elapsed_time = end - start
print("경과 시간: ",f"{elapsed_time:.5f} sec")