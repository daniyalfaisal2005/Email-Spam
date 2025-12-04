"""
Vertex Coloring Module

Implements greedy vertex coloring algorithm for node classification.

Concept:
Graph coloring assigns colors to vertices such that no two adjacent vertices
share the same color. This is the graph coloring problem (NP-hard in general).

Greedy algorithm: Assign colors to nodes one by one, using smallest available color.
- Not optimal but fast (polynomial time)
- Good for approximation in our spam classification context

Application in spam detection:
- Color 0 (Red): Spam nodes
- Color 1 (Yellow): Suspicious nodes
- Color 2 (Green): Legitimate nodes

Constraint: Adjacent (connected) nodes should avoid same category when possible.
"""

import networkx as nx
from typing import Dict, List
from core.directed_graph import DirectedEmailGraph


def greedy_vertex_coloring(graph: DirectedEmailGraph) -> Dict[str, int]:
    """
    Perform greedy vertex coloring on the graph.
    
    Algorithm:
    1. For each node in arbitrary order:
       - Get colors of all neighbors
       - Assign smallest color not used by neighbors
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Dictionary mapping node → color (int)
    
    Note:
    - Returns valid coloring but not guaranteed to be optimal
    - Number of colors used may be more than chromatic number
    - Good for visualization and classification
    """
    nx_graph = graph.to_networkx()
    undirected = nx_graph.to_undirected()
    
    coloring = nx.greedy_color(undirected, strategy='largest_first')
    
    return coloring


def color_nodes_by_spam_score(
    graph: DirectedEmailGraph,
    spam_scores: Dict[str, float],
    thresholds: tuple = (40, 80)
) -> Dict[str, int]:
    """
    Assign colors to nodes based on spam scores.
    
    Args:
        graph: DirectedEmailGraph instance
        spam_scores: Dictionary mapping node → spam_score (0-100)
        thresholds: Tuple (low_threshold, high_threshold) for color boundaries
                   Default: (40, 80) means:
                   - Score 0-40: Color 0 (Green, Legitimate)
                   - Score 40-80: Color 1 (Yellow, Suspicious)
                   - Score 80-100: Color 2 (Red, Spam)
    
    Returns:
        Dictionary mapping node → color (0, 1, or 2)
    """
    low_threshold, high_threshold = thresholds
    coloring = {}
    
    for node in graph.get_nodes():
        score = spam_scores.get(node, 0)
        
        if score >= high_threshold:
            color = 2  # Red: Spam
        elif score >= low_threshold:
            color = 1  # Yellow: Suspicious
        else:
            color = 0  # Green: Legitimate
        
        coloring[node] = color
    
    return coloring


def get_color_distribution(coloring: Dict[str, int]) -> dict:
    """
    Get count of nodes for each color.
    
    Args:
        coloring: Dictionary mapping node → color
    
    Returns:
        Dictionary mapping color → count
    """
    distribution = {}
    for color in coloring.values():
        distribution[color] = distribution.get(color, 0) + 1
    
    return distribution


def get_nodes_by_color(coloring: Dict[str, int], color: int) -> List[str]:
    """
    Get all nodes with a specific color.
    
    Args:
        coloring: Dictionary mapping node → color
        color: Color value to filter by
    
    Returns:
        List of nodes with specified color
    """
    return [node for node, node_color in coloring.items() if node_color == color]


def validate_coloring(graph: DirectedEmailGraph, coloring: Dict[str, int]) -> bool:
    """
    Validate that coloring is proper (no adjacent nodes have same color).
    
    Args:
        graph: DirectedEmailGraph instance
        coloring: Dictionary mapping node → color
    
    Returns:
        True if coloring is valid (proper coloring)
    """
    nx_graph = graph.to_networkx()
    undirected = nx_graph.to_undirected()
    
    for u, v in undirected.edges():
        if coloring.get(u) == coloring.get(v):
            return False
    
    return True


def get_chromatic_number_approximation(graph: DirectedEmailGraph) -> int:
    """
    Get approximation of chromatic number (minimum colors needed).
    
    Uses greedy algorithm, so result is >= actual chromatic number.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Approximate chromatic number
    """
    coloring = greedy_vertex_coloring(graph)
    return max(coloring.values()) + 1 if coloring else 0
