from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Transaction, GoldHolding, PriceHistory, Deposit, PriceAlert


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'phone_number', 'date_of_birth')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'phone_number', 'date_of_birth', 'balance', 'is_verified',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'email', 'balance', 'is_verified', 'created_at', 'updated_at')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'date_of_birth')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'balance')
        read_only_fields = ('id', 'username', 'email', 'balance')


class TransactionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'user', 'user_email', 'transaction_type', 'gold_weight',
                  'gold_price_per_gram', 'total_amount', 'status', 'transaction_date',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'user_email', 'total_amount', 'transaction_date',
                           'created_at', 'updated_at')


class GoldHoldingSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    current_value = serializers.SerializerMethodField()
    profit_loss = serializers.SerializerMethodField()
    profit_loss_percent = serializers.SerializerMethodField()

    class Meta:
        model = GoldHolding
        fields = ('id', 'user', 'user_email', 'amount', 'avg_price',
                  'total_value', 'current_value', 'profit_loss', 'profit_loss_percent',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'user_email', 'total_value',
                           'current_value', 'profit_loss', 'profit_loss_percent',
                           'created_at', 'updated_at')

    def get_current_value(self, obj):
        try:
            latest_price = PriceHistory.objects.order_by('-timestamp').first()
            if latest_price:
                return float(obj.amount * latest_price.price_per_gram)
            return float(obj.total_value)
        except Exception:
            return float(obj.total_value)

    def get_profit_loss(self, obj):
        current_value = self.get_current_value(obj)
        return float(current_value - float(obj.total_value))

    def get_profit_loss_percent(self, obj):
        current_value = self.get_current_value(obj)
        total_value_float = float(obj.total_value)
        if total_value_float > 0:
            return float(((current_value - total_value_float) / total_value_float) * 100)
        return 0.0


class GoldHoldingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldHolding
        fields = ('amount', 'avg_price')


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ('id', 'price_per_gram', 'price_per_baht', 'currency',
                  'timestamp', 'source', 'notes')
        read_only_fields = ('id', 'timestamp')


class PriceHistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ('price_per_gram', 'price_per_baht', 'currency', 'source', 'notes')


class DepositSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Deposit
        fields = ('id', 'user', 'user_email', 'amount', 'status',
                  'reference', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user_email', 'status',
                           'reference', 'created_at', 'updated_at')


class DepositCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('amount',)


class DepositCompleteSerializer(serializers.Serializer):
    deposit_id = serializers.IntegerField()
    reference = serializers.CharField()


class DepositUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('status',)


class PriceAlertSerializer(serializers.ModelSerializer):
    """
    Serializer for PriceAlert model with user email.
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = PriceAlert
        fields = ('id', 'user', 'user_id', 'user_email', 'target_price', 'condition',
                  'is_active', 'is_triggered', 'triggered_at', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user_id', 'user_email', 'is_triggered',
                           'triggered_at', 'created_at', 'updated_at')


class PriceAlertCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new PriceAlert.
    """
    class Meta:
        model = PriceAlert
        fields = ('target_price', 'condition')

    def validate_target_price(self, value):
        """Ensure target price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Target price must be greater than zero.")
        return value


class PriceAlertUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing PriceAlert.
    """
    class Meta:
        model = PriceAlert
        fields = ('target_price', 'condition', 'is_active')
