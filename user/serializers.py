# webapp/user/serializers.py
from abc import ABC

from rest_framework import serializers
from .models import CustomUser, Notifications, Wallet
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from utils.common.generators import generate_random_code
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name', 'referred_by',
                  'mobile_number', 'department_id', 'designation', 'user_scope')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': False},
            'department_id': {'required': False},
            'mobile_number': {'required': True},
            'designation': {'required': False},
            'user_scope': {'required': False},
            'referred_by': {'required': False},
        }

    def create(self, validated_data):
        code = generate_random_code()  # Generate a random username
        username = code
        existing_obj = User.objects.filter(username=code).first()
        if existing_obj:
            username = generate_random_code()
        validated_data['username'] = username  # Assign the generated username to the data
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if 'new_password' in data and 'old_password' in data:
            if data['new_password'] == data['old_password']:
                raise serializers.ValidationError("New password should not be the same as the old password.")
        return data

    def update(self, instance, validated_data):
        if 'new_password' in validated_data:
            old_password = validated_data.get('old_password')
            if not instance.check_password(old_password):
                raise serializers.ValidationError("Incorrect old password.")

            new_password = validated_data.get('new_password')
            validate_password(new_password, user=instance)
            instance.set_password(new_password)
            instance.save()
        return instance


# Logged user can see his profile on dashboard.
class UserProfileSerializer(serializers.ModelSerializer):
    wallet_balance = serializers.SerializerMethodField()

    def get_wallet_balance(self, obj):
        return obj.wallet_balance()

    class Meta:
        model = CustomUser
        fields = ('id', 'uuid', 'first_name', 'last_name', 'email', 'username',
                  'department_id', 'designation', 'mobile_number',
                  'email_verified', 'mobile_verified', 'wallet_balance')


# Admin Can Update any User for CRUD Operations
class CustomUserSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'uuid', 'first_name', 'last_name', 'email', 'username',
                  'department_id', 'designation', 'mobile_number', 'referred_by',
                  'email_verified', 'mobile_verified', 'wallet_balance', 'status',
                  'created_at', 'created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'


# User Wallet for CRUD Operations
class WalletSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'uuid', 'user', 'points', 'remarks', 'from_user',
                  'txn_type', 'txn_id', 'code', 'created_at',
                  'created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        validated_data['user'] = self.context['request'].user
        validated_data['from_user'] = "SYSTEM"
        validated_data['txn_type'] = "DR"
        return super().create(validated_data)


