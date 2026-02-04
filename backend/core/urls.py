from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileView,
    LogoutAPIView,
    TokenRefreshViewCustom,
    user_me_view,
    # Gold holdings views
    GoldHoldingsListView,
    GoldHoldingDetailView,
    GoldHoldingsSummaryView,
    GoldHoldingsView,
    # Price history views
    PriceHistoryListView,
    PriceHistoryDetailView,
    CurrentGoldPriceView,
    # Deposit views
    DepositListView,
    DepositCreateView,
    DepositCompleteView,
    DepositDetailView,
    WalletBalanceView,
)

app_name = 'core'

urlpatterns = [
    # ==================== Authentication endpoints ====================
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshViewCustom.as_view(), name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/me/', user_me_view, name='user_me'),

    # ==================== Gold Holdings endpoints ====================
    path('gold/holdings/', GoldHoldingsListView.as_view(), name='gold_holdings_list'),
    path('gold/holdings/<int:pk>/', GoldHoldingDetailView.as_view(), name='gold_holding_detail'),
    path('gold/summary/', GoldHoldingsSummaryView.as_view(), name='gold_summary'),

    # ==================== Price History endpoints ====================
    path('gold/prices/', PriceHistoryListView.as_view(), name='price_history_list'),
    path('gold/prices/<int:pk>/', PriceHistoryDetailView.as_view(), name='price_history_detail'),
    path('gold/prices/current/', CurrentGoldPriceView.as_view(), name='current_price'),

    # ==================== Deposit endpoints ====================
    path('wallet/deposits/', DepositListView.as_view(), name='deposit_list'),
    path('wallet/deposits/<int:pk>/', DepositDetailView.as_view(), name='deposit_detail'),
    path('wallet/deposit/create/', DepositCreateView.as_view(), name='deposit_create'),
    path('wallet/deposit/complete/', DepositCompleteView.as_view(), name='deposit_complete'),
    path('wallet/balance/', WalletBalanceView.as_view(), name='wallet_balance'),
]
