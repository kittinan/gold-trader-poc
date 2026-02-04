"""
Factory for creating Transaction instances for testing.
"""
import factory
from decimal import Decimal
from core.models import Transaction
from .user_factory import UserFactory
from .gold_price_factory import GoldPriceFactory


class TransactionFactory(factory.django.DjangoModelFactory):
    """Factory for creating transaction records."""
    
    class Meta:
        model = Transaction
    
    user = factory.SubFactory(UserFactory)
    transaction_type = 'BUY'
    gold_weight = factory.LazyFunction(lambda: Decimal('2.000'))
    gold_price_per_gram = factory.LazyFunction(lambda: Decimal('2500.00'))
    total_amount = factory.LazyAttribute(lambda obj: obj.gold_weight * obj.gold_price_per_gram)
    status = 'COMPLETED'


class BuyTransactionFactory(TransactionFactory):
    """Factory for creating BUY transactions."""
    
    transaction_type = 'BUY'
    gold_weight = factory.LazyFunction(lambda: Decimal('5.000'))


class SellTransactionFactory(TransactionFactory):
    """Factory for creating SELL transactions."""
    
    transaction_type = 'SELL'
    gold_weight = factory.LazyFunction(lambda: Decimal('2.000'))


class PendingTransactionFactory(TransactionFactory):
    """Factory for creating PENDING transactions."""
    
    status = 'PENDING'
