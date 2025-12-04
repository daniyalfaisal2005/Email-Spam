"""
Spam Scorer Module

Calculates spam scores combining multiple detection metrics.

Metrics used:
1. Degree Ratio: out-degree / (in-degree + 1)
   - High ratio = broadcaster = suspicious
   
2. Betweenness Centrality: How often on shortest paths
   - High value = relay node = suspicious
   
3. Temporal Burst: Sudden spike in sending
   - Sharp increase = suspicious
"""

from typing import Dict
from core.directed_graph import DirectedEmailGraph
from algorithms.metrics.degree_stats import get_degree_ratio, get_out_degree, get_in_degree
from algorithms.centrality.betweenness import calculate_betweenness_centrality
from utils.config import (
    OUT_DEGREE_WEIGHT, CENTRALITY_WEIGHT, BURST_WEIGHT,
    MIN_SPAM_OUT_DEGREE, SPAM_SCORE_THRESHOLD
)
from utils.helpers import normalize_score


class SpamScorer:
    """Calculate spam scores for nodes."""
    
    def __init__(self, graph: DirectedEmailGraph):
        """
        Initialize spam scorer.
        
        Args:
            graph: DirectedEmailGraph instance
        """
        self.graph = graph
        self.degree_ratios = get_degree_ratio(graph)
        self.betweenness = calculate_betweenness_centrality(graph, normalized=True)
        self.out_degrees = get_out_degree(graph)
        self.in_degrees = get_in_degree(graph)
    
    def calculate_degree_score(self, node: str) -> float:
        """
        Calculate score based on degree ratio (out/in).
        
        Score 0-100 where:
        - 0-20: Balanced (normal)
        - 20-50: Slightly biased (watch)
        - 50-80: High out-degree (suspicious)
        - 80-100: Very high out-degree (likely spam)
        
        Args:
            node: Node to score
        
        Returns:
            Degree score (0-100)
        """
        ratio = self.degree_ratios.get(node, 0)
        out_deg = self.out_degrees.get(node, 0)
        
        # Check if meets minimum out-degree threshold
        if out_deg < MIN_SPAM_OUT_DEGREE:
            return 0
        
        # Normalize ratio (infinity becomes 100, 0 becomes 0)
        if ratio == float('inf'):
            score = 100
        elif ratio == 0:
            score = 0
        else:
            # Map ratio to 0-100: typical ratios are 0.1 to 10+
            # log scale: log(ratio+1) maps 0->0, 1->0.69, 10->2.4
            import math
            log_ratio = math.log(ratio + 1)
            score = normalize_score(log_ratio, 0, 3, 0, 100)
        
        return max(0, min(100, score))
    
    def calculate_centrality_score(self, node: str) -> float:
        """
        Calculate score based on betweenness centrality.
        
        High centrality = relay node = suspicious.
        
        Args:
            node: Node to score
        
        Returns:
            Centrality score (0-100)
        """
        centrality = self.betweenness.get(node, 0)
        # Direct mapping: centrality is already 0-1 (normalized)
        score = centrality * 100
        return score
    
    def calculate_burst_score(self, node: str) -> float:
        """
        Calculate score based on sudden sending spike.
        
        In real implementation, would analyze temporal patterns.
        For now, return 0 (placeholder for future enhancement).
        
        Args:
            node: Node to score
        
        Returns:
            Burst score (0-100)
        """
        # Placeholder: would require temporal data
        return 0
    
    def calculate_combined_score(self, node: str) -> float:
        """
        Calculate combined spam score.
        
        Combines degree, centrality, and burst scores using weights.
        
        Formula:
        score = (degree_score * DEGREE_WEIGHT +
                 centrality_score * CENTRALITY_WEIGHT +
                 burst_score * BURST_WEIGHT)
        
        Args:
            node: Node to score
        
        Returns:
            Combined spam score (0-100)
        """
        degree_score = self.calculate_degree_score(node)
        centrality_score = self.calculate_centrality_score(node)
        burst_score = self.calculate_burst_score(node)
        
        # Normalize weights to sum to 1
        weight_sum = OUT_DEGREE_WEIGHT + CENTRALITY_WEIGHT + BURST_WEIGHT
        norm_degree_weight = OUT_DEGREE_WEIGHT / weight_sum
        norm_centrality_weight = CENTRALITY_WEIGHT / weight_sum
        norm_burst_weight = BURST_WEIGHT / weight_sum
        
        combined = (
            degree_score * norm_degree_weight +
            centrality_score * norm_centrality_weight +
            burst_score * norm_burst_weight
        )
        
        return combined
    
    def calculate_all_scores(self) -> Dict[str, float]:
        """
        Calculate spam scores for all nodes.
        
        Args:
            None
        
        Returns:
            Dictionary mapping node → spam_score
        """
        scores = {}
        for node in self.graph.get_nodes():
            scores[node] = self.calculate_combined_score(node)
        
        return scores
    
    def get_score_components(self, node: str) -> dict:
        """
        Get individual score components for debugging.
        
        Args:
            node: Node to analyze
        
        Returns:
            Dictionary with component scores
        """
        return {
            'degree_score': self.calculate_degree_score(node),
            'centrality_score': self.calculate_centrality_score(node),
            'burst_score': self.calculate_burst_score(node),
            'combined_score': self.calculate_combined_score(node),
        }
