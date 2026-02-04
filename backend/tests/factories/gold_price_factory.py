"""
Factory for creating GoldPrice instances for testing.
"""
import factory
from decimal import Decimal
from core.models import GoldPrice, PriceHistory


class GoldPriceFactory(factory.django.DjangoModelFactory):
    """Factory for creating gold price records."""
    
    class Meta:
        model = GoldPrice
    
    price_per_gram = factory.LazyFunction(lambda: Decimal('2500.00'))
    price_per_baht = factory.LazyFunction(lambda: Decimal('38050.00'))
    currency = 'THB'
    source = 'Test Source'


class PriceHistoryFactory(factory.django.DjangoModelFactory):
    """Factory for creating price history records."""
    
    class Meta:
        model = PriceHistory
    
    price_per_gram = factory.LazyFunction(lambda: Decimal('2500.00'))
    price_per_baht = factory.LazyFunction(lambda: Decimal('38050.00'))
    currency = 'THB'
    source = 'Test Source'
    notes = factory.Faker('text', max_nb_chars=100)


class VariablePriceHistoryFactory(PriceHistoryFactory):
    """Factory for creating price history with variable prices."""
    
    price_per_gram = factory.Sequence(lambda n: Decimal('2500.00') + (n * Decimal('10.00')))
    price_per_baht = factory.Sequence(lambda n: Decimal('38050.00') + (n * Decimal('152.00')))
