"""
Unit tests for Deposit serializer.
"""
import pytest
from decimal import Decimal
from core.models import Deposit
from core.serializers import (
    DepositSerializer,
    DepositCreateSerializer,
    DepositCompleteSerializer
)
from tests.factories.deposit_factory import DepositFactory
from tests.factories.user_factory import UserFactory


class TestDepositSerializer:
    """Test cases for DepositSerializer."""
    
    def test_serialize_deposit(self):
        """Test serializing deposit."""
        user = UserFactory(email='test@example.com')
        deposit = DepositFactory(
            user=user,
            amount=Decimal('10000.00'),
            status='COMPLETED',
            reference='DEPOSIT-12345'
        )
        
        serializer = DepositSerializer(deposit)
        data = serializer.data
        
        assert data['user'] == user.id
        assert data['user_email'] == 'test@example.com'
        assert float(data['amount']) == 10000.00
        assert data['status'] == 'COMPLETED'
        assert data['reference'] == 'DEPOSIT-12345'
    
    def test_deposit_serializer_read_only_fields(self):
        """Test read-only fields in DepositSerializer."""
        user = UserFactory()
        deposit = DepositFactory(user=user)
        
        read_only_fields = DepositSerializer.Meta.read_only_fields
        assert 'id' in read_only_fields
        assert 'user_email' in read_only_fields
        assert 'status' in read_only_fields
        assert 'reference' in read_only_fields
    
    def test_deposit_serializer_user_email_field(self):
        """Test user_email source field."""
        user = UserFactory(email='custom@example.com')
        deposit = DepositFactory(user=user)
        
        serializer = DepositSerializer(deposit)
        assert serializer.data['user_email'] == 'custom@example.com'
    
    def test_serialize_multiple_deposits(self):
        """Test serializing multiple deposits."""
        user = UserFactory()
        deposits = [
            DepositFactory(user=user, amount=Decimal('10000.00')),
            DepositFactory(user=user, amount=Decimal('20000.00')),
            DepositFactory(user=user, amount=Decimal('5000.00'))
        ]
        
        serializer = DepositSerializer(deposits, many=True)
        data = serializer.data
        
        assert len(data) == 3
        assert float(data[0]['amount']) == 10000.00
        assert float(data[1]['amount']) == 20000.00
        assert float(data[2]['amount']) == 5000.00
    
    def test_deposit_serializer_includes_timestamps(self):
        """Test that serializer includes created_at and updated_at."""
        deposit = DepositFactory()
        
        serializer = DepositSerializer(deposit)
        data = serializer.data
        
        assert 'created_at' in data
        assert 'updated_at' in data


class TestDepositCreateSerializer:
    """Test cases for DepositCreateSerializer."""
    
    def test_valid_deposit_creation(self):
        """Test creating deposit with valid amount."""
        data = {
            'amount': '10000.00'
        }
        
        serializer = DepositCreateSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['amount'] == Decimal('10000.00')
    
    def test_deposit_create_serializer_fields(self):
        """Test DepositCreateSerializer only has amount field."""
        serializer = DepositCreateSerializer()
        
        fields = set(serializer.fields.keys())
        assert fields == {'amount'}
    
    def test_deposit_create_amount_validation(self):
        """Test amount validation in DepositCreateSerializer."""
        # Valid amount
        data = {'amount': '50000.00'}
        serializer = DepositCreateSerializer(data=data)
        assert serializer.is_valid()


class TestDepositCompleteSerializer:
    """Test cases for DepositCompleteSerializer."""
    
    def test_valid_deposit_completion(self):
        """Test valid deposit completion data."""
        data = {
            'deposit_id': 1,
            'reference': 'DEPOSIT-12345'
        }
        
        serializer = DepositCompleteSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['deposit_id'] == 1
        assert serializer.validated_data['reference'] == 'DEPOSIT-12345'
    
    def test_deposit_complete_serializer_fields(self):
        """Test DepositCompleteSerializer has correct fields."""
        serializer = DepositCompleteSerializer()
        
        fields = set(serializer.fields.keys())
        assert fields == {'deposit_id', 'reference'}
    
    def test_deposit_complete_missing_deposit_id(self):
        """Test missing deposit_id field."""
        data = {
            'reference': 'DEPOSIT-12345'
        }
        
        serializer = DepositCompleteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'deposit_id' in serializer.errors
    
    def test_deposit_complete_missing_reference(self):
        """Test missing reference field."""
        data = {
            'deposit_id': 1
        }
        
        serializer = DepositCompleteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'reference' in serializer.errors
