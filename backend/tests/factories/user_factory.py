"""
Factory for creating User instances for testing.
"""
import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating test users."""
    
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone_number = factory.Faker('phone_number')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    is_verified = False
    balance = factory.LazyAttribute(lambda obj: 0.00)
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to create user with password."""
        password = kwargs.pop('password', 'testpass123')
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, password=password, **kwargs)


class VerifiedUserFactory(UserFactory):
    """Factory for creating verified users."""
    
    is_verified = True
    balance = 100000.00


class AdminUserFactory(UserFactory):
    """Factory for creating admin users."""
    
    is_staff = True
    is_superuser = True
    is_verified = True
