import pandas as pd
import networkx as nx
import pygraphviz as pgv
import matplotlib.pyplot as plt

file_path = "tree_merged_1to20_table.csv"
df = pd.read_csv(file_path)

# 승리한 게임 배치가 최소 1인 데이터만 필터링
df_filtered = df[df['Wins'] >= 1]

# 트리 깊이 설정
max_depth = 5
df_filtered = df_filtered[df_filtered['Level'] <= max_depth]
df_filtered["Win Rate"] = df_filtered["Wins"] / df_filtered["Total Games"]

G = nx.DiGraph()

for _, row in df_filtered.iterrows():
    log_parts = row["Play Log"].split() if pd.notna(row["Play Log"]) else []
    parent = " ".join(log_parts[:-1]) if len(log_parts) > 1 else "Root"
    current = row["Play Log"] if row["Play Log"] else "Root"
    win_rate = row["Win Rate"] if row["Total Games"] > 0 else 0
    label = f"{current}\n({win_rate:.2%})"
    
    G.add_node(current, label=label, win_rate=win_rate)
    
    if parent != "Root" or current == "Root":
        G.add_edge(parent, current)

pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

labels = nx.get_node_attributes(G, 'label')
colors = [G.nodes[node]['win_rate'] for node in G.nodes]
node_sizes = [1000 + (min(5000, G.nodes[node]['win_rate'] * 5000)) for node in G.nodes]

plt.figure(figsize=(15, 10))
nx.draw(
    G, pos, with_labels=False, node_color=colors,
    cmap=plt.cm.coolwarm, node_size=node_sizes, alpha=0.9, edge_color="gray"
)

nx.draw_networkx_labels(G, pos, labels, font_size=8)

plt.title("Node-Link Diagram of Win Rates")
plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.coolwarm), label="Win Rate")

plt.show()
