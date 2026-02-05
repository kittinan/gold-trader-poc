from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/gold-price/$', consumers.GoldPriceConsumer.as_asgi()),
    re_path(r'ws/alerts/$', consumers.PriceAlertConsumer.as_asgi()),
]
