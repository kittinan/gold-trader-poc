from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # ==================== Authentication endpoints ====================
    path('auth/register/', views.RegisterAPIView.as_view(), name='register'),
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('auth/token/refresh/', views.TokenRefreshViewCustom.as_view(), name='token_refresh'),
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),
    path('auth/me/', views.user_me_view, name='user_me'),

    # ==================== Gold Holdings endpoints ====================
    path('gold/holdings/', views.GoldHoldingsListView.as_view(), name='gold_holdings_list'),
    path('gold/holdings/<int:pk>/', views.GoldHoldingDetailView.as_view(), name='gold_holding_detail'),
    path('gold/summary/', views.GoldHoldingsSummaryView.as_view(), name='gold_summary'),

    # ==================== Price History endpoints ====================
    path('gold/prices/', views.PriceHistoryListView.as_view(), name='price_history_list'),
    path('gold/prices/<int:pk>/', views.PriceHistoryDetailView.as_view(), name='price_history_detail'),
    path('gold/prices/current/', views.CurrentGoldPriceView.as_view(), name='current_price'),

    # ==================== Trading endpoints ====================
    path('gold/trade/', views.TradeAPIView.as_view(), name='gold_trade'),
    path('gold/transactions/', views.TransactionListView.as_view(), name='gold_transactions'),

    # ==================== Deposit endpoints ====================
    path('wallet/deposits/', views.DepositListView.as_view(), name='deposit_list'),
    path('wallet/deposits/<int:pk>/', views.DepositDetailView.as_view(), name='deposit_detail'),
    path('wallet/deposit/create/', views.DepositCreateView.as_view(), name='deposit_create'),
    path('wallet/deposit/complete/', views.MockDepositProcessView.as_view(), name='deposit_complete'),
    path('wallet/balance/', views.WalletBalanceView.as_view(), name='wallet_balance'),

    # ==================== Price Alert endpoints ====================
    path('alerts/', views.PriceAlertListView.as_view(), name='price_alert_list'),
    path('alerts/<int:pk>/', views.PriceAlertDetailView.as_view(), name='price_alert_detail'),
    path('alerts/<int:pk>/toggle/', views.PriceAlertToggleView.as_view(), name='price_alert_toggle'),
]
