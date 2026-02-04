"""
Unit tests for Wallet and GoldHolding models.
"""
import pytest
from decimal import Decimal
from core.models import Wallet, GoldHolding
from tests.factories.wallet_factory import WalletFactory, GoldHoldingFactory
from tests.factories.user_factory import UserFactory


class TestWalletModel:
    """Test cases for Wallet model."""
    
    def test_create_wallet(self):
        """Test creating a wallet."""
        user = UserFactory()
        wallet = Wallet.objects.create(
            user=user,
            balance=Decimal('50000.00'),
            gold_holdings=Decimal('5.000')
        )
        
        assert wallet.user == user
        assert wallet.balance == Decimal('50000.00')
        assert wallet.gold_holdings == Decimal('5.000')
    
    def test_wallet_factory(self):
        """Test Wallet factory."""
        wallet = WalletFactory()
        
        assert isinstance(wallet, Wallet)
        assert wallet.user is not None
        assert wallet.balance == Decimal('50000.00')
        assert wallet.gold_holdings == Decimal('5.000')
    
    def test_wallet_str_representation(self):
        """Test string representation of Wallet."""
        user = UserFactory(email='test@example.com')
        wallet = WalletFactory(
            user=user,
            balance=Decimal('100000.00'),
            gold_holdings=Decimal('10.000')
        )
        
        str_repr = str(wallet)
        assert 'test@example.com' in str_repr
        assert '100000.00' in str_repr
        assert '10.000' in str_repr
    
    def test_wallet_one_to_one_user_relationship(self):
        """Test one-to-one relationship with User."""
        user = UserFactory()
        wallet = WalletFactory(user=user)
        
        assert wallet.user == user
        assert user.wallet == wallet
    
    def test_wallet_timestamps(self):
        """Test created_at and updated_at fields."""
        wallet = WalletFactory()
        
        assert wallet.created_at is not None
        assert wallet.updated_at is not None
    
    def test_wallet_default_values(self):
        """Test default values for wallet."""
        user = UserFactory()
        wallet = Wallet.objects.create(user=user)
        
        assert wallet.balance == Decimal('0.00')
        assert wallet.gold_holdings == Decimal('0.000')
    
    def test_wallet_balance_precision(self):
        """Test balance precision (2 decimal places)."""
        wallet = WalletFactory(balance=Decimal('12345.67'))
        
        assert wallet.balance == Decimal('12345.67')
    
    def test_wallet_gold_holdings_precision(self):
        """Test gold holdings precision (3 decimal places)."""
        wallet = WalletFactory(gold_holdings=Decimal('12.345'))
        
        assert wallet.gold_holdings == Decimal('12.345')


class TestGoldHoldingModel:
    """Test cases for GoldHolding model."""
    
    def test_create_gold_holding(self):
        """Test creating a gold holding."""
        user = UserFactory()
        holding = GoldHolding.objects.create(
            user=user,
            amount=Decimal('10.000'),
            avg_price=Decimal('2400.00')
        )
        
        assert holding.user == user
        assert holding.amount == Decimal('10.000')
        assert holding.avg_price == Decimal('2400.00')
        assert holding.total_value == Decimal('24000.00')  # 10 * 2400
    
    def test_gold_holding_factory(self):
        """Test GoldHolding factory."""
        holding = GoldHoldingFactory()
        
        assert isinstance(holding, GoldHolding)
        assert holding.user is not None
        assert holding.amount == Decimal('10.000')
        assert holding.avg_price == Decimal('2400.00')
    
    def test_gold_holding_total_value_auto_calculation(self):
        """Test total_value auto-calculation on save."""
        holding = GoldHolding.objects.create(
            user=UserFactory(),
            amount=Decimal('5.000'),
            avg_price=Decimal('2500.00')
        )
        
        assert holding.total_value == holding.amount * holding.avg_price
        assert holding.total_value == Decimal('12500.00')
    
    def test_gold_holding_str_representation(self):
        """Test string representation of GoldHolding."""
        user = UserFactory(email='test@example.com')
        holding = GoldHoldingFactory(
            user=user,
            amount=Decimal('10.000'),
            avg_price=Decimal('2400.00')
        )
        
        str_repr = str(holding)
        assert 'test@example.com' in str_repr
        assert '10.000' in str_repr
        assert '2400.00' in str_repr
    
    def test_gold_holding_user_relationship(self):
        """Test gold holding-user relationship."""
        user = UserFactory()
        holding = GoldHoldingFactory(user=user)
        
        assert holding.user == user
        assert holding in user.gold_holdings.all()
    
    def test_gold_holding_timestamps(self):
        """Test created_at and updated_at fields."""
        holding = GoldHoldingFactory()
        
        assert holding.created_at is not None
        assert holding.updated_at is not None
    
    def test_gold_holding_ordering(self):
        """Test gold holdings ordering by updated_at."""
        old_holding = GoldHoldingFactory()
        new_holding = GoldHoldingFactory()
        
        # Query should order by -updated_at
        all_holdings = list(GoldHolding.objects.all())
        assert all_holdings[0].updated_at >= all_holdings[1].updated_at
    
    def test_multiple_gold_holdings_for_user(self):
        """Test multiple gold holdings for a single user."""
        user = UserFactory()
        count = 3
        
        holdings = [
            GoldHoldingFactory(user=user) for _ in range(count)
        ]
        
        assert len(holdings) == count
        assert user.gold_holdings.count() == count
        assert all(h.user == user for h in holdings)
    
    def test_gold_holding_amount_precision(self):
        """Test gold amount precision (3 decimal places)."""
        holding = GoldHoldingFactory(amount=Decimal('12.345'))
        
        assert holding.amount == Decimal('12.345')
    
    def test_gold_holding_avg_price_precision(self):
        """Test average price precision (2 decimal places)."""
        holding = GoldHoldingFactory(avg_price=Decimal('2345.67'))
        
        assert holding.avg_price == Decimal('2345.67')
    
    def test_gold_holding_total_value_precision(self):
        """Test total value precision (2 decimal places)."""
        holding = GoldHoldingFactory(
            amount=Decimal('5.123'),
            avg_price=Decimal('2345.67')
        )
        
        expected_value = holding.amount * holding.avg_price
        assert holding.total_value == expected_value
        # Check precision
        assert abs(holding.total_value - Decimal('12019.91')) < Decimal('0.01')
    
    def test_gold_holding_update(self):
        """Test updating gold holding recalculates total_value."""
        holding = GoldHoldingFactory(
            amount=Decimal('10.000'),
            avg_price=Decimal('2000.00')
        )
        
        assert holding.total_value == Decimal('20000.00')
        
        # Update amount
        holding.amount = Decimal('15.000')
        holding.save()
        
        assert holding.total_value == Decimal('30000.00')  # 15 * 2000
