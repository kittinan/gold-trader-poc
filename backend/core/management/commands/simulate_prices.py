"""
Django management command to simulate gold price updates.

Usage:
    python manage.py simulate_prices

Options:
    --interval SECONDS    Update interval in seconds (default: 10)
    --count COUNT         Number of updates to send (default: 0 = infinite)
    --min PRICE           Minimum starting price (default: 2500)
    --max PRICE           Maximum starting price (default: 3000)
"""
import time
import random
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from django.db import transaction

from core.models import PriceHistory
from core.services import PriceAlertService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Simulate gold price updates and broadcast via WebSocket'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=10,
            help='Update interval in seconds (default: 10)'
        )
        parser.add_argument(
            '--count',
            type=int,
            default=0,
            help='Number of updates to send (default: 0 = infinite)'
        )
        parser.add_argument(
            '--min',
            type=float,
            default=2500.0,
            help='Minimum starting price (default: 2500)'
        )
        parser.add_argument(
            '--max',
            type=float,
            default=3000.0,
            help='Maximum starting price (default: 3000)'
        )
        parser.add_argument(
            '--persist',
            action='store_true',
            help='Save prices to database (PriceHistory model)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        count = options['count']
        min_price = Decimal(str(options['min']))
        max_price = Decimal(str(options['max']))
        persist = options['persist']

        self.stdout.write(self.style.SUCCESS(
            f'\n=== Gold Price Simulator Started ===\n'
            f'Interval: {interval} seconds\n'
            f'Max updates: {"Infinite" if count == 0 else count}\n'
            f'Price range: {min_price} - {max_price} THB/gram\n'
            f'Persist to DB: {"Yes" if persist else "No"}\n'
        ))

        update_count = 0
        current_price = (min_price + max_price) / 2

        try:
            while True:
                if count > 0 and update_count >= count:
                    self.stdout.write(self.style.SUCCESS('\n=== Simulation completed ==='))
                    break

                update_count += 1
                timestamp = timezone.now()

                # Simulate price movement (-2% to +2%)
                change_percent = random.uniform(-0.02, 0.02)
                current_price = current_price * (1 + change_percent)

                # Ensure price stays within bounds
                if current_price < min_price:
                    current_price = min_price
                elif current_price > max_price:
                    current_price = max_price

                # Calculate price per baht (15.244 grams per baht)
                price_per_baht = current_price * Decimal('15.244')

                price_data = {
                    'price_per_gram': current_price,
                    'price_per_baht': price_per_baht,
                    'currency': 'THB',
                    'timestamp': timestamp,
                }

                # Persist to database if requested
                if persist:
                    with transaction.atomic():
                        PriceHistory.objects.create(
                            price_per_gram=current_price,
                            price_per_baht=price_per_baht,
                            currency='THB',
                            timestamp=timestamp,
                            source='SIMULATOR'
                        )

                # Broadcast via WebSocket
                PriceAlertService.broadcast_price_update(price_data)

                self.stdout.write(
                    f'[{update_count}] {timestamp.strftime("%H:%M:%S")} - '
                    f'Price: {current_price:.2f} THB/g ({price_per_baht:.2f} THB/baht) - '
                    f'Change: {change_percent*100:+.2f}%'
                )

                time.sleep(interval)

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n\nSimulation stopped by user'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nError: {e}'))
            raise
