"""
Common pytest fixtures and configurations for Gold Trader tests.
"""
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from core.models import GoldPrice, Transaction, Wallet, GoldHolding, PriceHistory, Deposit

User = get_user_model()


@pytest.fixture
def user_data():
    """Return sample user data for testing."""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'phone_number': '0812345678',
        'date_of_birth': '1990-01-01',
    }


@pytest.fixture
def user(user_data):
    """Create and return a test user."""
    user_data_copy = user_data.copy()
    password = user_data_copy.pop('password')
    user = User.objects.create_user(**user_data_copy)
    user.set_password(password)
    user.save()
    return user


@pytest.fixture
def verified_user(user_data):
    """Create and return a verified user."""
    user_data_copy = user_data.copy()
    password = user_data_copy.pop('password')
    user_data_copy['email'] = 'verified@example.com'
    user_data_copy['username'] = 'verifieduser'
    user = User.objects.create_user(**user_data_copy)
    user.set_password(password)
    user.is_verified = True
    user.balance = Decimal('100000.00')
    user.save()
    return user


@pytest.fixture
def admin_user(user_data):
    """Create and return an admin user."""
    user_data_copy = user_data.copy()
    password = user_data_copy.pop('password')
    user_data_copy['email'] = 'admin@example.com'
    user_data_copy['username'] = 'adminuser'
    user = User.objects.create_superuser(**user_data_copy)
    user.set_password(password)
    user.save()
    return user


@pytest.fixture
def gold_price():
    """Create and return a gold price record."""
    return GoldPrice.objects.create(
        price_per_gram=Decimal('2500.00'),
        price_per_baht=Decimal('38050.00'),
        currency='THB',
        source='Test Source'
    )


@pytest.fixture
def price_history():
    """Create and return a price history record."""
    return PriceHistory.objects.create(
        price_per_gram=Decimal('2500.00'),
        price_per_baht=Decimal('38050.00'),
        currency='THB',
        source='Test Source',
        notes='Historical price record'
    )


@pytest.fixture
def multiple_price_history():
    """Create multiple price history records."""
    prices = []
    base_price = Decimal('2500.00')
    base_baht = Decimal('38050.00')

    for i in range(10):
        price = PriceHistory.objects.create(
            price_per_gram=base_price + (i * Decimal('10.00')),
            price_per_baht=base_baht + (i * Decimal('152.00')),
            currency='THB',
            source='Test Source',
            notes=f'Price record {i}'
        )
        prices.append(price)

    return prices[::-1]  # Return in chronological order


@pytest.fixture
def wallet(user):
    """Create and return a wallet for the user."""
    return Wallet.objects.create(
        user=user,
        balance=Decimal('50000.00'),
        gold_holdings=Decimal('5.000')
    )


@pytest.fixture
def gold_holding(user):
    """Create and return a gold holding for the user."""
    return GoldHolding.objects.create(
        user=user,
        amount=Decimal('10.000'),
        avg_price=Decimal('2400.00')
    )


@pytest.fixture
def transaction(user, gold_price):
    """Create and return a transaction."""
    return Transaction.objects.create(
        user=user,
        transaction_type='BUY',
        gold_weight=Decimal('2.000'),
        gold_price_per_gram=gold_price.price_per_gram,
        total_amount=Decimal('5000.00'),
        status='COMPLETED'
    )


@pytest.fixture
def completed_buy_transaction(user, gold_price):
    """Create a completed BUY transaction."""
    return Transaction.objects.create(
        user=user,
        transaction_type='BUY',
        gold_weight=Decimal('5.000'),
        gold_price_per_gram=gold_price.price_per_gram,
        total_amount=Decimal('12500.00'),
        status='COMPLETED'
    )


@pytest.fixture
def completed_sell_transaction(user, gold_price):
    """Create a completed SELL transaction."""
    return Transaction.objects.create(
        user=user,
        transaction_type='SELL',
        gold_weight=Decimal('3.000'),
        gold_price_per_gram=gold_price.price_per_gram,
        total_amount=Decimal('7500.00'),
        status='COMPLETED'
    )


@pytest.fixture
def pending_transaction(user, gold_price):
    """Create a pending transaction."""
    return Transaction.objects.create(
        user=user,
        transaction_type='BUY',
        gold_weight=Decimal('1.000'),
        gold_price_per_gram=gold_price.price_per_gram,
        total_amount=Decimal('2500.00'),
        status='PENDING'
    )


@pytest.fixture
def deposit(user):
    """Create and return a deposit."""
    return Deposit.objects.create(
        user=user,
        amount=Decimal('10000.00'),
        status='PENDING',
        reference='TEST-REF-12345'
    )


@pytest.fixture
def completed_deposit(user):
    """Create and return a completed deposit."""
    deposit = Deposit.objects.create(
        user=user,
        amount=Decimal('50000.00'),
        status='COMPLETED',
        reference='TEST-REF-67890'
    )
    user.balance = Decimal('50000.00')
    user.save()
    return deposit


@pytest.fixture
def multiple_transactions(user, gold_price):
    """Create multiple transactions for the user."""
    transactions = []

    # Buy transactions
    for i in range(3):
        trans = Transaction.objects.create(
            user=user,
            transaction_type='BUY',
            gold_weight=Decimal('2.000'),
            gold_price_per_gram=gold_price.price_per_gram,
            total_amount=Decimal('5000.00'),
            status='COMPLETED'
        )
        transactions.append(trans)

    # Sell transactions
    for i in range(2):
        trans = Transaction.objects.create(
            user=user,
            transaction_type='SELL',
            gold_weight=Decimal('1.000'),
            gold_price_per_gram=gold_price.price_per_gram,
            total_amount=Decimal('2500.00'),
            status='COMPLETED'
        )
        transactions.append(trans)

    return transactions


@pytest.fixture
def api_client():
    """Return API client for testing."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Return authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    """Return authenticated admin API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def authenticated_verified_client(api_client, verified_user):
    """Return authenticated verified user API client."""
    api_client.force_authenticate(user=verified_user)
    return api_client
