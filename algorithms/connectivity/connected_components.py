"""
Connected Components Module

Identifies connected components in the email network.

Concept:
- Weakly connected component: All nodes reachable if treating edges as undirected
- Strongly connected component: All nodes reachable in both directions

Application in spam detection:
- Identify isolated spam clusters
- Find fragmented networks (potential botnets)
- Separate unrelated email groups
"""

import networkx as nx
from typing import List, Set
from core.directed_graph import DirectedEmailGraph


def get_weakly_connected_components(graph: DirectedEmailGraph) -> List[Set[str]]:
    """
    Get weakly connected components.
    
    A weakly connected component is a maximal set of nodes where any two nodes
    are connected by a path, ignoring edge direction.
    
    Use: Find clusters of senders/recipients that are connected through email flow,
    regardless of direction.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        List of sets, each containing nodes in a component
    """
    nx_graph = graph.to_networkx()
    components = nx.weakly_connected_components(nx_graph)
    return list(components)


def get_strongly_connected_components(graph: DirectedEmailGraph) -> List[Set[str]]:
    """
    Get strongly connected components.
    
    A strongly connected component is a maximal set of nodes where every node
    is reachable from every other node following directed edges.
    
    Use: Find mutually communicating nodes (likely coordinated groups,
    potential spam rings with mutual communication).
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        List of sets, each containing nodes in a component
    """
    nx_graph = graph.to_networkx()
    components = nx.strongly_connected_components(nx_graph)
    return list(components)


def get_component_sizes(graph: DirectedEmailGraph) -> dict:
    """
    Get size distribution of weakly connected components.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Dictionary mapping component_id → size
    """
    components = get_weakly_connected_components(graph)
    sizes = {i: len(comp) for i, comp in enumerate(components)}
    return sizes


def get_largest_component(graph: DirectedEmailGraph) -> Set[str]:
    """
    Get the largest weakly connected component.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Set of nodes in largest component
    """
    components = get_weakly_connected_components(graph)
    if not components:
        return set()
    return max(components, key=len)


def number_of_weakly_connected_components(graph: DirectedEmailGraph) -> int:
    """
    Get count of weakly connected components.
    
    High number suggests fragmented network or multiple independent spam operations.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Number of weakly connected components
    """
    nx_graph = graph.to_networkx()
    return nx.number_weakly_connected_components(nx_graph)


def number_of_strongly_connected_components(graph: DirectedEmailGraph) -> int:
    """
    Get count of strongly connected components.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Number of strongly connected components
    """
    nx_graph = graph.to_networkx()
    return nx.number_strongly_connected_components(nx_graph)
