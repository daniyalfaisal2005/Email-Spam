"""
MST Analyzer Module

Analyzes MST structure for spam patterns.
"""

from typing import List
from core.directed_graph import DirectedEmailGraph
from algorithms.spanning_trees.minimum_spanning_tree import (
    compute_minimum_spanning_tree,
    detect_mst_star_topology,
    get_mst_statistics
)


class MSTAnalyzer:
    """Analyze MST structure for spam indicators."""
    
    def __init__(self, graph: DirectedEmailGraph):
        """
        Initialize MST analyzer.
        
        Args:
            graph: DirectedEmailGraph instance
        """
        self.graph = graph
        self.mst = compute_minimum_spanning_tree(graph)
    
    def detect_star_topology(self, threshold: float = 0.5) -> List[str]:
        """
        Detect nodes with star topology in MST.
        
        Star topology = one node connected to many others.
        Typical of broadcast spam.
        
        Args:
            threshold: Proportion of nodes to connect (0-1)
        
        Returns:
            List of nodes with star topology
        """
        return detect_mst_star_topology(self.mst, threshold=threshold)
    
    def get_mst_metrics(self) -> dict:
        """
        Get MST statistics.
        
        Returns:
            Dictionary with MST metrics
        """
        return get_mst_statistics(self.mst)
    
    def is_on_backbone(self, node: str) -> bool:
        """
        Check if node is on MST backbone.
        
        Args:
            node: Node to check
        
        Returns:
            True if node is in MST
        """
        return node in self.mst.get_nodes()
    
    def get_mst_neighbors(self, node: str) -> List[str]:
        """
        Get neighbors of node in MST backbone.
        
        Args:
            node: Node to get neighbors for
        
        Returns:
            List of neighboring nodes in MST
        """
        if self.is_on_backbone(node):
            return self.mst.get_neighbors(node, direction='out')
        return []
