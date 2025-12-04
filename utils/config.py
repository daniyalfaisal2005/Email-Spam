"""
Configuration and constants for email spam detection system.
"""

# Spam Detection Thresholds
SPAM_SCORE_THRESHOLD = 80
SUSPICIOUS_SCORE_THRESHOLD = 40

# Degree Analysis
MIN_SPAM_OUT_DEGREE = 10
OUT_DEGREE_WEIGHT = 0.4

# Centrality Measures
CENTRALITY_WEIGHT = 0.35
BETWEENNESS_THRESHOLD = 0.3

# Temporal Analysis
BURST_DETECTION_THRESHOLD = 5
BURST_WEIGHT = 0.25

# Graph Visualization
MAX_NODES_FOR_DISPLAY = 5000
GRAPH_LAYOUT_ITERATIONS = 100

# Color Mapping for Node Classification
COLOR_SPAM = '#FF0000'           # Red
COLOR_SUSPICIOUS = '#FFFF00'     # Yellow
COLOR_LEGITIMATE = '#00AA00'     # Green
COLOR_MST_EDGE = '#FF6600'       # Orange

# Node Sizing
MIN_NODE_SIZE = 10
MAX_NODE_SIZE = 50

# Edge Properties
MIN_EDGE_WIDTH = 1
MAX_EDGE_WIDTH = 5

# MST Analysis
MST_EDGE_HIGHLIGHT_WIDTH = 3

# Bipartite Graph Settings
BIPARTITE_NODE_SIZE_RATIO = 1.5
