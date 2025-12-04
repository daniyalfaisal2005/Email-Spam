"""
Path Analyzer Module

Analyzes spam propagation paths using Dijkstra's algorithm.
"""

from typing import List, Dict, Tuple, Optional
from core.directed_graph import DirectedEmailGraph
from algorithms.shortest_paths import dijkstra_shortest_path, get_path_metadata


class PathAnalyzer:
    """Analyze spam propagation paths."""
    
    def __init__(self, graph: DirectedEmailGraph):
        """
        Initialize path analyzer.
        
        Args:
            graph: DirectedEmailGraph instance
        """
        self.graph = graph
    
    def find_spam_propagation_paths(
        self,
        spam_source: str,
        max_paths: int = 10
    ) -> List[Tuple[str, List[str], dict]]:
        """
        Find paths from spam source to recipients.
        
        Args:
            spam_source: Suspected spam source node
            max_paths: Maximum number of paths to find
        
        Returns:
            List of tuples (recipient, path, metadata)
        """
        if spam_source not in self.graph.get_nodes():
            return []
        
        paths = []
        recipients = self.graph.get_neighbors(spam_source, direction='out')
        
        for recipient in recipients[:max_paths]:
            path, distance = dijkstra_shortest_path(self.graph, spam_source, recipient)
            if path:
                metadata = get_path_metadata(self.graph, path)
                paths.append((recipient, path, metadata))
        
        return paths
    
    def analyze_path_hops(self, path: List[str]) -> dict:
        """
        Analyze number of hops and intermediaries in path.
        
        Args:
            path: List of nodes forming path
        
        Returns:
            Dictionary with hop analysis
        """
        if len(path) < 2:
            return {'hops': 0, 'intermediaries': []}
        
        intermediaries = path[1:-1]  # Nodes between source and target
        
        return {
            'total_hops': len(path) - 1,
            'intermediaries': intermediaries,
            'num_intermediaries': len(intermediaries),
        }
    
    def get_all_reachable_recipients(self, spam_source: str) -> List[str]:
        """
        Get all recipients reachable from spam source (direct and indirect).
        
        Args:
            spam_source: Suspected spam source
        
        Returns:
            List of reachable recipient nodes
        """
        if spam_source not in self.graph.get_nodes():
            return []
        
        # BFS to find all reachable nodes
        visited = set()
        queue = [spam_source]
        
        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                neighbors = self.graph.get_neighbors(current, direction='out')
                queue.extend([n for n in neighbors if n not in visited])
        
        # Remove source node
        visited.discard(spam_source)
        return list(visited)
