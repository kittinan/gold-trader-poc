"""
Services for Gold Trader application.
"""
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import PriceAlert, PriceHistory

logger = logging.getLogger(__name__)


class PriceAlertService:
    """
    Service for managing price alerts.
    """

    @staticmethod
    def check_and_trigger_alerts(current_price):
        """
        Check all active alerts and trigger those that meet the condition.

        Args:
            current_price (Decimal): Current gold price per gram

        Returns:
            list: List of triggered alerts
        """
        if current_price is None:
            logger.warning("Cannot check alerts: current_price is None")
            return []

        triggered_alerts = []

        # Get all active and non-triggered alerts
        active_alerts = PriceAlert.objects.filter(
            is_active=True,
            is_triggered=False
        ).select_related('user')

        for alert in active_alerts:
            if alert.check_alert(current_price):
                if alert.trigger():
                    triggered_alerts.append(alert)
                    logger.info(f"Alert triggered: {alert.user.email} - {alert.condition} {alert.target_price}")

                    # Send notification via WebSocket
                    PriceAlertService._send_alert_notification(alert, current_price)

        return triggered_alerts

    @staticmethod
    def _send_alert_notification(alert, current_price):
        """
        Send alert notification via WebSocket to the user.

        Args:
            alert (PriceAlert): The triggered alert
            current_price (Decimal): Current gold price
        """
        try:
            channel_layer = get_channel_layer()
            group_name = f"user_{alert.user.id}_alerts"

            message = {
                'type': 'price_alert_triggered',
                'alert_id': alert.id,
                'user_id': alert.user.id,
                'target_price': float(alert.target_price),
                'condition': alert.condition,
                'current_price': float(current_price),
                'triggered_at': alert.triggered_at.isoformat() if alert.triggered_at else None,
                'message': f"Price alert triggered: Gold price is now {current_price} THB/g (your target was {alert.condition} {alert.target_price})"
            }

            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_alert_notification',
                    'message': message
                }
            )
        except Exception as e:
            logger.error(f"Failed to send alert notification: {e}")

    @staticmethod
    def broadcast_price_update(price_data):
        """
        Broadcast gold price update to all connected clients.

        Args:
            price_data (dict): Dictionary containing price information
                - price_per_gram: Decimal
                - price_per_baht: Decimal
                - currency: str
                - timestamp: datetime
        """
        try:
            channel_layer = get_channel_layer()

            message = {
                'type': 'gold_price_update',
                'price_per_gram': float(price_data.get('price_per_gram', 0)),
                'price_per_baht': float(price_data.get('price_per_baht', 0)),
                'currency': price_data.get('currency', 'THB'),
                'timestamp': price_data.get('timestamp', timezone.now()).isoformat(),
            }

            # Broadcast to all gold price subscribers
            async_to_sync(channel_layer.group_send)(
                'gold_price_updates',
                {
                    'type': 'gold_price_update',
                    'data': message
                }
            )

            # Also check for triggered alerts
            current_price = price_data.get('price_per_gram')
            if current_price:
                PriceAlertService.check_and_trigger_alerts(current_price)

        except Exception as e:
            logger.error(f"Failed to broadcast price update: {e}")
