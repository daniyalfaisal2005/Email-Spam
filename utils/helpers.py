"""
Helper functions for email spam detection system.
"""

def format_number(num, decimals=2):
    """Format number to specified decimal places."""
    return round(num, decimals)


def normalize_score(value, min_val=0, max_val=1, target_min=0, target_max=100):
    """
    Normalize a value from one range to another.
    
    Args:
        value: Value to normalize
        min_val: Minimum value of source range
        max_val: Maximum value of source range
        target_min: Minimum value of target range
        target_max: Maximum value of target range
    
    Returns:
        Normalized value in target range
    """
    if max_val == min_val:
        return target_min
    normalized = (value - min_val) / (max_val - min_val)
    return normalized * (target_max - target_min) + target_min


def sort_dict_by_value(dictionary, reverse=True):
    """Sort dictionary by values."""
    return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=reverse))


def filter_nodes_by_threshold(node_dict, threshold):
    """Filter nodes that exceed threshold value."""
    return {node: value for node, value in node_dict.items() if value >= threshold}


def get_top_n_nodes(node_dict, n=10):
    """Get top N nodes by value."""
    sorted_dict = sort_dict_by_value(node_dict)
    return dict(list(sorted_dict.items())[:n])


def calculate_percentage(value, total):
    """Calculate percentage of value in total."""
    if total == 0:
        return 0
    return (value / total) * 100


def format_email_count(count):
    """Format email count with K, M notation."""
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count / 1_000:.1f}K"
    else:
        return str(count)
