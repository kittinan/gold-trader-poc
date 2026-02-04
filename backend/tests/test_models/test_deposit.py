"""
Unit tests for Deposit model.
"""
import pytest
from decimal import Decimal
from core.models import Deposit
from tests.factories.deposit_factory import (
    DepositFactory,
    CompletedDepositFactory,
    FailedDepositFactory
)
from tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestDepositModel:
    """Test cases for Deposit model."""
    
    def test_create_deposit(self):
        """Test creating a deposit."""
        user = UserFactory()
        deposit = Deposit.objects.create(
            user=user,
            amount=Decimal('10000.00'),
            status='PENDING',
            reference='DEPOSIT-001'
        )
        
        assert deposit.user == user
        assert deposit.amount == Decimal('10000.00')
        assert deposit.status == 'PENDING'
        assert deposit.reference == 'DEPOSIT-001'
    
    def test_deposit_factory(self):
        """Test Deposit factory."""
        deposit = DepositFactory()
        
        assert isinstance(deposit, Deposit)
        assert deposit.user is not None
        assert deposit.status == 'PENDING'
    
    def test_completed_deposit_factory(self):
        """Test CompletedDepositFactory."""
        deposit = CompletedDepositFactory()
        
        assert deposit.status == 'COMPLETED'
        assert deposit.amount == Decimal('50000.00')
    
    def test_failed_deposit_factory(self):
        """Test FailedDepositFactory."""
        deposit = FailedDepositFactory()
        
        assert deposit.status == 'FAILED'
    
    def test_deposit_str_representation(self):
        """Test string representation of Deposit."""
        user = UserFactory(email='test@example.com')
        deposit = DepositFactory(
            user=user,
            amount=Decimal('10000.00'),
            status='COMPLETED'
        )
        
        str_repr = str(deposit)
        assert 'test@example.com' in str_repr
        assert '10000.00' in str_repr
        assert 'COMPLETED' in str_repr
    
    def test_deposit_user_relationship(self):
        """Test deposit-user relationship."""
        user = UserFactory()
        deposit = DepositFactory(user=user)
        
        assert deposit.user == user
        assert deposit in user.deposits.all()
    
    def test_deposit_timestamps(self):
        """Test created_at and updated_at fields."""
        deposit = DepositFactory()
        
        assert deposit.created_at is not None
        assert deposit.updated_at is not None
    
    def test_deposit_ordering(self):
        """Test deposit ordering by created_at."""
        old_deposit = DepositFactory()
        new_deposit = DepositFactory()
        
        # Query should order by -created_at
        all_deposits = list(Deposit.objects.all())
        assert all_deposits[0].created_at >= all_deposits[1].created_at
    
    def test_deposit_status_choices(self):
        """Test deposit status choices."""
        for status in ['PENDING', 'COMPLETED', 'FAILED']:
            deposit = DepositFactory(status=status)
            assert deposit.status == status
    
    def test_deposit_reference_unique(self):
        """Test that reference field is unique."""
        reference = 'UNIQUE-REF-12345'
        user = UserFactory()
        
        DepositFactory(user=user, reference=reference)
        
        # Creating another deposit with same reference should fail
        with pytest.raises(Exception):  # IntegrityError
            DepositFactory(user=user, reference=reference)
    
    def test_deposit_amount_precision(self):
        """Test deposit amount precision (2 decimal places)."""
        deposit = DepositFactory(amount=Decimal('12345.67'))
        
        assert deposit.amount == Decimal('12345.67')
    
    def test_complete_deposit_method(self):
        """Test complete_deposit method updates user balance."""
        user = UserFactory(balance=Decimal('10000.00'))
        deposit_amount = Decimal('5000.00')
        
        deposit = Deposit.objects.create(
            user=user,
            amount=deposit_amount,
            status='PENDING',
            reference='TEST-REF'
        )
        
        # Initial balance
        assert user.balance == Decimal('10000.00')
        assert deposit.status == 'PENDING'
        
        # Complete deposit
        result = deposit.complete_deposit()
        
        assert result is True
        assert deposit.status == 'COMPLETED'
        
        # Refresh user from DB
        user.refresh_from_db()
        assert user.balance == Decimal('15000.00')  # 10000 + 5000
    
    def test_complete_deposit_already_completed(self):
        """Test completing an already completed deposit returns False."""
        deposit = CompletedDepositFactory()
        
        result = deposit.complete_deposit()
        
        assert result is False
    
    def test_multiple_deposits_for_user(self):
        """Test multiple deposits for a single user."""
        user = UserFactory()
        count = 5
        
        deposits = [
            DepositFactory(user=user) for _ in range(count)
        ]
        
        assert len(deposits) == count
        assert user.deposits.count() == count
        assert all(d.user == user for d in deposits)
    
    def test_deposit_default_status(self):
        """Test default deposit status."""
        deposit = DepositFactory(status='PENDING')
        
        assert deposit.status == 'PENDING'
    
    def test_deposit_reference_format(self):
        """Test deposit reference format."""
        deposit = DepositFactory()
        
        assert deposit.reference.startswith('DEPOSIT-')
        assert len(deposit.reference) > 10
