import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BaseConsumer(AsyncWebsocketConsumer):
    """
    Base WebSocket consumer for real-time features.
    """

    async def connect(self):
        """Handle new WebSocket connection."""
        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        pass

    async def receive(self, text_data):
        """Handle incoming WebSocket message."""
        data = json.loads(text_data)
        # Process the data
        await self.send(text_data=json.dumps({
            'status': 'received',
            'data': data
        }))


class GoldPriceConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time gold price updates.
    """

    async def connect(self):
        """Join the gold price updates group."""
        self.group_name = 'gold_price_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Leave the gold price updates group."""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def gold_price_update(self, event):
        """Send gold price update to the client."""
        await self.send(text_data=json.dumps(event.get('data', event)))


class PriceAlertConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for price alert notifications.
    """

    async def connect(self):
        """Join the user's alert group."""
        # Get user_id from the URL (if authenticated)
        # For now, we'll get it from the scope if authentication is set up
        user_id = self.scope.get('user_id')
        if user_id:
            self.group_name = f'user_{user_id}_alerts'
        else:
            # Fallback to a test group
            self.group_name = 'price_alerts_all'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Leave the user's alert group."""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_alert_notification(self, event):
        """Send alert notification to the client."""
        await self.send(text_data=json.dumps(event.get('message', event)))
