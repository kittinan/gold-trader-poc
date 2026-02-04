from rest_framework import serializers
from .models import User, GoldPrice, Transaction, Wallet


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'phone_number', 'date_of_birth',
                  'is_verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'phone_number']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # Create wallet for new user
        Wallet.objects.create(user=user)
        return user


class GoldPriceSerializer(serializers.ModelSerializer):
    """Serializer for GoldPrice model."""

    class Meta:
        model = GoldPrice
        fields = ['id', 'price_per_gram', 'price_per_baht', 'currency',
                  'timestamp', 'source']
        read_only_fields = ['id', 'timestamp']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'transaction_type', 'gold_weight',
                  'gold_price_per_gram', 'total_amount', 'status',
                  'transaction_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'total_amount', 'created_at', 'updated_at']


class WalletSerializer(serializers.ModelSerializer):
    """Serializer for Wallet model."""

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'gold_holdings', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
