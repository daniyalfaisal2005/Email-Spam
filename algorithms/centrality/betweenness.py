"""
Betweenness Centrality Module

Calculates betweenness centrality for identifying relay nodes.

Concept:
Betweenness centrality measures how often a node appears on shortest paths.
- High betweenness: Node is a "bridge" or relay between other nodes
- Used for: Identifying important intermediary nodes in network

Application in spam detection:
- Spammers often use relay nodes to hide origins
- High betweenness node = likely spam relay
- Blocking key relays can disrupt spam distribution
"""

import networkx as nx
from typing import Dict
from core.directed_graph import DirectedEmailGraph


def calculate_betweenness_centrality(graph: DirectedEmailGraph, normalized: bool = True) -> Dict[str, float]:
    """
    Calculate betweenness centrality for all nodes.
    
    Betweenness Centrality = fraction of shortest paths that pass through node.
    
    Formula: C_B(v) = sum of (σ_st(v) / σ_st) for all s,t pairs
    where:
    - σ_st = number of shortest paths from s to t
    - σ_st(v) = number of shortest paths from s to t through v
    
    Args:
        graph: DirectedEmailGraph instance
        normalized: If True, divide by (N-1)(N-2)/2 to get values in range [0,1]
    
    Returns:
        Dictionary mapping node → betweenness centrality
    
    Interpretation:
    - 0: Node is not on any shortest paths (peripheral)
    - 0.5+: Node is on many shortest paths (central relay)
    - 1.0: Node is on all shortest paths (critical intermediary)
    """
    nx_graph = graph.to_networkx()
    
    # Convert to undirected for centrality calculation
    # (betweenness in directed graphs is more complex)
    undirected = nx_graph.to_undirected()
    
    centrality = nx.betweenness_centrality(undirected, normalized=normalized, weight='weight')
    
    return centrality


def get_top_betweenness_nodes(
    graph: DirectedEmailGraph,
    top_n: int = 10,
    normalized: bool = True
) -> list:
    """
    Get nodes with highest betweenness centrality.
    
    These are likely relay/intermediary nodes.
    
    Args:
        graph: DirectedEmailGraph instance
        top_n: Number of top nodes to return
        normalized: Whether to use normalized centrality
    
    Returns:
        List of tuples (node, centrality) sorted by centrality descending
    """
    centrality = calculate_betweenness_centrality(graph, normalized=normalized)
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    return sorted_nodes[:top_n]


def is_bridge_node(graph: DirectedEmailGraph, node: str, threshold: float = 0.3) -> bool:
    """
    Check if a node is a bridge node (high betweenness relay).
    
    Args:
        graph: DirectedEmailGraph instance
        node: Node to check
        threshold: Centrality threshold for bridge classification
    
    Returns:
        True if node's betweenness centrality > threshold
    """
    centrality = calculate_betweenness_centrality(graph, normalized=True)
    return centrality.get(node, 0) > threshold
