"""
Factory for creating Wallet and GoldHolding instances for testing.
"""
import factory
from decimal import Decimal
from core.models import Wallet, GoldHolding
from .user_factory import UserFactory


class WalletFactory(factory.django.DjangoModelFactory):
    """Factory for creating wallet records."""
    
    class Meta:
        model = Wallet
    
    user = factory.SubFactory(UserFactory)
    balance = factory.LazyFunction(lambda: Decimal('50000.00'))
    gold_holdings = factory.LazyFunction(lambda: Decimal('5.000'))


class GoldHoldingFactory(factory.django.DjangoModelFactory):
    """Factory for creating gold holding records."""
    
    class Meta:
        model = GoldHolding
    
    user = factory.SubFactory(UserFactory)
    amount = factory.LazyFunction(lambda: Decimal('10.000'))
    avg_price = factory.LazyFunction(lambda: Decimal('2400.00'))
    total_value = factory.LazyAttribute(lambda obj: obj.amount * obj.avg_price)
