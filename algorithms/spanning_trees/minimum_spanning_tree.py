"""
Minimum Spanning Tree Module

Computes minimum spanning tree using Kruskal's algorithm.

Concept:
Minimum Spanning Tree (MST) is a subset of edges that connects all nodes
with minimum total weight without forming cycles.

- Uses Kruskal's algorithm: Sort edges by weight, add edges that don't form cycles
- Time complexity: O(E log E)

Application in spam detection:
- Identifies backbone/core communication paths
- Shows essential communication structure
- Different MST patterns for spam vs. legitimate networks
"""

import networkx as nx
from typing import List, Tuple, Set
from core.directed_graph import DirectedEmailGraph


def compute_minimum_spanning_tree(graph: DirectedEmailGraph) -> 'DirectedEmailGraph':
    """
    Compute minimum spanning tree of email network.
    
    Uses Kruskal's algorithm to find MST with minimum total weight.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        New DirectedEmailGraph containing only MST edges
    
    Algorithm:
    1. Sort all edges by weight (ascending)
    2. For each edge in sorted order:
       - If edge connects two unconnected nodes, add it to MST
       - If edge would create cycle, skip it
    3. Continue until all nodes are connected
    
    Example use:
    - Full network: 1000 nodes, 5000 edges
    - MST: 1000 nodes, 999 edges (most important paths)
    """
    # Convert to undirected for MST calculation
    nx_graph = graph.to_networkx()
    undirected = nx_graph.to_undirected()
    
    # Compute MST (NetworkX handles disconnected graphs)
    try:
        mst = nx.minimum_spanning_tree(undirected, weight='weight', algorithm='kruskal')
    except nx.NetworkXError:
        # Fallback if graph is empty or has issues
        mst = nx.Graph()
    
    # Convert back to DirectedEmailGraph
    result = DirectedEmailGraph()
    for u, v, data in mst.edges(data=True):
        # Add edge in both directions to preserve symmetry
        weight = data.get('weight', 1)
        result.add_email(u, v, weight)
        result.add_email(v, u, weight)
    
    return result


def get_mst_statistics(mst: 'DirectedEmailGraph') -> dict:
    """
    Calculate statistics about the MST.
    
    Args:
        mst: DirectedEmailGraph containing MST
    
    Returns:
        Dictionary with MST statistics
    """
    total_weight = sum(
        data.get('weight', 1) 
        for _, _, data in mst.to_networkx().edges(data=True)
    )
    
    return {
        'num_nodes': mst.get_number_of_nodes(),
        'num_edges': mst.get_number_of_edges(),
        'total_weight': total_weight,
        'average_edge_weight': total_weight / mst.get_number_of_edges() if mst.get_number_of_edges() > 0 else 0,
    }


def is_node_on_mst_backbone(graph: DirectedEmailGraph, mst: 'DirectedEmailGraph', node: str) -> bool:
    """
    Check if a node appears in MST backbone.
    
    Args:
        graph: Original DirectedEmailGraph
        mst: MST DirectedEmailGraph
        node: Node to check
    
    Returns:
        True if node is in MST
    """
    return node in mst.get_nodes()


def detect_mst_star_topology(mst: 'DirectedEmailGraph', threshold: float = 0.7) -> List[str]:
    """
    Detect nodes with star topology in MST (central hubs with many connections).
    
    Star topology = one node connected to many others (typical of broadcast spam).
    
    Args:
        mst: MST DirectedEmailGraph
        threshold: Proportion of nodes a node must connect to (0-1)
    
    Returns:
        List of nodes with star topology
    """
    out_degrees = mst.get_out_degree()
    total_nodes = mst.get_number_of_nodes()
    
    star_nodes = []
    for node, degree in out_degrees.items():
        if total_nodes > 0 and degree / total_nodes > threshold:
            star_nodes.append(node)
    
    return star_nodes


def get_mst_edges(mst: 'DirectedEmailGraph') -> List[Tuple[str, str, int]]:
    """
    Get all edges in MST with weights.
    
    Args:
        mst: MST DirectedEmailGraph
    
    Returns:
        List of tuples (source, target, weight)
    """
    return mst.get_weighted_edges()


def mst_path_exists(mst: 'DirectedEmailGraph', source: str, target: str) -> bool:
    """
    Check if path exists between nodes in MST backbone.
    
    Args:
        mst: MST DirectedEmailGraph
        source: Source node
        target: Target node
    
    Returns:
        True if path exists in MST
    """
    nx_mst = mst.to_networkx()
    undirected = nx_mst.to_undirected()
    
    return nx.has_path(undirected, source, target)
