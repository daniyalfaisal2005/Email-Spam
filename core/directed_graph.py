import networkx as nx
from typing import Dict, List, Tuple, Optional


class DirectedEmailGraph:
    """
    Directed weighted graph model for email communications.
    
    Concept: A directed graph (digraph) represents one-way relationships.
    In email networks, edges go from sender → recipient, representing
    email flow direction.
    """
    
    def __init__(self):
        """Initialize empty directed graph."""
        self.graph = nx.DiGraph()
    
    def add_email(self, sender: str, recipient: str, weight: int = 1) -> None:
        """
        Add an email communication to the graph.
        
        If edge already exists, increment weight by specified amount.
        If edge doesn't exist, create it with specified weight.
        
        Args:
            sender: Email address of sender
            recipient: Email address of recipient
            weight: Weight to add (default 1 for single email)
        """
        if self.graph.has_edge(sender, recipient):
            # Increment existing edge weight
            current_weight = self.graph[sender][recipient].get('weight', 1)
            self.graph[sender][recipient]['weight'] = current_weight + weight
        else:
            # Add new edge with weight
            self.graph.add_edge(sender, recipient, weight=weight)
    
    def add_emails_batch(self, emails: List[Tuple[str, str, int]]) -> None:
        """
        Add multiple emails to graph efficiently.
        
        Args:
            emails: List of tuples (sender, recipient, weight)
        """
        for sender, recipient, weight in emails:
            self.add_email(sender, recipient, weight)
    
    def get_nodes(self) -> List[str]:
        """Get list of all nodes (email addresses)."""
        return list(self.graph.nodes())
    
    def get_edges(self) -> List[Tuple[str, str]]:
        """Get list of all edges (sender, recipient pairs)."""
        return list(self.graph.edges())
    
    def get_weighted_edges(self) -> List[Tuple[str, str, int]]:
        """Get list of edges with weights (sender, recipient, weight)."""
        return [(u, v, d['weight']) for u, v, d in self.graph.edges(data=True)]
    
    def get_edge_weight(self, sender: str, recipient: str) -> Optional[int]:
        """
        Get weight of edge between sender and recipient.
        
        Returns:
            Edge weight or None if edge doesn't exist
        """
        if self.graph.has_edge(sender, recipient):
            return self.graph[sender][recipient].get('weight', 1)
        return None
    
    def get_in_degree(self, node: Optional[str] = None) -> Dict[str, int]:
        """
        Get in-degree of nodes (number of different senders).
        
        Args:
            node: If specified, return only in-degree of that node.
                  If None, return in-degrees for all nodes.
        
        Returns:
            Dictionary mapping node → in-degree or single value
        """
        if node:
            return dict(self.graph.in_degree([node]))[node]
        return dict(self.graph.in_degree())
    
    def get_out_degree(self, node: Optional[str] = None) -> Dict[str, int]:
        """
        Get out-degree of nodes (number of different recipients).
        
        Args:
            node: If specified, return only out-degree of that node.
                  If None, return out-degrees for all nodes.
        
        Returns:
            Dictionary mapping node → out-degree or single value
        """
        if node:
            return dict(self.graph.out_degree([node]))[node]
        return dict(self.graph.out_degree())
    
    def get_weighted_in_degree(self, node: Optional[str] = None) -> Dict[str, int]:
        """
        Get weighted in-degree (sum of incoming email counts).
        
        Args:
            node: If specified, return only weighted in-degree of that node.
                  If None, return weighted in-degrees for all nodes.
        
        Returns:
            Dictionary mapping node → weighted in-degree
        """
        result = {}
        for n in self.graph.nodes():
            weighted_in = sum(
                d.get('weight', 1) 
                for _, _, d in self.graph.in_edges(n, data=True)
            )
            result[n] = weighted_in
        
        if node:
            return result.get(node, 0)
        return result
    
    def get_weighted_out_degree(self, node: Optional[str] = None) -> Dict[str, int]:
        """
        Get weighted out-degree (sum of outgoing email counts).
        
        Args:
            node: If specified, return only weighted out-degree of that node.
                  If None, return weighted out-degrees for all nodes.
        
        Returns:
            Dictionary mapping node → weighted out-degree
        """
        result = {}
        for n in self.graph.nodes():
            weighted_out = sum(
                d.get('weight', 1) 
                for _, _, d in self.graph.out_edges(n, data=True)
            )
            result[n] = weighted_out
        
        if node:
            return result.get(node, 0)
        return result
    
    def get_neighbors(self, node: str, direction: str = 'out') -> List[str]:
        """
        Get neighbors of a node.
        
        Args:
            node: Node to get neighbors for
            direction: 'out' for successors, 'in' for predecessors
        
        Returns:
            List of neighbor nodes
        """
        if direction == 'out':
            return list(self.graph.successors(node))
        else:
            return list(self.graph.predecessors(node))
    
    def get_number_of_nodes(self) -> int:
        """Get total number of nodes."""
        return self.graph.number_of_nodes()
    
    def get_number_of_edges(self) -> int:
        """Get total number of edges."""
        return self.graph.number_of_edges()
    
    def to_networkx(self) -> nx.DiGraph:
        """
        Get underlying NetworkX DiGraph object.
        
        Returns:
            NetworkX DiGraph instance
        """
        return self.graph
    
    def copy(self) -> 'DirectedEmailGraph':
        """Create a deep copy of this graph."""
        new_graph = DirectedEmailGraph()
        new_graph.graph = self.graph.copy()
        return new_graph
    
    def get_subgraph(self, nodes: List[str]) -> 'DirectedEmailGraph':
        """
        Get subgraph containing only specified nodes.
        
        Args:
            nodes: List of nodes to include in subgraph
        
        Returns:
            New DirectedEmailGraph containing subgraph
        """
        subgraph = DirectedEmailGraph()
        subgraph.graph = self.graph.subgraph(nodes).copy()
        return subgraph
