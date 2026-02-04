"""
Unit tests for Deposit views.
"""
import pytest
from decimal import Decimal
from rest_framework import status
from core.models import Deposit
from tests.factories.deposit_factory import DepositFactory, CompletedDepositFactory
from tests.factories.user_factory import UserFactory, VerifiedUserFactory


class TestDepositListView:
    """Test cases for deposit list view."""
    
    def test_get_deposits_unauthorized(self, api_client):
        """Test getting deposits without authentication."""
        url = '/api/deposits/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_deposits_authorized(self, authenticated_client, user):
        """Test getting deposits with authentication."""
        # Create some deposits
        for _ in range(3):
            DepositFactory(user=user)
        
        url = '/api/deposits/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
    
    def test_get_other_users_deposits(self, authenticated_client, user):
        """Test that user can't see other users' deposits."""
        # Create another user with deposits
        other_user = UserFactory(email='other@example.com')
        DepositFactory(user=other_user)
        
        url = '/api/deposits/'
        response = authenticated_client.get(url)
        
        # Should only see authenticated user's deposits
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
    
    def test_create_deposit_authenticated(self, authenticated_client, user):
        """Test creating deposit with authentication."""
        url = '/api/deposits/'
        data = {'amount': '10000.00'}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert float(response.data['amount']) == 10000.00
        assert response.data['status'] == 'COMPLETED'  # Mock deposits auto-complete
        
        # Verify user balance was updated
        user.refresh_from_db()
        assert float(user.balance) == 10000.00


class TestDepositDetailView:
    """Test cases for deposit detail view."""
    
    def test_get_deposit_unauthorized(self, api_client):
        """Test getting deposit detail without authentication."""
        deposit = DepositFactory()
        url = f'/api/deposits/{deposit.id}/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_deposit_authorized_owner(self, authenticated_client, user):
        """Test getting own deposit detail."""
        deposit = DepositFactory(user=user)
        url = f'/api/deposits/{deposit.id}/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == deposit.id
    
    def test_get_other_users_deposit(self, authenticated_client, user):
        """Test getting other user's deposit detail."""
        other_user = UserFactory(email='other@example.com')
        deposit = DepositFactory(user=other_user)
        url = f'/api/deposits/{deposit.id}/'
        response = authenticated_client.get(url)
        
        # Should not find the deposit
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestMockDepositProcessView:
    """Test cases for mock deposit processing view."""
    
    def test_process_deposit_unauthorized(self, api_client):
        """Test processing deposit without authentication."""
        url = '/api/deposits/mock-process/'
        data = {'amount': '10000.00'}
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_process_deposit_success(self, authenticated_client, verified_user):
        """Test successful mock deposit processing."""
        initial_balance = verified_user.balance
        
        url = '/api/deposits/mock-process/'
        data = {
            'amount': '50000.00',
            'payment_method': 'BANK_TRANSFER',
            'notes': 'Test deposit'
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == 'Mock deposit processed successfully'
        assert float(response.data['deposit']['amount']) == 50000.00
        assert response.data['deposit']['status'] == 'COMPLETED'
        
        # Verify balance was updated
        verified_user.refresh_from_db()
        expected_balance = initial_balance + Decimal('50000.00')
        assert verified_user.balance == expected_balance
    
    def test_process_deposit_missing_amount(self, authenticated_client, verified_user):
        """Test processing deposit without amount."""
        url = '/api/deposits/mock-process/'
        data = {'payment_method': 'BANK_TRANSFER'}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_process_deposit_negative_amount(self, authenticated_client, verified_user):
        """Test processing deposit with negative amount."""
        url = '/api/deposits/mock-process/'
        data = {'amount': '-1000.00'}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_process_deposit_exceeds_limit(self, authenticated_client, verified_user):
        """Test processing deposit exceeding mock limit."""
        url = '/api/deposits/mock-process/'
        data = {'amount': '2000000.00'}  # Exceeds 1,000,000 limit
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_process_deposit_invalid_amount_format(self, authenticated_client, verified_user):
        """Test processing deposit with invalid amount format."""
        url = '/api/deposits/mock-process/'
        data = {'amount': 'invalid'}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data


class TestWalletBalanceView:
    """Test cases for wallet balance view."""
    
    def test_get_balance_unauthorized(self, api_client):
        """Test getting balance without authentication."""
        url = '/api/wallet/balance/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_balance_authorized(self, authenticated_client, verified_user):
        """Test getting balance with authentication."""
        url = '/api/wallet/balance/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == verified_user.email
        assert float(response.data['balance']) == float(verified_user.balance)
        assert 'updated_at' in response.data
