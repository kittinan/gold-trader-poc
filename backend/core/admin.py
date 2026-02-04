from django.contrib import admin
from .models import User, GoldPrice, Transaction, Wallet


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for User model."""
    list_display = ['email', 'username', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['email', 'username']
    ordering = ['-created_at']


@admin.register(GoldPrice)
class GoldPriceAdmin(admin.ModelAdmin):
    """Admin configuration for GoldPrice model."""
    list_display = ['price_per_baht', 'price_per_gram', 'currency', 'timestamp']
    list_filter = ['currency', 'timestamp']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for Transaction model."""
    list_display = ['user', 'transaction_type', 'gold_weight', 'total_amount', 'status', 'transaction_date']
    list_filter = ['transaction_type', 'status', 'transaction_date']
    search_fields = ['user__email']
    ordering = ['-transaction_date']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Admin configuration for Wallet model."""
    list_display = ['user', 'balance', 'gold_holdings', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']
