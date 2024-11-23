import pandas as pd
import tqdm
from tkinter import Tk, Canvas, Scrollbar, Frame

csvname = 'tree_merged_1to20_table.csv'
CUTTOTAL = 1
# CUTWINRATE = 0.7
# CUTLEVEL = 2
CUTROOT = 16 #출력할 루트노드 범위 설정

game = pd.read_csv(csvname)
game['Level'] = pd.to_numeric(game['Level'], errors='coerce')
game['Total Games'] = pd.to_numeric(game['Total Games'], errors='coerce')
game['Wins'] = pd.to_numeric(game['Wins'], errors='coerce')

game = game.dropna(subset=['Total Games', 'Wins', 'Level'])
game = game[game['Total Games'] > CUTTOTAL]
game['Win Rate'] = game['Wins'] / game['Total Games']

print("데이터 전처리 완료!")

def calculate_node_win_rate(root, game_df):
    children = get_children_nodes(game_df, root)
    if not children:
        return 0.0
    return sum(win_rate for _, win_rate in children) / len(children)

def get_children_nodes(game_df, parent_node):
    children = []
    for _, row in game_df.iterrows():
        play_log = str(row['Play Log']).split()
        if play_log[0] == parent_node and len(play_log) > 1:
            children.append((play_log[1], row['Win Rate']))
    return children

def get_full_tree(game_df, root, level=1, max_level=3, max_children=8):
    if level > max_level:
        return []
    children = get_children_nodes(game_df, root)
    children = sorted(children, key=lambda x: x[1], reverse=True)[:max_children]
    tree = [{"parent": root, "child": child, "win_rate": win_rate} for child, win_rate in children]
    for child, _ in children:
        tree.extend(get_full_tree(game_df, child, level + 1, max_level, max_children))
    return tree

def draw_tree(tree_data, max_level):
    window = Tk()
    window.title("Game Tree Visualization")

    frame = Frame(window)
    frame.pack(fill='both', expand=True)
    canvas_width = 1200
    canvas_height = 800 + (max_level - 3) * 200
    canvas = Canvas(frame, width=canvas_width, height=canvas_height, scrollregion=(0, 0, 2000, 2000))
    scrollbar_x = Scrollbar(frame, orient="horizontal", command=canvas.xview)
    scrollbar_y = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar_x.pack(side="bottom", fill="x")
    scrollbar_y.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    x_spacing = 200
    y_spacing = 100
    level_positions = {}

    def draw_node(node, level, x_pos, parent_coords=None, edge_label=None):
        y_pos = level * y_spacing + 50
        level_positions.setdefault(level, []).append(x_pos)

        canvas.create_oval(
            x_pos - 30, y_pos - 30, x_pos + 30, y_pos + 30,
            fill="skyblue", outline="black"
        )
        canvas.create_text(x_pos, y_pos, text=f"{node}", font=("Arial", 10, "bold"))

        if parent_coords:
            canvas.create_line(
                parent_coords[0], parent_coords[1] + 30, x_pos, y_pos - 30,
                arrow="last", fill="black"
            )
            if edge_label:
                mid_x = (parent_coords[0] + x_pos) / 2
                mid_y = (parent_coords[1] + y_pos) / 2
                canvas.create_text(mid_x, mid_y, text=f"{edge_label:.2f}", font=("Arial", 9), fill="red")
        return x_pos, y_pos

    def draw_tree_recursive(parent_node, current_level, parent_coords):
        if current_level > max_level:
            return
        children = [d for d in tree_data if d["parent"] == parent_node]
        num_children = len(children)

        if current_level not in level_positions:
            x_offset = 50
        else:
            x_offset = max(level_positions[current_level]) + x_spacing

        for i, child in enumerate(children):
            x_pos = x_offset + i * x_spacing
            child_coords = draw_node(child["child"], current_level, x_pos, parent_coords, edge_label=child["win_rate"])
            draw_tree_recursive(child["child"], current_level + 1, child_coords)

    root_coords = draw_node(selected_root, 1, canvas_width // 2)
    draw_tree_recursive(selected_root, 2, root_coords)

    window.mainloop()

while True:
    min_rate = input("승률 범위-최소값(0.0 ~ 1.0, 종료하려면 q): ")
    if min_rate.lower() == 'q':
        print("프로그램 종료!")
        break
    max_rate = input("승률 범위-최대값(0.0 ~ 1.0, 종료하려면 q): ")
    if max_rate.lower() == 'q':
        print("프로그램 종료!")
        break
    
    min_rate = float(min_rate)
    max_rate = float(max_rate)

    filtered_game = game[(game['Win Rate'] >= min_rate) & (game['Win Rate'] <= max_rate)]
    if filtered_game.empty:
        print(f"승률 범위 {min_rate:.2f} ~ {max_rate:.2f}에 해당하는 데이터가 없습니다.")
        continue

    root_nodes = (
        filtered_game['Play Log']
        .str.split().str[0]
        .value_counts()
        .index[:CUTROOT]
    )

    print(f"\n루트 노드 (상위 {CUTROOT}개, 승률 범위 {min_rate:.2f} ~ {max_rate:.2f}):")
    for idx, root in enumerate(root_nodes):
        avg_win_rate = calculate_node_win_rate(root, filtered_game)
        print(f"  [{idx}] 루트 노드: {root} | 확장 승률: {avg_win_rate:.2f}")

    root_idx = int(input("\n루트 노드를 선택(Index): "))
    selected_root = root_nodes[root_idx]

    max_children = int(input("시각화할 자식 노드의 최대 개수 입력(최소 1): "))
    max_level = int(input("트리 확장 깊이(최소 1): "))

    tree_data = get_full_tree(filtered_game, selected_root, max_level=max_level, max_children=max_children)

    if tree_data:
        draw_tree(tree_data, max_level)
    else:
        print(f"\n선택한 루트 노드 {selected_root}에서 확장 가능한 데이터X")
