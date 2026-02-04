"""
Unit tests for User serializers.
"""
import pytest
from decimal import Decimal
from core.models import User
from core.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UserSerializer
)
from tests.factories.user_factory import UserFactory


class TestUserRegistrationSerializer:
    """Test cases for UserRegistrationSerializer."""
    
    def test_valid_user_registration(self):
        """Test creating user with valid data."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'phone_number': '0812345678',
            'date_of_birth': '1990-01-01'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
    
    def test_password_mismatch(self):
        """Test password mismatch validation."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass',
        }
        
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
    
    def test_missing_required_fields(self):
        """Test missing required fields validation."""
        data = {
            'username': 'testuser',
        }
        
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors
        assert 'password' in serializer.errors


class TestUserLoginSerializer:
    """Test cases for UserLoginSerializer."""
    
    def test_valid_login_data(self):
        """Test valid login data."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        serializer = UserLoginSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['email'] == 'test@example.com'
    
    def test_missing_email_field(self):
        """Test missing email field."""
        data = {
            'password': 'testpass123'
        }
        
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors


class TestUserProfileSerializer:
    """Test cases for UserProfileSerializer."""
    
    def test_serialize_user_profile(self):
        """Test serializing user profile."""
        user = UserFactory(
            email='test@example.com',
            balance=Decimal('50000.00')
        )
        
        serializer = UserProfileSerializer(user)
        data = serializer.data
        
        assert data['email'] == 'test@example.com'
        assert float(data['balance']) == 50000.00
        assert 'id' in data
        assert 'username' in data
    
    def test_read_only_fields(self):
        """Test that certain fields are read-only."""
        user = UserFactory()
        serializer = UserProfileSerializer(user)
        
        # These should be in read_only_fields
        read_only_fields = UserProfileSerializer.Meta.read_only_fields
        assert 'id' in read_only_fields
        assert 'email' in read_only_fields
        assert 'balance' in read_only_fields


class TestUserProfileUpdateSerializer:
    """Test cases for UserProfileUpdateSerializer."""
    
    def test_update_user_profile(self):
        """Test updating user profile."""
        user = UserFactory(
            first_name='John',
            last_name='Doe'
        )
        
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone_number': '0898765432',
            'date_of_birth': '1995-05-15'
        }
        
        serializer = UserProfileUpdateSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        
        updated_user = serializer.save()
        assert updated_user.first_name == 'Jane'
        assert updated_user.last_name == 'Smith'
        assert updated_user.phone_number == '0898765432'
    
    def test_partial_update(self):
        """Test partial update of user profile."""
        user = UserFactory(
            first_name='John',
            last_name='Doe',
            phone_number='0812345678'
        )
        
        data = {
            'first_name': 'Jane'
        }
        
        serializer = UserProfileUpdateSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        
        updated_user = serializer.save()
        assert updated_user.first_name == 'Jane'
        assert updated_user.last_name == 'Doe'  # Unchanged


class TestUserSerializer:
    """Test cases for UserSerializer."""
    
    def test_serialize_user(self):
        """Test serializing user data."""
        user = UserFactory(
            username='testuser',
            email='test@example.com',
            first_name='John',
            balance=Decimal('100000.00')
        )
        
        serializer = UserSerializer(user)
        data = serializer.data
        
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert data['first_name'] == 'John'
        assert float(data['balance']) == 100000.00
    
    def test_user_serializer_fields(self):
        """Test UserSerializer has correct fields."""
        user = UserFactory()
        serializer = UserSerializer(user)
        
        expected_fields = {'id', 'username', 'email', 'first_name', 'last_name', 'balance'}
        assert set(serializer.data.keys()) == expected_fields
