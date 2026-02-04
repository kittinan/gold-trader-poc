from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GoldPriceViewSet, TransactionViewSet, WalletViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'gold-prices', GoldPriceViewSet, basename='gold-price')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'wallets', WalletViewSet, basename='wallet')

urlpatterns = [
    path('', include(router.urls)),
]
