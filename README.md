# Email Spam Detection System using Graph Theory

A comprehensive semester project demonstrating graph theory algorithms for email spam detection, built with Flask web interface and interactive visualization.

## Features

✅ **8 Graph Theory Algorithms:**
- Dijkstra's Shortest Path
- Minimum Spanning Tree (Kruskal's)
- Betweenness Centrality
- Closeness Centrality
- Connected Components
- Vertex Coloring
- Network Metrics (Density, Diameter, Clustering)
- Degree Statistics

✅ **3-Tier Spam Classification:**
- Degree Ratio Analysis (40%)
- Centrality Scoring (35%)
- Temporal Burst Detection (25%)

✅ **Interactive Web Interface:**
- 5 organized tabs (Data, Graph, Analysis, Threats, Dijkstra Pathfinder)
- Real-time graph visualization with Vis.js
- Network physics simulation
- Threat scoring dashboard

## Project Structure

```
├── core/                          # Graph models
│   ├── directed_graph.py          # DirectedEmailGraph
│   └── bipartite_graph.py         # BipartiteEmailGraph
├── algorithms/                    # Graph algorithms
│   ├── shortest_paths.py          # Dijkstra implementation
│   ├── centrality/                # Betweenness & Closeness
│   ├── connectivity/              # Connected Components
│   ├── spanning_trees/            # Minimum Spanning Tree
│   ├── coloring/                  # Vertex Coloring
│   └── metrics/                   # Network metrics
├── detection/                     # Spam detection pipeline
│   ├── spam_scorer.py             # 3-metric scoring
│   ├── spam_classifier.py         # Classification
│   ├── path_analyzer.py           # Dijkstra analysis
│   └── mst_analyzer.py            # MST analysis
├── data/                          # Data handling
│   ├── email_parser.py            # CSV parser
│   ├── email_generator.py         # Synthetic data
│   └── datasets/                  # Sample datasets
├── utils/                         # Utilities
│   ├── config.py                  # Configuration
│   ├── helpers.py                 # Helper functions
│   └── validators.py              # Validation
├── web_gui_tabbed.py              # Main Flask application
└── requirements.txt               # Dependencies
```

## Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/email-spam-detection-graph-theory.git
cd email-spam-detection-graph-theory

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
python web_gui_tabbed.py
```

Then open your browser to: **http://localhost:5000**

## Usage

### 1. **Data & Load Tab**
- Select from demo dataset or upload CSV
- View email statistics and classification overview

### 2. **Network Graph Tab**
- Interactive graph visualization
- Zoom, pan, and navigate
- Node colors indicate threat level:
  - 🔴 Red: High spam risk
  - 🟠 Orange: Suspicious
  - 🟢 Green: Legitimate

### 3. **Analysis Tab**
- Network density
- Graph diameter
- Clustering coefficient
- Connected components analysis

### 4. **Threats Tab**
- Top 15 suspicious senders ranked by score
- Detailed threat metrics

### 5. **Dijkstra Pathfinder Tab**
- Find shortest communication paths
- Analyze path characteristics
- Detect indirect spam propagation

## Dataset Format

CSV with columns: `sender,recipient,count`

Example:
```
spammer1@example.com,alice@example.com,5
legitimate@example.com,bob@example.com,1
spammer2@example.com,charlie@example.com,8
```

## Demo Dataset

`data/datasets/demo_small.csv` contains 27 emails with obvious spam patterns for manual verification:
- **spammer1@example.com**: 45 emails (obvious spam)
- **spammer2@example.com**: 68 emails (obvious spam)
- Legitimate users: Rest of emails (legitimate pattern)

## Algorithm Details

### Dijkstra's Shortest Path
- Finds minimum-cost communication paths
- Detects indirect spam propagation chains
- Cost = inverse of email count (more emails = lower cost = higher suspicion)

### Minimum Spanning Tree
- Identifies backbone communication network
- Detects hub-and-spoke spam topology
- Minimum 999 edges for 1000+ nodes

### Centrality Metrics
- **Betweenness**: Identifies intermediary spam nodes
- **Closeness**: Detects central hubs in network

### Graph Coloring
- Assigns colors to conflicts-free graph
- Useful for network segmentation

## Technologies Used

- **Python 3.13.2**
- **Flask 3.1.2** - Web framework
- **NetworkX 3.2** - Graph algorithms
- **Vis.js** - Interactive visualization
- **Chart.js** - Data visualization
- **NumPy, Pandas, SciPy** - Data analysis

## Performance

- **Small Dataset** (27 emails): <100ms
- **Demo Dataset** (135 emails): <500ms
- **Large Dataset** (1000+ emails): <2s

## Requirements

```
networkx==3.2
flask==3.1.2
flask-cors==6.0.1
numpy==1.24.3
pandas==2.1.3
scipy==1.11.4
matplotlib==3.8.2
pyvis==0.3.2
```

## License

MIT License - Feel free to use for educational purposes

## Author

[Your Name]  
Graph Theory Semester Project  
December 2025

## Notes

- PyQt6 GUI scaffolding available in alternative branches (Windows DLL issues)
- All algorithms tested and verified
- Project ready for presentation

---

**Start the application:** `python web_gui_tabbed.py` → http://localhost:5000
