"""
Email Data Generator

Generates synthetic email datasets for testing and demonstration.
Includes realistic email patterns and injected spam.
"""

import random
import csv
from datetime import datetime, timedelta
from typing import List, Tuple
import os


class EmailGenerator:
    """Generate synthetic email datasets with spam patterns."""
    
    def __init__(self, seed=None):
        """
        Initialize email generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        if seed:
            random.seed(seed)
    
    def generate_legitimate_emails(
        self,
        num_senders: int = 50,
        emails_per_sender: int = 20,
        recipients_per_sender: int = 5
    ) -> List[Tuple[str, str, int]]:
        """
        Generate legitimate email patterns.
        
        Characteristics:
        - Balanced senders and receivers
        - Each sender emails limited recipients
        - Reasonable email volumes
        
        Args:
            num_senders: Number of legitimate senders
            emails_per_sender: Average emails per sender
            recipients_per_sender: Average unique recipients per sender
        
        Returns:
            List of tuples (sender, recipient, count)
        """
        senders = [f"user{i}@example.com" for i in range(num_senders)]
        recipients = [f"user{i}@example.com" for i in range(num_senders)]
        
        emails = []
        for sender in senders:
            num_recipients = random.randint(1, recipients_per_sender)
            selected_recipients = random.sample(recipients, min(num_recipients, len(recipients)))
            
            for recipient in selected_recipients:
                if sender != recipient:  # No self-emails
                    count = random.randint(1, emails_per_sender * 2)
                    emails.append((sender, recipient, count))
        
        return emails
    
    def generate_spam_broadcast(
        self,
        num_spammers: int = 5,
        recipients_per_spammer: int = 100,
        emails_per_recipient: int = 10
    ) -> List[Tuple[str, str, int]]:
        """
        Generate mass-mailing spam pattern.
        
        Characteristics:
        - Few senders, many recipients
        - High out-degree, low in-degree
        - Typical of broadcast spam campaigns
        
        Args:
            num_spammers: Number of spam sources
            recipients_per_spammer: Recipients per spammer
            emails_per_recipient: Emails to each recipient
        
        Returns:
            List of tuples (sender, recipient, count)
        """
        recipients = [f"victim{i}@example.com" for i in range(recipients_per_spammer)]
        emails = []
        
        for i in range(num_spammers):
            spammer = f"spammer{i}@spam.com"
            for recipient in recipients:
                count = random.randint(emails_per_recipient - 2, emails_per_recipient + 2)
                emails.append((spammer, recipient, count))
        
        return emails
    
    def generate_spam_ring(
        self,
        ring_size: int = 10,
        shared_recipients: int = 50,
        emails_per_connection: int = 5
    ) -> List[Tuple[str, str, int]]:
        """
        Generate coordinated spam ring pattern.
        
        Characteristics:
        - Multiple spammers sharing same recipient list
        - Likely coordinated operation
        - Detectable by shared recipient patterns
        
        Args:
            ring_size: Number of spammers in ring
            shared_recipients: Shared target recipients
            emails_per_connection: Emails per connection
        
        Returns:
            List of tuples (sender, recipient, count)
        """
        spammers = [f"spam_ring{i}@xyz.com" for i in range(ring_size)]
        recipients = [f"target{i}@example.com" for i in range(shared_recipients)]
        
        emails = []
        for spammer in spammers:
            for recipient in recipients:
                count = random.randint(emails_per_connection - 1, emails_per_connection + 3)
                emails.append((spammer, recipient, count))
        
        return emails
    
    def combine_datasets(self, *email_lists) -> List[Tuple[str, str, int]]:
        """
        Combine multiple email datasets.
        
        Args:
            *email_lists: Variable number of email lists to combine
        
        Returns:
            Combined list of emails
        """
        combined = []
        for email_list in email_lists:
            combined.extend(email_list)
        return combined
    
    def export_to_csv(
        self,
        emails: List[Tuple[str, str, int]],
        filename: str,
        headers: List[str] = None
    ) -> None:
        """
        Export emails to CSV file.
        
        Args:
            emails: List of tuples (sender, recipient, count)
            filename: Output CSV filename
            headers: Column headers (default: ['sender', 'recipient', 'count'])
        """
        if headers is None:
            headers = ['sender', 'recipient', 'count']
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for email_tuple in emails:
                writer.writerow(email_tuple)
    
    @staticmethod
    def create_sample_datasets(output_dir: str = 'data/datasets'):
        """
        Create sample datasets for testing.
        
        Args:
            output_dir: Directory to save sample files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        gen = EmailGenerator(seed=42)
        
        # Dataset 1: Legitimate emails only
        legitimate = gen.generate_legitimate_emails(
            num_senders=50,
            emails_per_sender=15,
            recipients_per_sender=5
        )
        gen.export_to_csv(legitimate, f'{output_dir}/legitimate.csv')
        print(f"Created: {output_dir}/legitimate.csv")
        
        # Dataset 2: Mixed - legitimate + spam broadcast
        spam_broadcast = gen.generate_spam_broadcast(
            num_spammers=3,
            recipients_per_spammer=100,
            emails_per_recipient=8
        )
        mixed = gen.combine_datasets(legitimate, spam_broadcast)
        gen.export_to_csv(mixed, f'{output_dir}/mixed_with_broadcast.csv')
        print(f"Created: {output_dir}/mixed_with_broadcast.csv")
        
        # Dataset 3: Mixed - legitimate + spam ring
        spam_ring = gen.generate_spam_ring(
            ring_size=8,
            shared_recipients=50,
            emails_per_connection=6
        )
        mixed_ring = gen.combine_datasets(legitimate, spam_ring)
        gen.export_to_csv(mixed_ring, f'{output_dir}/mixed_with_ring.csv')
        print(f"Created: {output_dir}/mixed_with_ring.csv")
        
        # Dataset 4: All combined
        all_combined = gen.combine_datasets(legitimate, spam_broadcast, spam_ring)
        gen.export_to_csv(all_combined, f'{output_dir}/all_combined.csv')
        print(f"Created: {output_dir}/all_combined.csv")
