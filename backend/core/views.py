from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.db.models import Sum, F
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from decimal import Decimal, InvalidOperation
import uuid

from .models import User, GoldHolding, PriceHistory, Deposit, Transaction
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
    DepositSerializer,
    DepositCreateSerializer,
    DepositCompleteSerializer,
    TransactionSerializer,
)


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
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
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        return self.request.user


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshViewCustom(TokenRefreshView):
    pass


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_me_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ==================== Gold Holdings Views ====================

class GoldHoldingsListView(generics.ListCreateAPIView):
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoldHoldingCreateSerializer

    def get_queryset(self):
        return GoldHolding.objects.filter(user=self.request.user)


class GoldHoldingsSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        holdings = GoldHolding.objects.filter(user=request.user)
        total_amount = holdings.aggregate(total=Sum('amount'))['total'] or 0
        total_cost = holdings.aggregate(cost=Sum(F('amount') * F('avg_price')))['cost'] or 0
        latest_price = PriceHistory.objects.order_by('-timestamp').first()
        current_value = 0
        profit_loss = 0
        profit_loss_percent = 0
        if latest_price:
            current_value = total_amount * latest_price.price_per_gram
            if total_cost > 0:
                profit_loss = current_value - total_cost
                profit_loss_percent = (profit_loss / total_cost) * 100
        return Response({
            'total_amount': float(total_amount),
            'total_cost': float(total_cost),
            'current_value': float(current_value),
            'profit_loss': float(profit_loss),
            'profit_loss_percent': float(profit_loss_percent),
        })


# ==================== Price History Views ====================

class PriceHistoryListView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PriceHistorySerializer
    queryset = PriceHistory.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Only admins can create price history.")
        serializer.save()


class PriceHistoryDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PriceHistorySerializer
    queryset = PriceHistory.objects.all()


