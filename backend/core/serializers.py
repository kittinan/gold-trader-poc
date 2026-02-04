from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Transaction, GoldHolding, PriceHistory


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
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
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile (read and update).
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'phone_number', 'date_of_birth', 'balance', 'is_verified',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'email', 'balance', 'is_verified', 'created_at', 'updated_at')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for partial user profile updates.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'date_of_birth')


class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer for public display.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id', 'username', 'email')


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for transaction display.
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'user', 'user_email', 'transaction_type', 'gold_weight',
                  'gold_price_per_gram', 'total_amount', 'status', 'transaction_date',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'user_email', 'total_amount', 'transaction_date',
                           'created_at', 'updated_at')


class GoldHoldingSerializer(serializers.ModelSerializer):
    """
    Serializer for user gold holdings.
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)
    current_value = serializers.SerializerMethodField()
    profit_loss = serializers.SerializerMethodField()
    profit_loss_percent = serializers.SerializerMethodField()

    class Meta:
        model = GoldHolding
        fields = ('id', 'user', 'user_email', 'amount', 'avg_price',
                  'total_value', 'current_value', 'profit_loss', 'profit_loss_percent',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'user_email', 'total_value',
                           'current_value', 'profit_loss', 'profit_loss_percent',
                           'created_at', 'updated_at')

    def get_current_value(self, obj):
        """
        Calculate current value based on latest gold price.
        """
        try:
            latest_price = PriceHistory.objects.order_by('-timestamp').first()
            if latest_price:
                return float(obj.amount * latest_price.price_per_gram)
            return float(obj.total_value)
        except Exception:
            return float(obj.total_value)

    def get_profit_loss(self, obj):
        """
        Calculate profit/loss amount.
        """
        current_value = self.get_current_value(obj)
        return float(current_value - obj.total_value)

    def get_profit_loss_percent(self, obj):
        """
        Calculate profit/loss percentage.
        """
        current_value = self.get_current_value(obj)
        if obj.total_value > 0:
            return float(((current_value - obj.total_value) / obj.total_value) * 100)
        return 0.0


class GoldHoldingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating gold holdings.
    """
    class Meta:
        model = GoldHolding
        fields = ('amount', 'avg_price')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_avg_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Average price must be greater than zero.")
        return value


class PriceHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for price history records.
    """
    class Meta:
        model = PriceHistory
        fields = ('id', 'price_per_gram', 'price_per_baht', 'currency',
                  'timestamp', 'source', 'notes')
        read_only_fields = ('id', 'timestamp')


class PriceHistoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new price history records.
    """
    class Meta:
        model = PriceHistory
        fields = ('price_per_gram', 'price_per_baht', 'currency', 'source', 'notes')

    def validate_price_per_gram(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price per gram must be greater than zero.")
        return value

    def validate_price_per_baht(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price per baht must be greater than zero.")
        return value
