# webapp/features/serializers.py
from rest_framework import serializers
from .models import (
    Departments, Faq, NoticeBoard)


class DepartmentSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = Departments
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class NoticeBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBoard
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)
