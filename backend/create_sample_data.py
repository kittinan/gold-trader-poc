from decimal import Decimal
from django.utils import timezone
from django.db import models
from core.models import GoldPrice, Transaction, Wallet
from django.contrib.auth.models import User
import random

# Create or update GoldPrice
price, created = GoldPrice.objects.get_or_create(
    price_per_gram=Decimal('2145.50'),
    price_per_baht=Decimal('32698.00'),
    defaults={
        'currency': 'THB',
        'source': 'Bank of Thailand',
        'timestamp': timezone.now()
    }
)

print(f"Gold price {'created' if created else 'updated'}: {price}")

# Get first user (assuming you have at least one user)
try:
    user = User.objects.first()
    if user:
        print(f"Using user: {user.email}")
        
        # Create or get wallet for the user
        wallet, created = Wallet.objects.get_or_create(
            user=user,
            defaults={
                'balance': Decimal('50000.00'),
                'gold_holdings': Decimal('15.244')  # 1 baht
            }
        )
        print(f"Wallet {'created' if created else 'found'} for {user.email}")
        
        # Create some sample transactions
        transactions_data = [
            {
                'transaction_type': 'BUY',
                'gold_weight': Decimal('5.000'),
                'gold_price_per_gram': Decimal('2100.00'),
                'status': 'COMPLETED'
            },
            {
                'transaction_type': 'BUY', 
                'gold_weight': Decimal('7.244'),
                'gold_price_per_gram': Decimal('2150.00'),
                'status': 'COMPLETED'
            },
            {
                'transaction_type': 'SELL',
                'gold_weight': Decimal('2.000'),
                'gold_price_per_gram': Decimal('2180.00'),
                'status': 'COMPLETED'
            },
            {
                'transaction_type': 'BUY',
                'gold_weight': Decimal('10.000'),
                'gold_price_per_gram': Decimal('2120.00'),
                'status': 'COMPLETED'
            }
        ]
        
        for i, t_data in enumerate(transactions_data):
            transaction, created = Transaction.objects.get_or_create(
                user=user,
                transaction_type=t_data['transaction_type'],
                gold_weight=t_data['gold_weight'],
                gold_price_per_gram=t_data['gold_price_per_gram'],
                defaults={
                    'total_amount': t_data['gold_weight'] * t_data['gold_price_per_gram'],
                    'status': t_data['status'],
                    'transaction_date': timezone.now() - timezone.timedelta(days=i*2)
                }
            )
            print(f"Transaction {i+1}: {transaction.transaction_type} {transaction.gold_weight}g at {transaction.gold_price_per_gram}/g")
        
        # Update wallet gold holdings based on transactions
        buy_total = Transaction.objects.filter(user=user, transaction_type='BUY', status='COMPLETED').aggregate(total=models.Sum('gold_weight'))['total'] or Decimal('0')
        sell_total = Transaction.objects.filter(user=user, transaction_type='SELL', status='COMPLETED').aggregate(total=models.Sum('gold_weight'))['total'] or Decimal('0')
        
        wallet.gold_holdings = buy_total - sell_total
        wallet.save()
        
        print(f"Updated wallet gold holdings: {wallet.gold_holdings}g")
        
    else:
        print("No users found in the database")
        
except Exception as e:
    print(f"Error: {e}")

print("Sample data creation completed!")