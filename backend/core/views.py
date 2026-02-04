from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import User, GoldPrice, Transaction, Wallet
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    GoldPriceSerializer, TransactionSerializer, WalletSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['email', 'username']
    filterset_fields = ['is_verified']
    ordering_fields = ['created_at', 'email']

    def get_permissions(self):
        """Custom permission for registration action."""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """Use different serializer for registration."""
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class GoldPriceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for GoldPrice model (read-only)."""
    queryset = GoldPrice.objects.all()
    serializer_class = GoldPriceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['currency']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get the latest gold price."""
        latest_price = self.queryset.first()
        serializer = self.get_serializer(latest_price)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for Transaction model."""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['transaction_type', 'status']
    ordering_fields = ['transaction_date', 'created_at']
    ordering = ['-transaction_date']

    def get_queryset(self):
        """Only return transactions for the current user."""
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user and calculate total amount."""
        gold_weight = serializer.validated_data['gold_weight']
        gold_price_per_gram = serializer.validated_data['gold_price_per_gram']
        total_amount = gold_weight * gold_price_per_gram

        serializer.save(
            user=self.request.user,
            total_amount=total_amount
        )


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Wallet model (read-only)."""
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return wallet for the current user."""
        return Wallet.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_wallet(self, request):
        """Get current user's wallet."""
        wallet = Wallet.objects.get(user=request.user)
        serializer = self.get_serializer(wallet)
        return Response(serializer.data)
