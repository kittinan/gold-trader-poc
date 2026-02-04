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
        await self.send(text_data=json.dumps(event))
