# webapp/cms/temples/serializer.py
from rest_framework import serializers
from utils.views import get_api_objects
from .models import (TempleData, ServiceData, TempleGallery, ServiceGallery, Poojas, Bookings, Blog, Festivals)


class TempleSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = TempleData
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class ServiceSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = ServiceData
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class PoojaSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = Poojas
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class FestivalSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = Festivals
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class BookingSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = Bookings
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class BlogSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class TempleGallerySerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = TempleGallery
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


class ServiceGallerySerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(max_length=40, read_only=True)
    updated_by = serializers.CharField(max_length=40, read_only=True)

    class Meta:
        model = ServiceGallery
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = str(self.context['request'].user.uuid)
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().create(validated_data)

    def perform_update(self, instance, validated_data):
        validated_data['updated_by'] = str(self.context['request'].user.uuid)
        return super().perform_update(instance, validated_data)


# Detailed serializer for Supporting Temple detailed view
class GetPoojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poojas
        fields = ('id', 'name', 'code', 'remarks', 'description', 'amount', 'booking_available', 'uuid', 'status')


class GetFestivalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festivals
        fields = (
            'id', 'name', 'sub_title', 'highlights', 'description', 'start_date', 'end_date',
            'location', 'thumbnail', 'image', 'uuid', 'status')


class GetServiceGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGallery
        fields = ('id', 'uuid', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5',
                  'image_6', 'image_7', 'image_8', 'name', 'created_at', 'created_by')


class GetTempleGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = TempleGallery
        fields = ('id', 'uuid', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5',
                  'image_6', 'image_7', 'image_8', 'name', 'created_at', 'created_by')


# Custom Serializer to Show Temple with Pooja and festival details
class GetTempleDetailedSerializer(serializers.ModelSerializer):
    pooja_details = serializers.SerializerMethodField()
    festivals = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = TempleData
        fields = ("id", "created_by", "updated_by", "uuid", "status",
                  "created_at", "updated_at", "name", "subtitle", "description",
                  "image", "deity", "deity_list", "landmark", "location", "town",
                  "district", "zipcode", "state", "country", "latitude", "longitude",
                  "map_url", "telephone", "mobile", "email", "website", "slug",
                  "embedded_url", "time_slot_1", "time_slot_2", "time_slot_3",
                  "acc_number", "ifsc_code", "bank_name", "account_name", "upi_id",
                  "upi_qr", "story", "gallery", "pooja_details", "festivals", "social_media")

    def get_festivals(self, tmp):
        festival_obj = Festivals.objects.filter(is_deleted=False, status=True, temple_uuid=str(tmp.uuid)).order_by("id")
        return GetFestivalsSerializer(festival_obj, many=True).data

    def get_pooja_details(self, tmp):
        pooja_obj = Poojas.objects.filter(is_deleted=False, status=True, temple_uuid=tmp.uuid).order_by("id")
        return GetPoojaSerializer(pooja_obj, many=True).data

    def get_gallery(self, tmp):
        gallery_obj = TempleGallery.objects.filter(is_deleted=False, status=True, temple_uuid=tmp.uuid).order_by("id")
        return GetTempleGallerySerializer(gallery_obj, many=True).data


# Custom Serializer to Show Temple with Pooja and festival details
class GetServiceDetailedSerializer(serializers.ModelSerializer):
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = ServiceData
        fields = ("id", "created_by", "updated_by", "uuid", "status",
                  "created_at", "updated_at", "name", "subtitle", "description",
                  "image", "category", "landmark", "location", "town",
                  "district", "zipcode", "state", "country", "latitude", "longitude",
                  "map_url", "telephone", "mobile", "email", "website", "slug",
                  "embedded_url", "time_slot_1", "time_slot_2", "time_slot_3",
                  "acc_number", "ifsc_code", "bank_name", "account_name", "upi_id",
                  "upi_qr", "story", "gallery", "enable_booking", "social_media")

    def get_gallery(self, obj):
        gallery_obj = ServiceGallery.objects.filter(is_deleted=False, status=True, service_uuid=obj.uuid).order_by("id")
        return GetServiceGallerySerializer(gallery_obj, many=True).data
