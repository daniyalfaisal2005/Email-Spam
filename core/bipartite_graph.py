"""
Bipartite Email Graph Model

Represents email communication as a bipartite graph where:
- Set A: Senders
- Set B: Recipients
- Edges: Email communications between senders and recipients

This module implements bipartite graph analysis for mass-mailing
and ring detection patterns.
"""

import networkx as nx
from typing import Dict, List, Tuple, Set


class BipartiteEmailGraph:
    """
    Bipartite graph model for sender-recipient relationships.
    
    Concept: A bipartite graph divides nodes into two disjoint sets
    with edges only between sets, never within a set.
    
    In email networks: senders in one set, recipients in another.
    This reveals structure: which senders target which recipients.
    """
    
    def __init__(self):
        """Initialize empty bipartite graph."""
        self.graph = nx.Graph()
        self.senders = set()
        self.recipients = set()
    
    def add_email(self, sender: str, recipient: str, weight: int = 1) -> None:
        """
        Add an email communication to bipartite graph.
        
        Args:
            sender: Email address of sender
            recipient: Email address of recipient
            weight: Weight to add (default 1)
        """
        self.senders.add(sender)
        self.recipients.add(recipient)
        
        if self.graph.has_edge(sender, recipient):
            current_weight = self.graph[sender][recipient].get('weight', 1)
            self.graph[sender][recipient]['weight'] = current_weight + weight
        else:
            self.graph.add_edge(sender, recipient, weight=weight, bipartite=0)
    
    def add_emails_batch(self, emails: List[Tuple[str, str, int]]) -> None:
        """Add multiple emails to bipartite graph."""
        for sender, recipient, weight in emails:
            self.add_email(sender, recipient, weight)
    
    def get_senders(self) -> List[str]:
        """Get list of all senders."""
        return list(self.senders)
    
    def get_recipients(self) -> List[str]:
        """Get list of all recipients."""
        return list(self.recipients)
    
    def project_onto_senders(self) -> 'BipartiteEmailGraph':
        """
        Create projection onto sender set.
        
        Concept: Project bipartite graph by removing recipient nodes.
        Two senders are connected if they share at least one recipient.
        Edge weight = number of shared recipients.
        
        Use: Identify coordinated spam rings (senders sharing targets).
        
        Returns:
            New BipartiteEmailGraph with sender projection
        """
        # Use NetworkX bipartite projection
        projection = nx.bipartite.projected_graph(
            self.graph, 
            self.senders,
            multigraph=False
        )
        
        result = BipartiteEmailGraph()
        result.graph = projection
        result.senders = self.senders.copy()
        result.recipients = self.recipients.copy()
        
        return result
    
    def project_onto_recipients(self) -> 'BipartiteEmailGraph':
        """
        Create projection onto recipient set.
        
        Concept: Project bipartite graph by removing sender nodes.
        Two recipients are connected if targeted by same sender.
        Edge weight = number of senders targeting both.
        
        Use: Identify common targets (likely spam campaigns).
        
        Returns:
            New BipartiteEmailGraph with recipient projection
        """
        projection = nx.bipartite.projected_graph(
            self.graph,
            self.recipients,
            multigraph=False
        )
        
        result = BipartiteEmailGraph()
        result.graph = projection
        result.senders = self.senders.copy()
        result.recipients = self.recipients.copy()
        
        return result
    
    def get_sender_degree(self, sender: str) -> int:
        """
        Get degree of sender (number of unique recipients).
        
        Args:
            sender: Sender email address
        
        Returns:
            Number of recipients this sender emails
        """
        if sender in self.graph:
            return self.graph.degree(sender)
        return 0
    
    def get_recipient_degree(self, recipient: str) -> int:
        """
        Get degree of recipient (number of unique senders).
        
        Args:
            recipient: Recipient email address
        
        Returns:
            Number of senders emailing this recipient
        """
        if recipient in self.graph:
            return self.graph.degree(recipient)
        return 0
    
    def get_shared_recipients(self, sender1: str, sender2: str) -> Set[str]:
        """
        Get recipients shared by two senders.
        
        Args:
            sender1: First sender
            sender2: Second sender
        
        Returns:
            Set of recipients targeted by both senders
        """
        neighbors1 = set(self.graph.neighbors(sender1)) if sender1 in self.graph else set()
        neighbors2 = set(self.graph.neighbors(sender2)) if sender2 in self.graph else set()
        
        return neighbors1.intersection(neighbors2)
    
    def get_number_of_nodes(self) -> int:
        """Get total number of nodes."""
        return self.graph.number_of_nodes()
    
    def get_number_of_edges(self) -> int:
        """Get total number of edges."""
        return self.graph.number_of_edges()
    
    def to_networkx(self) -> nx.Graph:
        """Get underlying NetworkX Graph object."""
        return self.graph
