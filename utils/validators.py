"""
Input validation functions for email spam detection system.
"""

import re


def validate_email_format(email):
    """
    Validate email format.
    
    Args:
        email: Email string to validate
    
    Returns:
        True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_csv_format(filepath):
    """
    Validate CSV file format and structure.
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        Tuple (is_valid, error_message)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if not first_line:
                return False, "CSV file is empty"
            
            # Check for required columns
            headers = first_line.split(',')
            required_columns = {'sender', 'recipient'}
            
            # Normalize headers
            headers_lower = [h.strip().lower() for h in headers]
            
            if not required_columns.issubset(set(headers_lower)):
                return False, f"CSV must contain 'sender' and 'recipient' columns. Found: {', '.join(headers)}"
            
            # Check at least one data row exists
            second_line = f.readline().strip()
            if not second_line:
                return False, "CSV file contains only headers, no data rows"
            
            return True, ""
    
    except Exception as e:
        return False, f"Error reading CSV file: {str(e)}"


def validate_graph_structure(graph):
    """
    Validate graph structure.
    
    Args:
        graph: NetworkX graph object
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if graph is None:
        return False, "Graph is None"
    
    if len(graph.nodes()) == 0:
        return False, "Graph has no nodes"
    
    return True, ""


def validate_numeric_range(value, min_val, max_val, param_name="value"):
    """
    Validate numeric value is within range.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        param_name: Name of parameter for error message
    
    Returns:
        Tuple (is_valid, error_message)
    """
    try:
        num_value = float(value)
        if num_value < min_val or num_value > max_val:
            return False, f"{param_name} must be between {min_val} and {max_val}"
        return True, ""
    except ValueError:
        return False, f"{param_name} must be a number"
