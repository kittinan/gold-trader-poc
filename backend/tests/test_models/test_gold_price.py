"""
Unit tests for GoldPrice and PriceHistory models.
"""
import pytest
from decimal import Decimal
from core.models import GoldPrice, PriceHistory
from tests.factories.gold_price_factory import GoldPriceFactory, PriceHistoryFactory, VariablePriceHistoryFactory


@pytest.mark.django_db
class TestGoldPriceModel:
    """Test cases for GoldPrice model."""
    
    def test_create_gold_price(self):
        """Test creating a gold price record."""
        gold_price = GoldPrice.objects.create(
            price_per_gram=Decimal('2500.00'),
            price_per_baht=Decimal('38050.00'),
            currency='THB',
            source='Test Source'
        )
        
        assert gold_price.price_per_gram == Decimal('2500.00')
        assert gold_price.price_per_baht == Decimal('38050.00')
        assert gold_price.currency == 'THB'
        assert gold_price.source == 'Test Source'
    
    def test_gold_price_factory(self):
        """Test GoldPrice factory."""
        gold_price = GoldPriceFactory()
        
        assert isinstance(gold_price, GoldPrice)
        assert gold_price.currency == 'THB'
    
    def test_gold_price_str_representation(self):
        """Test string representation of GoldPrice."""
        gold_price = GoldPriceFactory(
            price_per_baht=Decimal('38050.00')
        )
        
        str_repr = str(gold_price)
        assert '38050.00' in str_repr
        assert 'THB/baht' in str_repr
    
    def test_gold_price_default_timestamp(self):
        """Test default timestamp field."""
        gold_price = GoldPriceFactory()
        
        assert gold_price.timestamp is not None
    
    def test_multiple_gold_prices(self):
        """Test creating multiple gold prices."""
        count = 5
        gold_prices = [GoldPriceFactory() for _ in range(count)]
        
        assert len(gold_prices) == count
        assert all(isinstance(gp, GoldPrice) for gp in gold_prices)
    
    def test_gold_price_ordering(self):
        """Test gold prices ordering by timestamp."""
        old_price = GoldPriceFactory()
        new_price = GoldPriceFactory()
        
        # Query should order by -timestamp
        all_prices = list(GoldPrice.objects.all())
        assert all_prices[0].timestamp >= all_prices[1].timestamp


@pytest.mark.django_db
class TestPriceHistoryModel:
    """Test cases for PriceHistory model."""
    
    def test_create_price_history(self):
        """Test creating a price history record."""
        price_history = PriceHistory.objects.create(
            price_per_gram=Decimal('2500.00'),
            price_per_baht=Decimal('38050.00'),
            currency='THB',
            source='Test Source',
            notes='Historical price'
        )
        
        assert price_history.price_per_gram == Decimal('2500.00')
        assert price_history.price_per_baht == Decimal('38050.00')
        assert price_history.currency == 'THB'
        assert price_history.source == 'Test Source'
        assert price_history.notes == 'Historical price'
    
    def test_price_history_factory(self):
        """Test PriceHistory factory."""
        price_history = PriceHistoryFactory()
        
        assert isinstance(price_history, PriceHistory)
        assert price_history.currency == 'THB'
    
    def test_price_history_str_representation(self):
        """Test string representation of PriceHistory."""
        price_history = PriceHistoryFactory(
            price_per_baht=Decimal('38050.00')
        )
        
        str_repr = str(price_history)
        assert '38050.00' in str_repr
        assert 'THB/baht' in str_repr
    
    def test_variable_price_history_factory(self):
        """Test VariablePriceHistoryFactory creates different prices."""
        price_histories = [VariablePriceHistoryFactory() for _ in range(5)]
        
        # Extract prices
        prices = [ph.price_per_gram for ph in price_histories]
        
        # Prices should be different (increasing)
        assert len(set(prices)) > 1
        assert prices == sorted(prices)
    
    def test_price_history_notes_field(self):
        """Test notes field in PriceHistory."""
        notes = 'Important price update due to market changes'
        price_history = PriceHistoryFactory(notes=notes)
        
        assert price_history.notes == notes
    
    def test_price_history_ordering(self):
        """Test price history ordering by timestamp."""
        old_history = PriceHistoryFactory()
        new_history = PriceHistoryFactory()
        
        # Query should order by -timestamp
        all_history = list(PriceHistory.objects.all())
        assert all_history[0].timestamp >= all_history[1].timestamp
    
    def test_price_history_blank_fields(self):
        """Test blank fields in PriceHistory."""
        price_history = PriceHistory.objects.create(
            price_per_gram=Decimal('2500.00'),
            price_per_baht=Decimal('38050.00'),
            currency='THB',
            source='',
            notes=''
        )
        
        assert price_history.source == ''
        assert price_history.notes == ''
    
    def test_calculate_baht_from_gram(self):
        """Test baht calculation from gram (1 baht = 15.244 grams)."""
        price_per_gram = Decimal('2500.00')
        expected_baht = price_per_gram * Decimal('15.244')
        
        price_history = PriceHistoryFactory(
            price_per_gram=price_per_gram,
            price_per_baht=expected_baht
        )
        
        assert price_history.price_per_baht == expected_baht
