from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Extended User model for Gold Trader.
    """
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # User's cash balance in THB
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class GoldPrice(models.Model):
    """
    Model to store historical gold prices.
    """
    price_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_baht = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='THB')
    timestamp = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'gold_prices'
        verbose_name = 'Gold Price'
        verbose_name_plural = 'Gold Prices'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.price_per_baht} THB/baht at {self.timestamp}"


class Transaction(models.Model):
    """
    Model for gold buy/sell transactions.
    """
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    gold_weight = models.DecimalField(max_digits=10, decimal_places=3)  # in grams
    gold_price_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transaction_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-transaction_date']

    def __str__(self):
        return f"{self.transaction_type} {self.gold_weight}g - {self.user.email}"


class Wallet(models.Model):
    """
    Model for user wallet/cash balance.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    gold_holdings = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)  # in grams
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wallets'
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return f"{self.user.email} - {self.balance} THB, {self.gold_holdings}g gold"
