from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Transaction


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
