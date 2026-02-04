from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileView,
    LogoutAPIView,
    TokenRefreshViewCustom,
    user_me_view,
)

app_name = 'core'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshViewCustom.as_view(), name='token_refresh'),

    # User profile endpoints
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/me/', user_me_view, name='user_me'),
]
