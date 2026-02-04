"""
Unit tests for Transaction and Trading views.
"""
import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Transaction, Wallet, GoldHolding
from tests.factories.transaction_factory import TransactionFactory
from tests.factories.user_factory import UserFactory, VerifiedUserFactory
from tests.factories.gold_price_factory import PriceHistoryFactory


@pytest.mark.django_db
class TestTransactionListView:
    """Test cases for transaction list view."""

    def test_get_transactions_unauthorized(self, api_client):
        """Test getting transactions without authentication."""
        url = '/api/gold/transactions/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_transactions_authorized(self, authenticated_client, user):
        """Test getting transactions with authentication."""
        # Create some transactions
        for _ in range(3):
            TransactionFactory(user=user)
        
        url = '/api/gold/transactions/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
    
    def test_get_other_users_transactions(self, authenticated_client, user):
        """Test that user can't see other users' transactions."""
        # Create another user with transactions
        other_user = UserFactory(email='other@example.com')
        TransactionFactory(user=other_user)
        
        url = '/api/gold/transactions/'
        response = authenticated_client.get(url)
        
        # Should only see authenticated user's transactions
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0  # No transactions for authenticated user


@pytest.mark.django_db
class TestTradeAPIView:
    """Test cases for trade API view."""

    def test_trade_unauthorized(self, api_client):
        """Test trading without authentication."""
        url = '/api/gold/trade/'
        data = {'type': 'BUY', 'amount': 1.0}
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_buy_gold_success(self, authenticated_client, user):
        """Test successful gold purchase."""
        # Setup initial balance
        user.balance = Decimal('100000.00')
        user.save()
        user.refresh_from_db()
        
        # Create price history
        price = PriceHistoryFactory(price_per_gram=Decimal('2500.00'))
        
        url = '/api/gold/trade/'
        data = {'type': 'BUY', 'amount': 2.0}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'สำเร็จ'
        assert response.data['transaction']['type'] == 'BUY'
        assert response.data['transaction']['amount'] == 2.0
        
        # Verify balance was deducted
        user.refresh_from_db()
        expected_balance = Decimal('100000.00') - (Decimal('2.0') * price.price_per_gram)
        assert user.balance == expected_balance
    
    def test_buy_gold_insufficient_balance(self, authenticated_client, user):
        """Test buying gold with insufficient balance."""
        user.balance = Decimal('100.00')
        user.save()
        
        # Create price history
        price = PriceHistoryFactory(price_per_gram=Decimal('2500.00'))
        
        url = '/api/gold/trade/'
        data = {'type': 'BUY', 'amount': 1.0}  # Cost: 2500, balance: 100
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_sell_gold_success(self, authenticated_client, user):
        """Test successful gold sale."""
        # Create price history
        price = PriceHistoryFactory(price_per_gram=Decimal('2500.00'))
        
        # Create gold holding for user
        GoldHolding.objects.create(
            user=user,
            amount=Decimal('10.000'),
            avg_price=Decimal('2400.00')
        )
        
        # Set initial balance
        initial_balance = Decimal('50000.00')
        user.balance = initial_balance
        user.save()
        user.refresh_from_db()
        
        url = '/api/gold/trade/'
        data = {'type': 'SELL', 'amount': 2.0}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'สำเร็จ'
        assert response.data['transaction']['type'] == 'SELL'
        
        # Verify balance was increased
        user.refresh_from_db()
        expected_balance = initial_balance + (Decimal('2.0') * price.price_per_gram)
        assert user.balance == expected_balance
    
    def test_sell_gold_insufficient_holdings(self, authenticated_client, user):
        """Test selling gold with insufficient holdings."""
        # Create price history
        price = PriceHistoryFactory(price_per_gram=Decimal('2500.00'))
        
        # Create small gold holding
        GoldHolding.objects.create(
            user=user,
            amount=Decimal('1.000'),
            avg_price=Decimal('2400.00')
        )
        
        url = '/api/gold/trade/'
        data = {'type': 'SELL', 'amount': 2.0}  # Have: 1g, Sell: 2g
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_trade_invalid_type(self, authenticated_client, verified_user):
        """Test trading with invalid transaction type."""
        url = '/api/gold/trade/'
        data = {'type': 'INVALID', 'amount': 1.0}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_trade_zero_amount(self, authenticated_client, verified_user):
        """Test trading with zero amount."""
        url = '/api/gold/trade/'
        data = {'type': 'BUY', 'amount': 0}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_trade_no_price_data(self, authenticated_client, verified_user):
        """Test trading when no price data is available."""
        url = '/api/gold/trade/'
        data = {'type': 'BUY', 'amount': 1.0}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
