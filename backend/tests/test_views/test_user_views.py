"""
Unit tests for User views.
"""
import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import User
from core.serializers import UserSerializer
from tests.factories.user_factory import UserFactory, VerifiedUserFactory


@pytest.mark.django_db
class TestRegisterView:
    """Test cases for user registration view."""

    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    def test_register_user_success(self, api_client):
        """Test successful user registration."""
        url = '/api/auth/register/'
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'phone_number': '0812345678',
            'date_of_birth': '1990-01-01'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == 'Registration successful'
        assert 'user' in response.data
        assert 'tokens' in response.data
        assert 'access' in response.data['tokens']
        assert 'refresh' in response.data['tokens']
        
        # Verify user was created
        user = User.objects.get(email='test@example.com')
        assert user.username == 'testuser'
    
    def test_register_password_mismatch(self, api_client):
        """Test registration with password mismatch."""
        url = '/api/auth/register/'
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass',
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_duplicate_email(self, api_client, user):
        """Test registration with duplicate email."""
        url = '/api/auth/register/'
        data = {
            'username': 'newuser',
            'email': user.email,  # Duplicate email
            'password': 'testpass123',
            'password_confirm': 'testpass123',
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLoginView:
    """Test cases for user login view."""

    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    def test_login_success(self, api_client, user_data):
        """Test successful login."""
        # Create user first
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_data_copy = user_data.copy()
        password = user_data_copy.pop('password')
        user = User.objects.create_user(**user_data_copy)
        user.set_password(password)
        user.save()
        
        url = '/api/auth/login/'
        data = {
            'email': user.email,
            'password': password
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Login successful'
        assert 'user' in response.data
        assert 'tokens' in response.data
    
    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials."""
        url = '/api/auth/login/'
        data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpass123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data


@pytest.mark.django_db
class TestProfileView:
    """Test cases for user profile view."""

    def test_get_profile_unauthorized(self, api_client):
        """Test getting profile without authentication."""
        url = '/api/auth/profile/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_profile_authorized(self, authenticated_client, user):
        """Test getting profile with authentication."""
        url = '/api/auth/profile/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['username'] == user.username
    
    def test_update_profile(self, authenticated_client, user):
        """Test updating user profile."""
        url = '/api/auth/profile/'
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone_number': '0898765432'
        }
        
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Jane'
        assert response.data['last_name'] == 'Smith'
        
        # Verify in database
        user.refresh_from_db()
        assert user.first_name == 'Jane'
        assert user.last_name == 'Smith'


@pytest.mark.django_db
class TestLogoutView:
    """Test cases for logout view."""

    def test_logout_unauthorized(self, api_client):
        """Test logout without authentication."""
        url = '/api/auth/logout/'
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_logout_authorized(self, authenticated_client):
        """Test logout with authentication."""
        url = '/api/auth/logout/'
        
        # Get refresh token first
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(authenticated_client.handler._force_user)
        
        response = authenticated_client.post(url, {'refresh': str(refresh)}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Logout successful'


@pytest.mark.django_db
class TestUserMeView:
    """Test cases for /api/auth/me/ endpoint."""

    def test_user_me_unauthorized(self, api_client):
        """Test getting user info without authentication."""
        url = '/api/auth/me/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_user_me_authorized(self, authenticated_client, user):
        """Test getting user info with authentication."""
        url = '/api/auth/me/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['username'] == user.username
        assert float(response.data['balance']) == float(user.balance)
