"""
USSD Application Models

This module can be extended to include database models for:
- User accounts
- Transaction history
- Session management
- etc.
"""

from django.db import models

# Example model structure for future implementation:
'''
class Account(models.Model):
    """
    Account model to store user account information.
    """
    account_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Account: {self.account_number}"


class Transaction(models.Model):
    """
    Transaction model to store account transactions.
    """
    TRANSACTION_TYPES = [
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


class UssdSession(models.Model):
    """
    Model to store USSD session information.
    """
    session_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    session_data = models.JSONField(default=dict)
    start_time = models.DateTimeField(auto_now_add=True)
    last_access = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Session: {self.session_id}"
'''

