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


class GoldHolding(models.Model):
    """
    Model to track user's gold holdings with average purchase price.
    This maintains a record of gold owned by each user with their average buy price.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gold_holdings')
    amount = models.DecimalField(max_digits=10, decimal_places=3)  # Gold amount in grams
    avg_price = models.DecimalField(max_digits=10, decimal_places=2)  # Average buy price per gram in THB
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Total value (amount * avg_price)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gold_holdings'
        verbose_name = 'Gold Holding'
        verbose_name_plural = 'Gold Holdings'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.email} - {self.amount}g @ {self.avg_price} THB/g"

    def save(self, *args, **kwargs):
        # Auto-calculate total value
        self.total_value = self.amount * self.avg_price
        super().save(*args, **kwargs)


class PriceHistory(models.Model):
    """
    Model to record historical gold price changes.
    This model maintains a comprehensive history of gold price updates.
    """
    price_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_baht = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='THB')
    timestamp = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'price_history'
        verbose_name = 'Price History'
        verbose_name_plural = 'Price History'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.price_per_baht} THB/baht at {self.timestamp}"
