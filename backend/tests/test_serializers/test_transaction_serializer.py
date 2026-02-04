"""
Unit tests for Transaction serializer.
"""
import pytest
from decimal import Decimal
from core.models import Transaction
from core.serializers import TransactionSerializer
from tests.factories.transaction_factory import TransactionFactory
from tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestTransactionSerializer:
    """Test cases for TransactionSerializer."""

    def test_serialize_transaction(self):
        """Test serializing transaction."""
        user = UserFactory(email='test@example.com')
        transaction = TransactionFactory(
            user=user,
            transaction_type='BUY',
            gold_weight=Decimal('5.000'),
            gold_price_per_gram=Decimal('2500.00'),
            total_amount=Decimal('12500.00'),
            status='COMPLETED'
        )
        
        serializer = TransactionSerializer(transaction)
        data = serializer.data
        
        assert data['user'] == user.id
        assert data['user_email'] == 'test@example.com'
        assert data['transaction_type'] == 'BUY'
        assert float(data['gold_weight']) == 5.000
        assert float(data['gold_price_per_gram']) == 2500.00
        assert float(data['total_amount']) == 12500.00
        assert data['status'] == 'COMPLETED'
    
    def test_transaction_serializer_read_only_fields(self):
        """Test read-only fields in TransactionSerializer."""
        user = UserFactory()
        transaction = TransactionFactory(user=user)
        
        read_only_fields = TransactionSerializer.Meta.read_only_fields
        assert 'id' in read_only_fields
        assert 'user_email' in read_only_fields
        assert 'total_amount' in read_only_fields
        assert 'transaction_date' in read_only_fields
    
    def test_transaction_serializer_user_email_field(self):
        """Test user_email source field."""
        user = UserFactory(email='custom@example.com')
        transaction = TransactionFactory(user=user)
        
        serializer = TransactionSerializer(transaction)
        assert serializer.data['user_email'] == 'custom@example.com'
    
    def test_serialize_multiple_transactions(self):
        """Test serializing multiple transactions."""
        user = UserFactory()
        transactions = [
            TransactionFactory(user=user, transaction_type='BUY'),
            TransactionFactory(user=user, transaction_type='SELL'),
            TransactionFactory(user=user, transaction_type='BUY')
        ]
        
        serializer = TransactionSerializer(transactions, many=True)
        data = serializer.data
        
        assert len(data) == 3
        assert data[0]['transaction_type'] == 'BUY'
        assert data[1]['transaction_type'] == 'SELL'
        assert data[2]['transaction_type'] == 'BUY'
    
    def test_transaction_serializer_includes_timestamps(self):
        """Test that serializer includes created_at and updated_at."""
        transaction = TransactionFactory()
        
        serializer = TransactionSerializer(transaction)
        data = serializer.data
        
        assert 'created_at' in data
        assert 'updated_at' in data
        assert data['created_at'] is not None
        assert data['updated_at'] is not None
