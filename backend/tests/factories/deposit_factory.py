"""
Factory for creating Deposit instances for testing.
"""
import factory
from decimal import Decimal
from core.models import Deposit
from .user_factory import UserFactory


class DepositFactory(factory.django.DjangoModelFactory):
    """Factory for creating deposit records."""
    
    class Meta:
        model = Deposit
    
    user = factory.SubFactory(UserFactory)
    amount = factory.LazyFunction(lambda: Decimal('10000.00'))
    status = 'PENDING'
    reference = factory.Sequence(lambda n: f'DEPOSIT-{n:06d}')


class CompletedDepositFactory(DepositFactory):
    """Factory for creating completed deposits."""
    
    status = 'COMPLETED'
    amount = factory.LazyFunction(lambda: Decimal('50000.00'))


class FailedDepositFactory(DepositFactory):
    """Factory for creating failed deposits."""
    
    status = 'FAILED'
