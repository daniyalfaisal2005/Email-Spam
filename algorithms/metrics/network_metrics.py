"""
Network Metrics Module

Calculates global network properties like density, diameter, clustering coefficient.

Concept:
- Network Density: How connected is the network (0 to 1)
- Diameter: Maximum shortest path between any two nodes
- Clustering Coefficient: How much nodes cluster together
- Average Path Length: Average shortest path between nodes
"""

import networkx as nx
from typing import Optional
from core.directed_graph import DirectedEmailGraph


def network_density(graph: DirectedEmailGraph) -> float:
    """
    Calculate network density.
    
    Density = actual_edges / possible_edges
    Range: 0 (no edges) to 1 (fully connected)
    
    Interpretation:
    - High density: Tightly connected (unusual for real email networks)
    - Low density: Sparse (typical for email networks)
    - Spam networks often have different density patterns
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Network density (0 to 1)
    """
    nx_graph = graph.to_networkx()
    return nx.density(nx_graph)


def diameter(graph: DirectedEmailGraph) -> Optional[int]:
    """
    Calculate network diameter (maximum shortest path).
    
    Diameter = longest shortest path between any two nodes.
    
    Interpretation:
    - Large diameter: Network is spread out, fragmented
    - Small diameter: Network is tightly connected
    
    Note: Returns None if graph is not connected.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Diameter value or None if graph not connected
    """
    nx_graph = graph.to_networkx()
    
    # Convert to undirected for diameter calculation
    undirected = nx_graph.to_undirected()
    
    # Check if connected
    if not nx.is_connected(undirected):
        # For disconnected graphs, get diameter of largest component
        largest_cc = max(nx.connected_components(undirected), key=len)
        subgraph = undirected.subgraph(largest_cc)
        if len(subgraph) > 1:
            return nx.diameter(subgraph)
        return 0
    
    return nx.diameter(undirected)


def radius(graph: DirectedEmailGraph) -> Optional[int]:
    """
    Calculate network radius (minimum shortest path from a center node to all others).
    
    Radius = minimum eccentricity of any node
    
    Interpretation:
    - Small radius: There's a central node that can reach all others quickly
    - Large radius: No good central node (fragmented or spread out)
    - Radius ≤ Diameter (always)
    
    For spam detection:
    - Small radius: Suggests organized spam ring with a command center
    - Large radius: Suggests distributed, unorganized spam
    
    Note: Returns None if graph is not connected.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Network radius or None if graph not connected
    """
    nx_graph = graph.to_networkx()
    undirected = nx_graph.to_undirected()
    
    # Check if connected
    if not nx.is_connected(undirected):
        # For disconnected graphs, use largest component
        largest_cc = max(nx.connected_components(undirected), key=len)
        subgraph = undirected.subgraph(largest_cc)
        if len(subgraph) > 1:
            return nx.radius(subgraph)
        return 0
    
    return nx.radius(undirected)


def average_shortest_path_length(graph: DirectedEmailGraph) -> Optional[float]:
    """
    Calculate average shortest path length.
    
    Interpretation:
    - Small average path length: "Small-world" network (efficient communication)
    - Large average path length: Fragmented network
    
    Note: Returns None if graph is not connected.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Average shortest path length or None if not connected
    """
    nx_graph = graph.to_networkx()
    undirected = nx_graph.to_undirected()
    
    if not nx.is_connected(undirected):
        # For disconnected graphs, use largest component
        largest_cc = max(nx.connected_components(undirected), key=len)
        subgraph = undirected.subgraph(largest_cc)
        if len(subgraph) > 1:
            return nx.average_shortest_path_length(subgraph)
        return 0
    
    return nx.average_shortest_path_length(undirected)


def clustering_coefficient(graph: DirectedEmailGraph, node: Optional[str] = None) -> dict:
    """
    Calculate clustering coefficient.
    
    Clustering coefficient measures how much neighbors of a node are connected.
    Range: 0 (no clustering) to 1 (complete clustering)
    
    Interpretation:
    - High clustering: Nodes tend to form tight groups/triangles
    - Low clustering: Random connections
    
    Args:
        graph: DirectedEmailGraph instance
        node: If specified, return only clustering coeff for that node.
              If None, return for all nodes.
    
    Returns:
        Dictionary mapping node → clustering coefficient (or single value if node specified)
    """
    nx_graph = graph.to_networkx()
    
    # Convert to undirected for clustering calculation
    undirected = nx_graph.to_undirected()
    
    if node:
        return nx.clustering(undirected, node)
    else:
        return nx.clustering(undirected)


def average_clustering_coefficient(graph: DirectedEmailGraph) -> float:
    """
    Calculate average clustering coefficient across all nodes.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Average clustering coefficient
    """
    nx_graph = graph.to_networkx()
    undirected = nx_graph.to_undirected()
    return nx.average_clustering(undirected)


def average_degree(graph: DirectedEmailGraph) -> float:
    """
    Calculate average degree of nodes in the network.
    
    Average Degree = 2 * num_edges / num_nodes
    
    Interpretation:
    - Higher average degree: More interconnected (spam networks often show higher degree)
    - Lower average degree: Sparse network
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Average degree (including both in-degree and out-degree)
    """
    nx_graph = graph.to_networkx()
    num_nodes = nx_graph.number_of_nodes()
    num_edges = nx_graph.number_of_edges()
    
    if num_nodes == 0:
        return 0
    
    # Average degree = 2 * edges / nodes
    return (2 * num_edges) / num_nodes


def number_of_triangles(graph: DirectedEmailGraph) -> int:
    """
    Count number of triangles (3-node cycles) in network.
    
    Triangle = three nodes all connected to each other.
    High triangles indicate tight communities/clustering.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Total number of triangles
    """
    nx_graph = graph.to_networkx()
    undirected = nx_graph.to_undirected()
    
    triangles = sum(nx.triangles(undirected).values()) // 3
    return triangles


def get_all_metrics(graph: DirectedEmailGraph) -> dict:
    """
    Calculate all network metrics at once.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Dictionary with all metrics
    """
    return {
        'num_nodes': graph.get_number_of_nodes(),
        'num_edges': graph.get_number_of_edges(),
        'average_degree': average_degree(graph),
        'density': network_density(graph),
        'diameter': diameter(graph),
        'radius': radius(graph),
        'average_path_length': average_shortest_path_length(graph),
        'average_clustering': average_clustering_coefficient(graph),
        'triangles': number_of_triangles(graph),
    }