class CurrentGoldPriceView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        latest_price = PriceHistory.objects.order_by('-timestamp').first()
        if not latest_price:
            return Response({'error': 'No price data available'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PriceHistorySerializer(latest_price).data)


# ==================== Trading Views ====================

class TradeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        trade_type = request.data.get('type')
        amount = Decimal(str(request.data.get('amount', 0)))
        if amount <= 0:
            return Response({'error': 'จำนวนทองต้องมากกว่า 0'}, status=status.HTTP_400_BAD_REQUEST)
        latest_price = PriceHistory.objects.order_by('-timestamp').first()
        if not latest_price:
            return Response({'error': 'ไม่มีข้อมูลราคาทองในขณะนี้'}, status=status.HTTP_400_BAD_REQUEST)
        price_per_gram = latest_price.price_per_gram
        total_cost = amount * price_per_gram
        user = request.user
        with transaction.atomic():
            if trade_type == 'BUY':
                if user.balance < total_cost:
                    return Response({'error': 'ยอดเงินไม่เพียงพอ'}, status=status.HTTP_400_BAD_REQUEST)
                user.balance -= total_cost
                user.save()
                holding, _ = GoldHolding.objects.get_or_create(user=user, defaults={'amount': Decimal('0'), 'avg_price': Decimal('0')})
                new_total_amount = holding.amount + amount
                new_avg_price = ((holding.amount * holding.avg_price) + (amount * price_per_gram)) / new_total_amount
                holding.amount = new_total_amount
                holding.avg_price = new_avg_price
                holding.save()
            elif trade_type == 'SELL':
                try:
                    holding = GoldHolding.objects.get(user=user)
                    if holding.amount < amount:
                        return Response({'error': 'จำนวนทองไม่เพียงพอ'}, status=status.HTTP_400_BAD_REQUEST)
                except GoldHolding.DoesNotExist:
                    return Response({'error': 'คุณยังไม่มีทองในครอบครอง'}, status=status.HTTP_400_BAD_REQUEST)
                user.balance += total_cost
                user.save()
                holding.amount -= amount
                holding.save()
            else:
                return Response({'error': 'ประเภทธุรกรรมไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)
            trans = Transaction.objects.create(
                user=user, transaction_type=trade_type, gold_weight=amount,
                gold_price_per_gram=price_per_gram, total_amount=total_cost, status='COMPLETED'
            )
        return Response({
            'message': 'สำเร็จ', 
            'transaction': {
                'type': trans.transaction_type,
                'amount': float(trans.gold_weight),
                'gold_price_per_gram': float(trans.gold_price_per_gram),
                'total_amount': float(trans.total_amount),
                'status': trans.status,
                'transaction_date': trans.transaction_date.isoformat()
            }
        })


class TransactionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-transaction_date')


# ==================== Deposit Views ====================

class DepositListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepositSerializer

    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DepositCreateSerializer
        return DepositSerializer

    def perform_create(self, serializer):
        # Auto-generate reference
        reference = f"MOCK-{uuid.uuid4().hex[:12].upper()}"
        # For mock purposes, auto-complete the deposit
        serializer.save(user=self.request.user, reference=reference, status='COMPLETED')
        
        # Update user balance immediately for mock deposit
        user = self.request.user
        # Ensure balance is Decimal
        current_balance = Decimal(str(user.balance)) if not isinstance(user.balance, Decimal) else user.balance
        user.balance = current_balance + serializer.validated_data['amount']
        user.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Use full serializer for response
        response_serializer = DepositSerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DepositCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DepositCreateSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            reference = f"MOCK-{uuid.uuid4().hex[:12].upper()}"
            deposit = Deposit.objects.create(user=request.user, amount=amount, status='PENDING', reference=reference)
            return Response({'message': 'Deposit request created', 'deposit': DepositSerializer(deposit).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DepositCompleteSerializer(data=request.data)
        if serializer.is_valid():
            deposit_id = serializer.validated_data['deposit_id']
            reference = serializer.validated_data['reference']
            try:
                deposit = Deposit.objects.get(id=deposit_id, user=request.user)
                if deposit.reference != reference:
                    return Response({'error': 'Invalid reference'}, status=status.HTTP_400_BAD_REQUEST)
                if deposit.status == 'COMPLETED':
                    return Response({'message': 'Already completed'})
                deposit.complete_deposit()
                return Response({'message': 'Deposit completed', 'new_balance': float(request.user.balance)})
            except Deposit.DoesNotExist:
                return Response({'error': 'Deposit not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MockDepositProcessView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method', 'BANK_TRANSFER')
        notes = request.data.get('notes', '')
        
        # Validate amount
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            amount_decimal = Decimal(str(amount))
            if amount_decimal <= 0:
                return Response({'error': 'Amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Mock limit: 1,000,000
            if amount_decimal > Decimal('1000000.00'):
                return Response({'error': 'Amount exceeds mock limit of 1,000,000'}, status=status.HTTP_400_BAD_REQUEST)
                
        except (ValueError, TypeError, InvalidOperation):
            return Response({'error': 'Invalid amount format'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # Create completed deposit
            reference = f"MOCK-{uuid.uuid4().hex[:12].upper()}"
            deposit = Deposit.objects.create(
                user=request.user,
                amount=amount_decimal,
                status='COMPLETED',
                reference=reference
            )
            
            # Update user balance - refresh to get latest balance
            from core.models import User
            user = User.objects.select_for_update().get(pk=request.user.pk)
            user.balance = Decimal(str(user.balance)) + amount_decimal
            user.save()
            
            return Response({
                'message': 'Mock deposit processed successfully',
                'deposit': {
                    'id': deposit.id,
                    'amount': float(deposit.amount),
                    'status': deposit.status,
                    'reference': deposit.reference,
                    'created_at': deposit.created_at.isoformat(),
                    'updated_at': deposit.updated_at.isoformat()
                }
            }, status=status.HTTP_201_CREATED)


class DepositDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepositSerializer

    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)


class WalletBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'email': request.user.email,
            'balance': float(request.user.balance),
            'updated_at': request.user.updated_at.isoformat()
        })
