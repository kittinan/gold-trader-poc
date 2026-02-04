from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.db.models import Sum, F
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User, GoldHolding, PriceHistory
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UserSerializer,
    GoldHoldingSerializer,
    GoldHoldingCreateSerializer,
    PriceHistorySerializer,
    PriceHistoryCreateSerializer,
)


class RegisterAPIView(APIView):
    """
    API endpoint for user registration.
    POST /api/auth/register/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate tokens for the new user
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Registration successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    API endpoint for user login.
    POST /api/auth/login/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                }, status=status.HTTP_200_OK)

            return Response({
                'error': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user profile.
    GET /api/auth/profile/
    PATCH /api/auth/profile/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        return self.request.user

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            # Return the full profile with all fields
            full_serializer = UserProfileSerializer(request.user)
            return Response(full_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """
    API endpoint for user logout.
    POST /api/auth/logout/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid refresh token'
            }, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshViewCustom(TokenRefreshView):
    """
    Custom token refresh view.
    POST /api/auth/token/refresh/
    """
    pass


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_me_view(request):
    """
    Simple endpoint to get current user info.
    GET /api/auth/me/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ==================== Gold Holdings Views ====================

class GoldHoldingsListView(generics.ListCreateAPIView):
    """
    API endpoint to list and create user gold holdings.
    GET /api/gold/holdings/ - List user's gold holdings
    POST /api/gold/holdings/ - Create new gold holding entry
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GoldHoldingCreateSerializer
        return GoldHoldingSerializer

    def get_queryset(self):
        return GoldHolding.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoldHoldingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific gold holding.
    GET /api/gold/holdings/:id/ - Get specific holding
    PUT /api/gold/holdings/:id/ - Update holding
    PATCH /api/gold/holdings/:id/ - Partial update holding
    DELETE /api/gold/holdings/:id/ - Delete holding
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoldHoldingCreateSerializer

    def get_queryset(self):
        return GoldHolding.objects.filter(user=self.request.user)


class GoldHoldingsSummaryView(APIView):
    """
    API endpoint to get user's gold holdings summary with total value.
    GET /api/gold/summary/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        holdings = GoldHolding.objects.filter(user=request.user)

        # Calculate totals
        total_amount = holdings.aggregate(total=Sum('amount'))['total'] or 0
        total_cost = holdings.aggregate(cost=Sum(F('amount') * F('avg_price')))['cost'] or 0

        # Get latest price for current value calculation
        latest_price = PriceHistory.objects.order_by('-timestamp').first()
        current_value = 0
        profit_loss = 0
        profit_loss_percent = 0

        if latest_price:
            current_value = total_amount * latest_price.price_per_gram
            if total_cost > 0:
                profit_loss = current_value - total_cost
                profit_loss_percent = (profit_loss / total_cost) * 100

        response_data = {
            'total_amount': float(total_amount),
            'total_cost': float(total_cost),
            'current_price_per_gram': float(latest_price.price_per_gram) if latest_price else 0,
            'current_price_per_baht': float(latest_price.price_per_baht) if latest_price else 0,
            'current_value': float(current_value),
            'profit_loss': float(profit_loss),
            'profit_loss_percent': float(profit_loss_percent),
            'holdings_count': holdings.count(),
        }

        return Response(response_data, status=status.HTTP_200_OK)


# ==================== Price History Views ====================

class PriceHistoryListView(generics.ListCreateAPIView):
    """
    API endpoint to list and create price history records.
    GET /api/gold/prices/ - List price history
    POST /api/gold/prices/ - Create new price record (admin only)
    """
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # Only allow creating by admins or authenticated users
            if self.request.user.is_authenticated and self.request.user.is_staff:
                return PriceHistoryCreateSerializer
            else:
                return PriceHistorySerializer
        return PriceHistorySerializer

    def get_queryset(self):
        queryset = PriceHistory.objects.all()
        # Optional: limit results by query param
        limit = self.request.query_params.get('limit', None)
        if limit:
            queryset = queryset[:int(limit)]
        return queryset

    def perform_create(self, serializer):
        # Only staff can create price history
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Only admins can create price history.")
        serializer.save()


class PriceHistoryDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve a specific price history record.
    GET /api/gold/prices/:id/ - Get specific price record
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PriceHistorySerializer
    queryset = PriceHistory.objects.all()


class CurrentGoldPriceView(APIView):
    """
    API endpoint to get the latest gold price.
    GET /api/gold/prices/current/
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        latest_price = PriceHistory.objects.order_by('-timestamp').first()

        if not latest_price:
            return Response({
                'error': 'No price data available'
            }, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'price_per_gram': float(latest_price.price_per_gram),
            'price_per_baht': float(latest_price.price_per_baht),
            'currency': latest_price.currency,
            'timestamp': latest_price.timestamp,
            'source': latest_price.source,
        }

        return Response(response_data, status=status.HTTP_200_OK)


