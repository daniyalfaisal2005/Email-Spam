"""
Degree Statistics Module

Calculates in-degree and out-degree metrics for email networks.

Concept: 
- In-degree: Number of unique senders emailing a person
- Out-degree: Number of unique recipients a person emails

For spam detection:
- High out-degree + low in-degree = likely spammer (broadcasts emails)
- Balanced in/out degree = likely legitimate user
"""

from typing import Dict
from core.directed_graph import DirectedEmailGraph


def get_in_degree(graph: DirectedEmailGraph) -> Dict[str, int]:
    """
    Get in-degree for all nodes.
    
    In-degree = number of different senders emailing this node.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Dictionary mapping node → in-degree count
    """
    return graph.get_in_degree()


def get_out_degree(graph: DirectedEmailGraph) -> Dict[str, int]:
    """
    Get out-degree for all nodes.
    
    Out-degree = number of different recipients this node emails.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Dictionary mapping node → out-degree count
    """
    return graph.get_out_degree()


def get_degree_ratio(graph: DirectedEmailGraph) -> Dict[str, float]:
    """
    Calculate out-degree to in-degree ratio for all nodes.
    
    Ratio > 1: More recipients than senders (broadcaster)
    Ratio ≈ 1: Balanced communication (legitimate)
    Ratio < 1: More senders than recipients (receiver)
    
    High ratio is spam indicator: high out-degree but few incoming emails.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Dictionary mapping node → degree ratio
    """
    in_degrees = get_in_degree(graph)
    out_degrees = get_out_degree(graph)
    
    ratios = {}
    for node in graph.get_nodes():
        in_deg = in_degrees.get(node, 0)
        out_deg = out_degrees.get(node, 0)
        
        # Avoid division by zero
        if in_deg == 0:
            # High out-degree with no incoming is very suspicious
            ratios[node] = float('inf') if out_deg > 0 else 0
        else:
            ratios[node] = out_deg / in_deg
    
    return ratios


def get_weighted_in_degree(graph: DirectedEmailGraph) -> Dict[str, int]:
    """
    Get weighted in-degree (sum of incoming email counts).
    
    Represents total volume of emails received from all senders.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Dictionary mapping node → weighted in-degree
    """
    return graph.get_weighted_in_degree()


def get_weighted_out_degree(graph: DirectedEmailGraph) -> Dict[str, int]:
    """
    Get weighted out-degree (sum of outgoing email counts).
    
    Represents total volume of emails sent to all recipients.
    High weighted out-degree = likely spammer.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Dictionary mapping node → weighted out-degree
    """
    return graph.get_weighted_out_degree()


def get_degree_sequence(graph: DirectedEmailGraph) -> list:
    """
    Get degree sequence (sorted list of all out-degrees).
    
    Concept: In graph theory, degree sequence is ordered list of node degrees.
    Used to characterize graph structure and compare networks.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Sorted list of out-degrees (descending)
    """
    out_degrees = get_out_degree(graph)
    degree_sequence = sorted(out_degrees.values(), reverse=True)
    return degree_sequence


def get_max_in_degree_node(graph: DirectedEmailGraph) -> tuple:
    """
    Get node with maximum in-degree and its value.
    
    This is the most-emailed-to recipient.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Tuple (node, in_degree)
    """
    in_degrees = get_in_degree(graph)
    if not in_degrees:
        return None, 0
    max_node = max(in_degrees.items(), key=lambda x: x[1])
    return max_node


def get_max_out_degree_node(graph: DirectedEmailGraph) -> tuple:
    """
    Get node with maximum out-degree and its value.
    
    This is the largest sender/broadcaster.
    Likely spam source if out-degree is very high.
    
    Args:
        graph: DirectedEmailGraph instance
    
    Returns:
        Tuple (node, out_degree)
    """
    out_degrees = get_out_degree(graph)
    if not out_degrees:
        return None, 0
    max_node = max(out_degrees.items(), key=lambda x: x[1])
    return max_node
