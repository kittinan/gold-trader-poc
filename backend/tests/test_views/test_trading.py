import pytest
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from core.models import Transaction, GoldHolding

@pytest.mark.django_db
class TestTradingViews:
    def test_get_gold_holdings(self, authenticated_client, gold_holding):
        url = reverse('core:gold_holdings_list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert Decimal(str(response.data[0]['amount'])) == gold_holding.amount

    def test_buy_gold_success(self, authenticated_client, user, price_history):
        user.balance = Decimal('10000.00')
        user.save()
        
        url = reverse('core:gold_trade')
        data = {'type': 'BUY', 'amount': 2.0}
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert Transaction.objects.filter(user=user, transaction_type='BUY').exists()
        
        user.refresh_from_db()
        expected_balance = Decimal('10000.00') - (Decimal('2.0') * price_history.price_per_gram)
        assert user.balance == expected_balance
        
        holding = GoldHolding.objects.get(user=user)
        assert holding.amount == Decimal('2.0')

    def test_buy_gold_insufficient_balance(self, authenticated_client, user, price_history):
        user.balance = Decimal('100.00')
        user.save()
        
        url = reverse('core:gold_trade')
        data = {'type': 'BUY', 'amount': 10.0}
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'ยอดเงินไม่เพียงพอ' in response.data['error']

    def test_sell_gold_success(self, authenticated_client, user, gold_holding, price_history):
        user.balance = Decimal('0.00')
        user.save()
        
        url = reverse('core:gold_trade')
        data = {'type': 'SELL', 'amount': 5.0}
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        
        user.refresh_from_db()
        expected_balance = Decimal('5.0') * price_history.price_per_gram
        assert user.balance == expected_balance
        
        gold_holding.refresh_from_db()
        assert gold_holding.amount == Decimal('5.000') # 10 - 5
