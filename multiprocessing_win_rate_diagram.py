import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import set_start_method, cpu_count, Pool

def get_pool_size():
    return cpu_count()

def split_games(df):
    games = []
    current_game = []
    prev_level = -1

    for _, row in df.iterrows():
        if row['Level'] < prev_level:
            if current_game:
                games.append(pd.DataFrame(current_game))  
                current_game = [] 
        current_game.append(row)
        prev_level = row['Level']

    if current_game: 
        games.append(pd.DataFrame(current_game))

    return games

def create_graph_from_chunk(chunk):
    G = nx.DiGraph()

    for _, row in chunk.iterrows():
        log_parts = row["Play Log"].split() if pd.notna(row["Play Log"]) else []
        parent = " ".join(log_parts[:-1]) if len(log_parts) > 1 else "Root"
        current = row["Play Log"] if pd.notna(row["Play Log"]) else "Root"
        win_rate = row["Win_Rate"]
        label = f"{current}\n({win_rate:.2%})"

        G.add_node(current, label=label, Win_Rate=win_rate)
        if parent != current: 
            G.add_edge(parent, current)
    
    return G

def process_game_chunk(game_chunk):
    game_chunk["Win_Rate"] = game_chunk.apply(
        lambda row: row["Wins"] / row["Total Games"] if row["Total Games"] > 0 else 0,
        axis=1
    )
    graph = create_graph_from_chunk(game_chunk)
    return graph

def merge_graphs(graphs):
    merged_graph = nx.DiGraph()
    for graph in graphs:
        merged_graph.add_nodes_from(graph.nodes(data=True))
        merged_graph.add_edges_from(graph.edges(data=True))
    return merged_graph


def get_layout_choice():
    
    return 'spectral_layout'  

def plot_graph(G, output_file):
    nodes_with_win_rate = [node for node in G.nodes if 'Win_Rate' in G.nodes[node]]
    labels = {node: G.nodes[node]['label'] for node in nodes_with_win_rate}
    colors = [G.nodes[node]['Win_Rate'] for node in nodes_with_win_rate]
    node_sizes = [1000 + min(5000, G.nodes[node]['Win_Rate'] * 5000) for node in nodes_with_win_rate]

    layout_choice = get_layout_choice()
    
    if layout_choice == 'spring_layout':
        pos = nx.spring_layout(G)
    elif layout_choice == 'spectral_layout':
        pos = nx.spectral_layout(G)
    elif layout_choice == 'kamada_kawai_layout':
        pos = nx.kamada_kawai_layout(G)
    else:
        pos = nx.spring_layout(G) 

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

def main():
    file_path = "tree_merged_1to20_table.csv"
    df = pd.read_csv(file_path)
    try:
        set_start_method('spawn')
    except RuntimeError:
        pass

    games = split_games(df)

    game_chunks = []
    for game in games:
        chunk_size = 300
        for start in range(0, len(game), chunk_size):
            game_chunks.append(game.iloc[start:start + chunk_size])

   
    pool_size = get_pool_size()
    print(f"Using {pool_size} processes for parallel processing.")
    
    pool = Pool(processes=pool_size) 
    graphs = pool.map(process_game_chunk, game_chunks)

    merged_graph = merge_graphs(graphs)

    output_file = "node_link_diagram_win_rate.png"
    plot_graph(merged_graph, output_file)

if __name__ == "__main__":
    main()
