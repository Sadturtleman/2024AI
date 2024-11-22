import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

file_path = "tree_merged_1to20_table.csv"
output_file = "node_link_diagram_win_rate.png"

df = pd.read_csv(file_path)

required_columns = ['Level', 'Wins', 'Total Games', 'Play Log']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"CSV 파일에 다음 열이 필요합니다: {required_columns}")

df_filtered = df[df['Wins'] >= 1]
df_filtered = df_filtered[df_filtered['Level'] <= 3]
df_filtered["Win_Rate"] = df_filtered.apply(
    lambda row: row["Wins"] / row["Total Games"] if row["Total Games"] > 0 else 0,
    axis=1
)

G = nx.DiGraph()

for _, row in df_filtered.iterrows():
    log_parts = row["Play Log"].split() if pd.notna(row["Play Log"]) else []
    parent = " ".join(log_parts[:-1]) if len(log_parts) > 1 else "Root"
    current = row["Play Log"] if pd.notna(row["Play Log"]) else "Root"
    win_rate = row["Win_Rate"]
    label = f"{current}\n({win_rate:.2%})"
    

    G.add_node(current, label=label, Win_Rate=win_rate)
    if parent != "Root" or current == "Root":
        G.add_edge(parent, current)

nodes_with_win_rate = [node for node in G.nodes if 'Win_Rate' in G.nodes[node]]

labels = {node: G.nodes[node]['label'] for node in nodes_with_win_rate}
colors = [G.nodes[node]['Win_Rate'] for node in nodes_with_win_rate]
node_sizes = [1000 + min(5000, G.nodes[node]['Win_Rate'] * 5000) for node in nodes_with_win_rate]

pos = nx.spring_layout(G)

for node in nodes_with_win_rate:
    if node not in pos:
        pos[node] = [0, 0]  

plt.figure(figsize=(15, 10))
vmin, vmax = 0, 1


nx.draw(
    G, pos, with_labels=False, nodelist=nodes_with_win_rate, node_color=colors, 
    vmin=vmin, vmax=vmax, cmap=plt.cm.coolwarm, node_size=node_sizes, alpha=0.9, edge_color="gray"
)

nx.draw_networkx_labels(G, pos, labels, font_size=8)

plt.title("Node-Link Diagram of Win Rates")
plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, norm=plt.Normalize(vmin=vmin, vmax=vmax)), label="Win_Rate")
plt.savefig(output_file, format="png", dpi=300)
print(f"Node-Link Diagram saved as {output_file}")
