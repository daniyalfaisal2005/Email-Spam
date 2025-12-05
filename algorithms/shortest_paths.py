"""
Shortest Paths Module - Dijkstra's Algorithm

Implements Dijkstra's algorithm for finding shortest paths in weighted graphs.

Concept:
Dijkstra's algorithm finds the shortest path between two nodes in a weighted graph.
- Used for: Finding minimum-cost routes
- Weight interpretation: Can be distance, cost, or in this case, inverse email frequency
- Time complexity: O((V + E) log V) with min-heap

Application in spam detection:
- Find shortest communication chain between suspected spammers and victims
- Identify if spammers use intermediaries to avoid detection
- Trace spam propagation paths
"""

import networkx as nx
from typing import List, Tuple, Optional
from core.directed_graph import DirectedEmailGraph


def dijkstra_shortest_path(
    graph: DirectedEmailGraph,
    source: str,
    target: str,
    weight_type: str = 'inverse'
) -> Tuple[Optional[List[str]], Optional[float]]:
    """
    Find shortest path between source and target using Dijkstra's algorithm.
    
    Args:
        graph: DirectedEmailGraph instance
        source: Starting node (sender)
        target: Ending node (recipient)
        weight_type: How to interpret edge weights
            - 'inverse': Lower weights are closer (high email count = low distance)
            - 'direct': Higher weights are closer (raw weight)
    
    Returns:
        Tuple (path_list, total_distance)
        - path_list: List of nodes from source to target
        - total_distance: Sum of edge weights along path
        Returns (None, None) if no path exists
    
    Example:
        path, distance = dijkstra_shortest_path(graph, 'spam@example.com', 'victim@example.com')
        # path = ['spam@example.com', 'relay@example.com', 'victim@example.com']
        # distance = 150 (total emails)
    """
    nx_graph = graph.to_networkx()
    
    # Check if nodes exist
    if source not in nx_graph or target not in nx_graph:
        return None, None
    
    # Check if target is reachable from source
    if not nx.has_path(nx_graph, source, target):
        return None, None
    
    try:
        if weight_type == 'inverse':
            # Lower email count = shorter distance
            # Transform weights: distance = 1 / weight
            # To avoid division issues, use: distance = max_weight - weight
            max_weight = 0
            for u, v, data in nx_graph.edges(data=True):
                w = data.get('weight', 1)
                if w > max_weight:
                    max_weight = w
            
            # Create new graph with inverted weights
            inverted_graph = nx_graph.copy()
            for u, v in inverted_graph.edges():
                original_weight = inverted_graph[u][v].get('weight', 1)
                # Inverse: high weight becomes low distance
                inverted_graph[u][v]['weight'] = max_weight + 1 - original_weight
            
            path = nx.dijkstra_path(inverted_graph, source, target, weight='weight')
            
            # Calculate ACTUAL distance (sum of original weights along the path)
            actual_distance = 0
            for i in range(len(path) - 1):
                edge_weight = nx_graph[path[i]][path[i+1]].get('weight', 1)
                actual_distance += edge_weight
            
            return path, actual_distance
        else:
            # Use weights directly
            path = nx.dijkstra_path(nx_graph, source, target, weight='weight')
            distance = nx.dijkstra_path_length(nx_graph, source, target, weight='weight')
            
            return path, distance
    
    except nx.NetworkXNoPath:
        return None, None
    except nx.NodeNotFound:
        return None, None


def dijkstra_shortest_path_length(
    graph: DirectedEmailGraph,
    source: str,
    target: str
) -> Optional[float]:
    """
    Get only the distance of shortest path (not the path itself).
    
    Args:
        graph: DirectedEmailGraph instance
        source: Starting node
        target: Ending node
    
    Returns:
        Total path distance or None if no path exists
    """
    _, distance = dijkstra_shortest_path(graph, source, target)
    return distance


def dijkstra_from_source(
    graph: DirectedEmailGraph,
    source: str
) -> Tuple[dict, dict]:
    """
    Find shortest paths from source to all reachable nodes.
    
    Returns shortest distances and paths from source to all nodes.
    
    Args:
        graph: DirectedEmailGraph instance
        source: Starting node
    
    Returns:
        Tuple (distances_dict, paths_dict)
        - distances_dict: {node: distance}
        - paths_dict: {node: path_list}
    """
    nx_graph = graph.to_networkx()
    
    if source not in nx_graph:
        return {}, {}
    
    lengths = nx.single_source_dijkstra_path_length(nx_graph, source, weight='weight')
    paths = nx.single_source_dijkstra_path(nx_graph, source, weight='weight')
    
    return lengths, paths


def get_path_metadata(
    graph: DirectedEmailGraph,
    path: List[str]
) -> dict:
    """
    Get detailed information about a path.
    
    Args:
        graph: DirectedEmailGraph instance
        path: List of nodes forming the path
    
    Returns:
        Dictionary with path metadata:
        - hop_count: Number of hops (edges)
        - total_weight: Sum of edge weights
        - edge_weights: Individual edge weights
        - average_weight: Average weight per edge
    """
    if not path or len(path) < 2:
        return {'hop_count': 0, 'total_weight': 0, 'edge_weights': [], 'average_weight': 0}
    
    edge_weights = []
    total_weight = 0
    
    for i in range(len(path) - 1):
        source = path[i]
        target = path[i + 1]
        weight = graph.get_edge_weight(source, target)
        if weight is not None:
            edge_weights.append(weight)
            total_weight += weight
    
    hop_count = len(path) - 1
    average_weight = total_weight / hop_count if hop_count > 0 else 0
    
    return {
        'hop_count': hop_count,
        'total_weight': total_weight,
        'edge_weights': edge_weights,
        'average_weight': average_weight,
    }
