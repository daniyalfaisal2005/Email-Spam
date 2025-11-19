import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# Load dataset file
file_path = r"E:\3 Semester\GT\email.xlsx"
df = pd.read_excel(file_path)
df.columns = [col.lower() for col in df.columns]

# Create directed graph
G = nx.DiGraph()
for _, row in df.iterrows():
    sender = str(row['sender']).strip()
    receiver = str(row['reciever']).strip()
    G.add_edge(sender, receiver)

# Compute out-degree
out_degree = dict(G.out_degree())
total_users = len(G.nodes)
spammers = [node for node, deg in out_degree.items() if deg > total_users / 2]

# Create results DataFrame
results = pd.DataFrame({
    'sender': list(out_degree.keys()),
    'degree_out': list(out_degree.values()),
    'spam_flag': ['YES' if node in spammers else 'NO' for node in out_degree.keys()]
})

# Save results and zip
output_path = r"E:\3 Semester\GT\email_spam_results.xlsx"
results.to_excel(output_path, index=False)
print(f"Potential spammers: {spammers}")

# ------------------------
# Normal directed graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5)
node_colors = ['red' if node in spammers else 'green' for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500,
        arrowstyle='->', arrowsize=15)
plt.title("Email Network - Spammers in Red")
plt.show()

# ------------------------
# Enhanced bipartite graph
from networkx.algorithms import bipartite

B = nx.DiGraph()
senders = set(df['sender'])
receivers = set(df['reciever'])
B.add_nodes_from(senders, bipartite=0)
B.add_nodes_from(receivers, bipartite=1)
for _, row in df.iterrows():
    B.add_edge(row['sender'], row['reciever'])

# Node sizes proportional to out-degree (for senders) and in-degree (for receivers)
sender_sizes = [out_degree.get(node, 1)*100 for node in senders]
receiver_sizes = [max(1, B.in_degree(node))*100 for node in receivers]

# Position nodes: senders on left (x=0), receivers on right (x=1)
pos = {}
for i, node in enumerate(senders):
    pos[node] = (0, i)
for i, node in enumerate(receivers):
    pos[node] = (1, i)

plt.figure(figsize=(14, 10))
nx.draw(B, pos, with_labels=True,
        node_color=['red' if node in spammers else 'green' if node in senders else 'lightblue' for node in B.nodes()],
        node_size=[sender_sizes[i] if node in senders else receiver_sizes[i - len(senders)] 
                   for i, node in enumerate(B.nodes())],
        arrowstyle='->', arrowsize=20, edge_color='gray')
plt.title("Enhanced Bipartite Email Network - Red = Spammers, Green = Senders, Blue = Receivers")
plt.show()