# Gold Holdings Views
from .models import Wallet, Transaction, GoldPrice
from decimal import Decimal


class GoldHoldingsView(APIView):
    """
    API endpoint for getting user's gold holdings information.
    GET /api/gold-holdings/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get comprehensive gold holdings information including:
        - Current gold holdings (total grams)
        - Average purchase price
        - Current market value
        - Profit/loss calculation
        - Transaction history for profit calculation
        """
        try:
            # Get or create user's wallet
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            
            # Get user's completed BUY transactions
            buy_transactions = Transaction.objects.filter(
                user=request.user,
                transaction_type='BUY',
                status='COMPLETED'
            ).order_by('transaction_date')
            
            # Get user's completed SELL transactions
            sell_transactions = Transaction.objects.filter(
                user=request.user,
                transaction_type='SELL',
                status='COMPLETED'
            ).order_by('transaction_date')
            
            # Calculate total gold bought and sold
            total_bought = sum(t.gold_weight for t in buy_transactions)
            total_sold = sum(t.gold_weight for t in sell_transactions)
            
            # Calculate weighted average purchase price
            total_cost = sum(t.gold_weight * t.gold_price_per_gram for t in buy_transactions)
            avg_purchase_price = total_cost / total_bought if total_bought > 0 else Decimal('0')
            
            # Get current gold price
            current_gold_price = GoldPrice.objects.first()
            current_price_per_gram = current_gold_price.price_per_gram if current_gold_price else Decimal('0')
            
            # Calculate current market value
            current_market_value = wallet.gold_holdings * current_price_per_gram
            
            # Calculate total cost of holdings (FIFO method - simplified)
            # For simplicity, we'll use the average purchase price
            total_cost_of_holdings = wallet.gold_holdings * avg_purchase_price
            
            # Calculate unrealized profit/loss
            unrealized_pl = current_market_value - total_cost_of_holdings
            unrealized_pl_percent = (unrealized_pl / total_cost_of_holdings * 100) if total_cost_of_holdings > 0 else Decimal('0')
            
            # Calculate realized profit/loss from sell transactions
            realized_pl = sum(
                (t.gold_price_per_gram - avg_purchase_price) * t.gold_weight 
                for t in sell_transactions
            )
            
            # Get recent transactions
            recent_transactions = Transaction.objects.filter(
                user=request.user,
                status='COMPLETED'
            ).order_by('-transaction_date')[:10]
            
            # Serialize transaction data
            from .serializers import TransactionSerializer
            recent_transactions_data = TransactionSerializer(recent_transactions, many=True).data
            
            response_data = {
                'current_holdings': {
                    'gold_weight_grams': float(wallet.gold_holdings),
                    'gold_weight_baht': float(wallet.gold_holdings / 15.244),  # Convert grams to baht
                    'average_purchase_price_per_gram': float(avg_purchase_price),
                    'average_purchase_price_per_baht': float(avg_purchase_price * 15.244),
                },
                'market_value': {
                    'current_price_per_gram': float(current_price_per_gram),
                    'current_price_per_baht': float(current_price_per_gram * 15.244) if current_price_per_gram else 0,
                    'current_market_value_thb': float(current_market_value),
                    'total_cost_thb': float(total_cost_of_holdings),
                },
                'profit_loss': {
                    'unrealized_pl_thb': float(unrealized_pl),
                    'unrealized_pl_percent': float(unrealized_pl_percent),
                    'realized_pl_thb': float(realized_pl),
                    'total_pl_thb': float(unrealized_pl + realized_pl),
                },
                'transactions': {
                    'total_buy_transactions': buy_transactions.count(),
                    'total_sell_transactions': sell_transactions.count(),
                    'recent_transactions': recent_transactions_data,
                }
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Failed to fetch gold holdings: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
