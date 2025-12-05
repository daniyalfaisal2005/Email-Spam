from typing import Dict, List
from utils.config import SPAM_SCORE_THRESHOLD, SUSPICIOUS_SCORE_THRESHOLD


class SpamClassifier:
    """Classify nodes based on spam scores."""
    
    def __init__(
        self,
        spam_threshold: float = SPAM_SCORE_THRESHOLD,
        suspicious_threshold: float = SUSPICIOUS_SCORE_THRESHOLD
    ):
        """
        Initialize classifier with thresholds.
        
        Args:
            spam_threshold: Score above which node is classified as spam
            suspicious_threshold: Score above which node is suspicious
        """
        self.spam_threshold = spam_threshold
        self.suspicious_threshold = suspicious_threshold
    
    def classify_node(self, score: float) -> str:
        """
        Classify a single node based on score.
        
        Args:
            score: Spam score (0-100)
        
        Returns:
            Classification: 'spam', 'suspicious', or 'legitimate'
        """
        if score >= self.spam_threshold:
            return 'spam'
        elif score >= self.suspicious_threshold:
            return 'suspicious'
        else:
            return 'legitimate'
    
    def classify_all_nodes(self, spam_scores: Dict[str, float]) -> Dict[str, str]:
        """
        Classify all nodes.
        
        Args:
            spam_scores: Dictionary mapping node → score
        
        Returns:
            Dictionary mapping node → classification
        """
        classifications = {}
        for node, score in spam_scores.items():
            classifications[node] = self.classify_node(score)
        
        return classifications
    
    def get_spam_nodes(self, spam_scores: Dict[str, float]) -> List[str]:
        """Get list of spam nodes."""
        return [node for node, score in spam_scores.items() 
                if score >= self.spam_threshold]
    
    def get_suspicious_nodes(self, spam_scores: Dict[str, float]) -> List[str]:
        """Get list of suspicious nodes."""
        return [node for node, score in spam_scores.items() 
                if self.suspicious_threshold <= score < self.spam_threshold]
    
    def get_legitimate_nodes(self, spam_scores: Dict[str, float]) -> List[str]:
        """Get list of legitimate nodes."""
        return [node for node, score in spam_scores.items() 
                if score < self.suspicious_threshold]
    
    def get_classification_summary(self, spam_scores: Dict[str, float]) -> dict:
        """
        Get summary of classifications.
        
        Args:
            spam_scores: Dictionary mapping node → score
        
        Returns:
            Dictionary with counts of each classification
        """
        spam = self.get_spam_nodes(spam_scores)
        suspicious = self.get_suspicious_nodes(spam_scores)
        legitimate = self.get_legitimate_nodes(spam_scores)
        
        total = len(spam_scores)
        
        return {
            'spam_count': len(spam),
            'spam_percentage': (len(spam) / total * 100) if total > 0 else 0,
            'suspicious_count': len(suspicious),
            'suspicious_percentage': (len(suspicious) / total * 100) if total > 0 else 0,
            'legitimate_count': len(legitimate),
            'legitimate_percentage': (len(legitimate) / total * 100) if total > 0 else 0,
            'total_nodes': total,
        }
