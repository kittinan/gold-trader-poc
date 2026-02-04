"""
Unit tests for User model.
"""
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from core.models import GoldPrice, Transaction, Wallet, GoldHolding, PriceHistory, Deposit
from tests.factories.user_factory import UserFactory, VerifiedUserFactory, AdminUserFactory

User = get_user_model()


class TestUserModel:
    """Test cases for User model."""
    
    def test_create_user(self, user_data):
        """Test creating a regular user."""
        password = user_data.pop('password')
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        
        assert user.email == user_data['email']
        assert user.username == user_data['username']
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_verified
        assert user.balance == Decimal('0.00')
    
    def test_create_verified_user(self):
        """Test creating a verified user."""
        user = VerifiedUserFactory()
        
        assert user.is_verified
        assert user.balance == Decimal('100000.00')
    
    def test_create_admin_user(self):
        """Test creating an admin user."""
        user = AdminUserFactory()
        
        assert user.is_staff
        assert user.is_superuser
        assert user.is_verified
    
    def test_user_str_representation(self):
        """Test string representation of user."""
        user = UserFactory(email='test@example.com')
        
        assert str(user) == 'test@example.com'
    
    def test_user_phone_number_field(self):
        """Test phone number field."""
        user = UserFactory(phone_number='0812345678')
        
        assert user.phone_number == '0812345678'
    
    def test_user_date_of_birth_field(self):
        """Test date of birth field."""
        from datetime import date
        user = UserFactory(date_of_birth=date(1990, 1, 1))
        
        assert user.date_of_birth == date(1990, 1, 1)
    
    def test_user_balance_field(self):
        """Test balance field."""
        user = UserFactory(balance=Decimal('50000.00'))
        
        assert user.balance == Decimal('50000.00')
    
    def test_user_timestamps(self):
        """Test created_at and updated_at fields."""
        user = UserFactory()
        
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_unique_email_constraint(self):
        """Test email uniqueness constraint."""
        UserFactory(email='duplicate@example.com')
        
        with pytest.raises(Exception):  # IntegrityError
            UserFactory(email='duplicate@example.com')
    
    def test_user_username_field(self):
        """Test USERNAME_FIELD configuration."""
        assert User.USERNAME_FIELD == 'email'
    
    def test_user_required_fields(self):
        """Test REQUIRED_FIELDS configuration."""
        assert User.REQUIRED_FIELDS == ['username']
