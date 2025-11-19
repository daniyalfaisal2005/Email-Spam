import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================
# 1. Load & Clean Data
# ============================================

def load_data(filepath):
    df = pd.read_excel(filepath)

    df.columns = [col.lower() for col in df.columns]

    # Clean
    df = df.dropna(subset=['sender', 'reciever'])
    df['sender'] = df['sender'].str.strip().str.lower()
    df['reciever'] = df['reciever'].str.strip().str.lower()

    # Remove self-loops
    df = df[df['sender'] != df['reciever']]

    return df


# ============================================
# 2. Build Graph
# ============================================

def build_graph(df):
    G = nx.DiGraph()
    edges = list(zip(df['sender'], df['reciever']))
    G.add_edges_from(edges)
    return G


# ============================================
# 3. Compute Graph Metrics
# ============================================

def compute_metrics(G):
    metrics = pd.DataFrame({
        'node': list(G.nodes()),
        'out_degree': [G.out_degree(n) for n in G.nodes()],
        'in_degree': [G.in_degree(n) for n in G.nodes()],
        'degree_ratio': [G.out_degree(n) / (G.in_degree(n) + 1) for n in G.nodes()]
    })

    return metrics


# ============================================
# 4. Spam Detection Rule
# ============================================

def detect_spam(metrics):
    # Simple rule: spammer if out_degree extremely high OR degree ratio high
    metrics['spam_flag'] = metrics.apply(
        lambda row: "YES" if (row['out_degree'] > metrics['out_degree'].mean()*2
                              or row['degree_ratio'] > metrics['degree_ratio'].mean()*3)
        else "NO",
        axis=1
    )
    return metrics


# ============================================
# 5. Save Results
# ============================================

def save_results(metrics, output_file="spam_results.xlsx"):
    metrics.to_excel(output_file, index=False)

# ============================================
# 6. Visualization - Normal Graph
# ============================================

def visualize_graph(G, metrics):
    spam_nodes = set(metrics[metrics['spam_flag'] == "YES"]['node'])

    plt.figure(figsize=(16, 12))
    
    # Try multiple layout options and pick the best
    # Use spring_layout with larger k value to increase repulsion
    pos = nx.spring_layout(G, k=3, iterations=100, seed=42)
    
    # Alternative: Use shell_layout for circular arrangement
    # pos = nx.shell_layout(G)
    
    # Alternative: Use spectral_layout
    # pos = nx.spectral_layout(G)

    node_colors = ['red' if node in spam_nodes else 'green' for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.9)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, 
                          arrowstyle='->', arrowsize=25, width=1.5, 
                          connectionstyle='arc3,rad=0.1', alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

    plt.title("Email Network — Spammers in Red", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("graph_main.png", dpi=300, bbox_inches='tight')
    plt.show()
    print("Graph saved as graph_main.png")


# ============================================
# 7. Visualization — Bipartite Graph
# ============================================

def visualize_bipartite(df, metrics):
    B = nx.DiGraph()
    senders = set(df['sender'])
    receivers = set(df['reciever'])
    B.add_nodes_from(senders, bipartite=0)
    B.add_nodes_from(receivers, bipartite=1)
    for _, row in df.iterrows():
        B.add_edge(row['sender'], row['reciever'])

    spam_nodes = set(metrics[metrics['spam_flag'] == "YES"]['node'])
    
    # Compute out-degree for senders
    out_degree = dict(B.out_degree())

    # Node sizes proportional to out-degree (for senders) and in-degree (for receivers)
    node_sizes = []
    for node in B.nodes():
        if node in senders:
            node_sizes.append(out_degree.get(node, 1) * 150)
        else:
            node_sizes.append(max(1, B.in_degree(node)) * 150)

    # Manual bipartite layout: senders on left, receivers on right with good spacing
    pos = {}
    sender_list = sorted(list(senders))
    receiver_list = sorted(list(receivers))
    
    # Position senders on the left with vertical spacing
    for i, node in enumerate(sender_list):
        pos[node] = (0, -i * 2)
    
    # Position receivers on the right with vertical spacing
    for i, node in enumerate(receiver_list):
        pos[node] = (4, -i * 2)

    fig, ax = plt.subplots(figsize=(16, 12))
    node_colors = ['red' if node in spam_nodes else 'green' if node in senders else 'lightblue' for node in B.nodes()]
    
    # Draw nodes and edges separately
    nx.draw_networkx_nodes(B, pos, node_color=node_colors, node_size=node_sizes, alpha=0.85, ax=ax)
    nx.draw_networkx_edges(B, pos, edge_color='gray', arrows=True, 
                          arrowstyle='->', arrowsize=25, width=2, 
                          connectionstyle='arc3,rad=0.1', alpha=0.4, ax=ax)
    nx.draw_networkx_labels(B, pos, font_size=9, font_weight='bold', ax=ax)
    
    ax.set_title("Bipartite Email Network\nGreen: Senders (Left) | Blue: Receivers (Right) | Red: Spammers", 
                fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig("graph_bipartite.png", dpi=300, bbox_inches='tight')
    plt.show()

    print("Bipartite graph saved as graph_bipartite.png")


# ============================================
# Main Execution
# ============================================

if __name__ == "__main__":

    file_path = Path(r"E:\3 Semester\GT\email.xlsx")

    print("Loading data...")
    df = load_data(file_path)

    print("Building graph...")
    G = build_graph(df)

    print("Computing graph metrics...")
    metrics = compute_metrics(G)

    print("Detecting spam...")
    metrics = detect_spam(metrics)

    print("\nDetected Spammers:")
    print(metrics[metrics['spam_flag'] == "YES"])

    print("\nSaving results...")
    save_results(metrics)

    print("Visualizing normal graph...")
    visualize_graph(G, metrics)

    print("Visualizing bipartite graph...")
    visualize_bipartite(df, metrics)

    print("\n✔ All tasks completed successfully!")
