"""
Closeness Centrality Module

Calculates closeness centrality for identifying coordination hubs.

Concept:
Closeness centrality measures how close a node is to all other nodes.
- High closeness: Node has short average distance to others (central coordinator)
- Used for: Identifying central hubs in network

Application in spam detection:
- Spam ring coordinators often have high closeness
- Central hub sending coordinated spam campaigns
- Measure of network influence
"""

import networkx as nx
from typing import Dict
from core.directed_graph import DirectedEmailGraph


def calculate_closeness_centrality(graph: DirectedEmailGraph, distance: str = 'shortest_path') -> Dict[str, float]:
    """
    Calculate closeness centrality for all nodes.
    
    Closeness Centrality = 1 / (average distance to all other nodes)
    
    Formula: C_C(v) = (N-1) / sum(d(v, t)) for all t
    where:
    - N = number of nodes
    - d(v, t) = shortest path distance
    
    Args:
        graph: DirectedEmailGraph instance
        distance: Distance metric to use (currently supports 'shortest_path')
    
    Returns:
        Dictionary mapping node → closeness centrality (0 to 1)
    
    Interpretation:
    - High (0.7+): Central hub, close to many nodes
    - Medium (0.3-0.7): Moderately central
    - Low (<0.3): Peripheral, far from others
    """
    nx_graph = graph.to_networkx()
    
    # Convert to undirected for closeness calculation
    undirected = nx_graph.to_undirected()
    
    centrality = nx.closeness_centrality(undirected, distance='weight')
    
    return centrality


def get_top_closeness_nodes(
    graph: DirectedEmailGraph,
    top_n: int = 10
) -> list:
    """
    Get nodes with highest closeness centrality.
    
    These are likely central coordinators/hubs.
    
    Args:
        graph: DirectedEmailGraph instance
        top_n: Number of top nodes to return
    
    Returns:
        List of tuples (node, centrality) sorted by centrality descending
    """
    centrality = calculate_closeness_centrality(graph)
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    return sorted_nodes[:top_n]


def is_central_hub(graph: DirectedEmailGraph, node: str, threshold: float = 0.6) -> bool:
    """
    Check if a node is a central hub (high closeness).
    
    Args:
        graph: DirectedEmailGraph instance
        node: Node to check
        threshold: Centrality threshold for hub classification
    
    Returns:
        True if node's closeness centrality > threshold
    """
    centrality = calculate_closeness_centrality(graph)
    return centrality.get(node, 0) > threshold
