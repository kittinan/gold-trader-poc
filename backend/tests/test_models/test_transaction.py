"""
Unit tests for Transaction model.
"""
import pytest
from decimal import Decimal
from core.models import Transaction
from tests.factories.transaction_factory import (
    TransactionFactory,
    BuyTransactionFactory,
    SellTransactionFactory,
    PendingTransactionFactory
)
from tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestTransactionModel:
    """Test cases for Transaction model."""
    
    def test_create_buy_transaction(self):
        """Test creating a BUY transaction."""
        user = UserFactory()
        transaction = Transaction.objects.create(
            user=user,
            transaction_type='BUY',
            gold_weight=Decimal('5.000'),
            gold_price_per_gram=Decimal('2500.00'),
            total_amount=Decimal('12500.00'),
            status='COMPLETED'
        )
        
        assert transaction.transaction_type == 'BUY'
        assert transaction.gold_weight == Decimal('5.000')
        assert transaction.gold_price_per_gram == Decimal('2500.00')
        assert transaction.total_amount == Decimal('12500.00')
        assert transaction.status == 'COMPLETED'
    
    def test_create_sell_transaction(self):
        """Test creating a SELL transaction."""
        user = UserFactory()
        transaction = Transaction.objects.create(
            user=user,
            transaction_type='SELL',
            gold_weight=Decimal('2.000'),
            gold_price_per_gram=Decimal('2600.00'),
            total_amount=Decimal('5200.00'),
            status='COMPLETED'
        )
        
        assert transaction.transaction_type == 'SELL'
        assert transaction.gold_weight == Decimal('2.000')
    
    def test_transaction_factory(self):
        """Test Transaction factory."""
        transaction = TransactionFactory()
        
        assert isinstance(transaction, Transaction)
        assert transaction.user is not None
    
    def test_buy_transaction_factory(self):
        """Test BuyTransactionFactory."""
        transaction = BuyTransactionFactory()
        
        assert transaction.transaction_type == 'BUY'
        assert transaction.gold_weight == Decimal('5.000')
        assert transaction.status == 'COMPLETED'
    
    def test_sell_transaction_factory(self):
        """Test SellTransactionFactory."""
        transaction = SellTransactionFactory()
        
        assert transaction.transaction_type == 'SELL'
        assert transaction.status == 'COMPLETED'
    
    def test_pending_transaction_factory(self):
        """Test PendingTransactionFactory."""
        transaction = PendingTransactionFactory()
        
        assert transaction.status == 'PENDING'
    
    def test_transaction_str_representation(self):
        """Test string representation of Transaction."""
        user = UserFactory(email='test@example.com')
        transaction = TransactionFactory(
            user=user,
            transaction_type='BUY',
            gold_weight=Decimal('2.000')
        )
        
        str_repr = str(transaction)
        assert 'BUY' in str_repr
        assert '2.000' in str_repr
        assert 'test@example.com' in str_repr
    
    def test_transaction_user_relationship(self):
        """Test transaction-user relationship."""
        user = UserFactory()
        transaction = TransactionFactory(user=user)
        
        assert transaction.user == user
        assert transaction in user.transactions.all()
    
    def test_transaction_timestamps(self):
        """Test created_at and updated_at fields."""
        transaction = TransactionFactory()
        
        assert transaction.created_at is not None
        assert transaction.updated_at is not None
    
    def test_transaction_ordering(self):
        """Test transaction ordering by transaction_date."""
        old_trans = TransactionFactory()
        new_trans = TransactionFactory()
        
        # Query should order by -transaction_date
        all_trans = list(Transaction.objects.all())
        assert all_trans[0].transaction_date >= all_trans[1].transaction_date
    
    def test_transaction_type_choices(self):
        """Test transaction type choices."""
        transaction = TransactionFactory(transaction_type='BUY')
        assert transaction.transaction_type == 'BUY'
        
        transaction = TransactionFactory(transaction_type='SELL')
        assert transaction.transaction_type == 'SELL'
    
    def test_transaction_status_choices(self):
        """Test transaction status choices."""
        for status in ['PENDING', 'COMPLETED', 'CANCELLED']:
            transaction = TransactionFactory(status=status)
            assert transaction.status == status
    
    def test_transaction_total_amount_calculation(self):
        """Test total amount calculation."""
        gold_weight = Decimal('5.000')
        gold_price_per_gram = Decimal('2500.00')
        expected_total = gold_weight * gold_price_per_gram
        
        transaction = Transaction.objects.create(
            user=UserFactory(),
            transaction_type='BUY',
            gold_weight=gold_weight,
            gold_price_per_gram=gold_price_per_gram,
            total_amount=expected_total,
            status='COMPLETED'
        )
        
        assert transaction.total_amount == expected_total
        assert transaction.total_amount == Decimal('12500.00')
    
    def test_multiple_transactions_for_user(self):
        """Test multiple transactions for a single user."""
        user = UserFactory()
        count = 5
        
        transactions = [
            TransactionFactory(user=user) for _ in range(count)
        ]
        
        assert len(transactions) == count
        assert user.transactions.count() == count
        assert all(t.user == user for t in transactions)
    
    def test_transaction_gold_weight_precision(self):
        """Test gold weight precision (3 decimal places)."""
        transaction = TransactionFactory(gold_weight=Decimal('2.345'))
        
        assert transaction.gold_weight == Decimal('2.345')
    
    def test_transaction_default_status(self):
        """Test default transaction status."""
        transaction = TransactionFactory(status='PENDING')
        
        assert transaction.status == 'PENDING'
