# webapp/adminapp/serializers.py
from rest_framework import serializers
from .models import UserAgreements, AdminConfig, Logos, GeneralSettings, Payments


class UserAgreementSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = UserAgreements
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class AdminConfigSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = AdminConfig
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class LogosSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = Logos
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class PaymentsSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = Payments
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class GeneralSettingsSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = GeneralSettings
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)
