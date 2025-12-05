"""
Spam Scorer Module

Calculates spam scores based on degree ratio analysis.

Metrics used:
1. Degree Ratio: out-degree / (in-degree + 1)
   - High ratio = broadcaster = suspicious
   - This is the primary spam detection metric
"""

from typing import Dict
from core.directed_graph import DirectedEmailGraph
from algorithms.metrics.degree_stats import get_degree_ratio, get_out_degree, get_in_degree
from utils.config import (
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
        out_deg = self.out_degrees.get(node, 0)
        in_deg = self.in_degrees.get(node, 0)
        
        # Check if meets minimum out-degree threshold
        if out_deg < MIN_SPAM_OUT_DEGREE:
            return 0
        
        # Score based on out-degree to differentiate spam levels
        # Pure broadcaster (in_deg=0): Maps recipients to score
        #   3-5 recipients = ~40-55 (suspicious)
        #   6-9 recipients = ~60-75 (very suspicious)
        #   10+ recipients = ~80-100 (spam)
        
        if in_deg == 0:
            # Never receives emails (pure broadcaster)
            # Formula: score = 35 + (out_degree * 5)
            # 3 -> 50, 5 -> 60, 7 -> 70, 10 -> 85, 15 -> 110 (capped at 100)
            score = min(100, 35 + (out_deg * 5))
        else:
            # Has some incoming emails - use ratio
            ratio = out_deg / (in_deg + 1)
            import math
            log_ratio = math.log(ratio + 1)
            score = normalize_score(log_ratio, 0, 3, 0, 100)
        
        return max(0, min(100, score))
    
    def calculate_combined_score(self, node: str) -> float:
        """
        Calculate combined spam score based on degree ratio only.
        
        Uses only the degree ratio metric as the primary detector.
        
        Args:
            node: Node to score
        
        Returns:
            Combined spam score (0-100)
        """
        degree_score = self.calculate_degree_score(node)
        return degree_score
    
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
            'combined_score': self.calculate_combined_score(node),
        }
