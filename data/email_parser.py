"""
Email Data Parser

Loads and parses email data from CSV files.
"""

import csv
import os
from typing import List, Tuple
from utils.validators import validate_csv_format


class EmailParser:
    """Parse email data from CSV files."""
    
    @staticmethod
    def parse_csv(filepath: str) -> List[Tuple[str, str, int]]:
        """
        Parse CSV file into list of email tuples.
        
        CSV format expected:
        - Column 1 (sender): Email address of sender
        - Column 2 (recipient): Email address of recipient
        - Column 3 (count): Number of emails sent (optional, default=1)
        
        Args:
            filepath: Path to CSV file
        
        Returns:
            List of tuples (sender, recipient, count)
        
        Raises:
            ValueError: If CSV format is invalid
            FileNotFoundError: If file not found
        """
        # Validate file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Validate CSV format
        is_valid, error_msg = validate_csv_format(filepath)
        if not is_valid:
            raise ValueError(f"Invalid CSV format: {error_msg}")
        
        emails = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (skip header)
                try:
                    # Get sender and recipient (case-insensitive column names)
                    sender = None
                    recipient = None
                    
                    # Find sender column
                    for key in row.keys():
                        if key.strip().lower() == 'sender':
                            sender = row[key].strip()
                            break
                    
                    # Find recipient column
                    for key in row.keys():
                        if key.strip().lower() == 'recipient':
                            recipient = row[key].strip()
                            break
                    
                    if not sender or not recipient:
                        continue
                    
                    # Get count (optional)
                    count = 1
                    for key in row.keys():
                        if key.strip().lower() in ['count', 'frequency', 'number']:
                            try:
                                count = int(row[key].strip())
                            except:
                                count = 1
                            break
                    
                    emails.append((sender, recipient, count))
                
                except Exception as e:
                    print(f"Warning: Error parsing row {row_num}: {str(e)}")
                    continue
        
        if not emails:
            raise ValueError("No valid email records found in CSV")
        
        return emails
    
    @staticmethod
    def get_statistics(emails: List[Tuple[str, str, int]]) -> dict:
        """
        Get statistics about parsed emails.
        
        Args:
            emails: List of email tuples
        
        Returns:
            Dictionary with statistics
        """
        unique_senders = set(sender for sender, _, _ in emails)
        unique_recipients = set(recipient for _, recipient, _ in emails)
        total_emails = sum(count for _, _, count in emails)
        
        return {
            'total_records': len(emails),
            'unique_senders': len(unique_senders),
            'unique_recipients': len(unique_recipients),
            'total_emails': total_emails,
            'average_emails_per_record': total_emails / len(emails) if emails else 0,
        }
