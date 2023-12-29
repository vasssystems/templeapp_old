# webapp/cms/temples
import time
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from ckeditor.fields import RichTextField
from utils.common.generators import generate_random_code, ChoiceMenu
from utils.common.general_functions import common_user_id
from utils.base_model import CommonFields
import logging

logger = logging.getLogger("django")

User = get_user_model()


def get_user_id(instance):
    try:
        if instance.created_by:
            user_id = instance.created_by if instance.created_by else "01"
        else:
            user_id = "01"
        return user_id
    except:
        return "01"


def temple_upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Schema/uploads/faq_uploads/user_<id>/<filename>
    schema_name = "public"
    user_id = get_user_id(instance)
    path = f"{schema_name}/temple_data/user_{user_id}/{instance.id}/{filename}"
    return path


def service_upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Schema/uploads/faq_uploads/user_<id>/<filename>
    schema_name = "public"
    user_id = get_user_id(instance)
    path = f"{schema_name}/service_data/user_{user_id}/{instance.id}/{filename}"
    return path


def default_blank_fields():
    fields = []
    return fields


# All data entered for criterion by users

"""
For Front End Developer :
"""


class TempleGallery(CommonFields):
    name = models.CharField(max_length=120, null=True)
    temple_uuid = models.UUIDField(null=True, blank=True)
    image_1 = models.ImageField(null=True, blank=True, upload_to=temple_upload_directory_path)
    image_2 = models.ImageField(null=True, blank=True, upload_to=temple_upload_directory_path)
    image_3 = models.ImageField(null=True, blank=True, upload_to=temple_upload_directory_path)
    image_4 = models.ImageField(null=True, blank=True, upload_to=temple_upload_directory_path)
    image_5 = models.ImageField(null=True, blank=True, upload_to=temple_upload_directory_path)
    image_6 = models.ImageField(null=True, blank=True, upload_to=temple_upload_directory_path)
    image_7 = models.ImageField(null=True, blank=True, upload_to=temple_upload_directory_path)
    image_8 = models.ImageField(null=True, blank=True, upload_to=temple_upload_directory_path)

    def __str__(self):
        return str(self.pk)


class ServiceGallery(CommonFields):
    name = models.CharField(max_length=120, null=True)
    service_uuid = models.UUIDField(null=True, blank=True)
    image_1 = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    image_2 = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    image_3 = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    image_4 = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    image_5 = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    image_6 = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    image_7 = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    image_8 = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)

    def __str__(self):
        return str(self.pk)


class Poojas(CommonFields):
    name = models.CharField(max_length=180, null=True)
    code = models.CharField(max_length=80, null=True, blank=True)  # Auto generated code
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(default=0.00, blank=True)
    remarks = models.CharField(max_length=220, null=True, blank=True)
    booking_available = models.BooleanField(default=False)
    temple_uuid = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class Festivals(CommonFields):
    name = models.CharField(max_length=180, null=True)
    sub_title = models.CharField(max_length=220, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    highlights = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=220, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    image = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    temple_uuid = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class Blog(CommonFields):
    title = models.CharField(max_length=120, null=True)
    slug = models.CharField(max_length=180, null=True, blank=True)  # Auto generated slug
    sub_title = models.CharField(max_length=220, null=True, blank=True)
    description = RichTextField(blank=True, null=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    image = models.ImageField(null=True, blank=True, upload_to=service_upload_directory_path)
    author = models.CharField(max_length=180, null=True, blank=True)
    reference = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class Bookings(CommonFields):
    name = models.CharField(max_length=120, null=True)
    code = models.CharField(max_length=180, null=True, blank=True)  # Auto generated code
    consulting_time = models.DateTimeField(null=True, blank=True)
    client_contact = models.CharField(max_length=15, null=True, blank=True)
    payment_done = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    service_uuid = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class TempleData(CommonFields):
    name = models.CharField(max_length=120, null=True)
    subtitle = models.CharField(max_length=225, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=temple_upload_directory_path, null=True, blank=True)
    deity = models.CharField(max_length=200, null=True, blank=True)
    deity_list = models.JSONField(default=default_blank_fields, null=True, blank=True)

    # Address details
    landmark = models.CharField(max_length=225, null=True, blank=True)
    location = models.CharField(max_length=225, null=True, blank=True)
    town = models.CharField(max_length=225, null=True, blank=True)
    district = models.CharField(max_length=225, null=True, blank=True)
    zipcode = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    map_url = models.URLField(null=True, blank=True)
    embedded_url = models.TextField(null=True, blank=True)
    # Timing & social media
    time_slot_1 = models.CharField(max_length=225, null=True, blank=True)
    time_slot_2 = models.CharField(max_length=225, null=True, blank=True)
    time_slot_3 = models.CharField(max_length=225, null=True, blank=True)
    social_media = models.JSONField(null=True, blank=True, default=default_blank_fields)

    # Contact details
    telephone = models.CharField(max_length=15, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    slug = models.CharField(null=True, blank=True, unique=True, max_length=220)

    # Payment and Donations
    acc_number = models.CharField(max_length=40, null=True, blank=True)
    ifsc_code = models.CharField(max_length=40, null=True, blank=True)
    bank_name = models.CharField(max_length=60, null=True, blank=True)
    account_name = models.CharField(max_length=140, null=True, blank=True)
    upi_id = models.CharField(max_length=80, null=True, blank=True)
    upi_qr = models.ImageField(upload_to=temple_upload_directory_path, null=True, blank=True)

    # Additional Information -  OneToOne Fields from Other Tables
    gallery = models.OneToOneField(TempleGallery, related_name='temple', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    story = models.CharField(max_length=180, null=True, blank=True)  # Link to Blog URL or Blog UUID

    def __str__(self):
        return str(self.pk)


class ServiceData(CommonFields):
    name = models.CharField(max_length=120, null=True)
    subtitle = models.CharField(max_length=225, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=temple_upload_directory_path, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)

    # Address details
    landmark = models.CharField(max_length=225, null=True, blank=True)
    location = models.CharField(max_length=225, null=True, blank=True)
    town = models.CharField(max_length=225, null=True, blank=True)
    district = models.CharField(max_length=225, null=True, blank=True)
    zipcode = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    map_url = models.URLField(null=True, blank=True)
    embedded_url = models.TextField(null=True, blank=True)

    # Timing & Social media
    time_slot_1 = models.CharField(max_length=225, null=True, blank=True)
    time_slot_2 = models.CharField(max_length=225, null=True, blank=True)
    time_slot_3 = models.CharField(max_length=225, null=True, blank=True)
    social_media = models.JSONField(null=True, blank=True, default=default_blank_fields)
    service_areas = models.JSONField(null=True, blank=True, default=default_blank_fields)

    # Contact details
    telephone = models.CharField(max_length=15, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    slug = models.CharField(null=True, blank=True, unique=True, max_length=220)

    # Payment and Donations
    acc_number = models.CharField(max_length=40, null=True, blank=True)
    ifsc_code = models.CharField(max_length=40, null=True, blank=True)
    bank_name = models.CharField(max_length=60, null=True, blank=True)
    account_name = models.CharField(max_length=140, null=True, blank=True)
    upi_id = models.CharField(max_length=80, null=True, blank=True)
    upi_qr = models.ImageField(upload_to=temple_upload_directory_path, null=True, blank=True)

    # Additional Information -  OneToOne Fields from Other Tables
    enable_booking = models.BooleanField(default=False)  # Enable Online Booking
    gallery = models.OneToOneField(ServiceGallery, on_delete=models.SET_NULL, null=True, blank=True)
    story = models.CharField(max_length=180, null=True, blank=True)  # Link to Blog URL or Blog UUID

    def __str__(self):
        return str(self.pk)


def generate_unique_slug(name, location):
    base_slug = slugify(f"{name} {location}")
    similar_slugs = TempleData.objects.filter(slug__startswith=base_slug).values_list('slug', flat=True)

    if not similar_slugs or base_slug not in similar_slugs:
        return base_slug  # If base slug is unique, return it

    # Generate a unique suffix for the slug
    suffix = 1
    while f"{base_slug}-{suffix}" in similar_slugs:
        suffix += 1

    return f"{base_slug}-{suffix}"  # Return a unique slug with a suffix


# Generate Random slug using temple name and location
@receiver(pre_save, sender=TempleData)
def temple_code_gen(sender, instance, **kwargs):
    try:
        if not instance.slug:
            instance.slug = generate_unique_slug(instance.name, instance.location)
        if not instance.created_by:
            instance.created_by = common_user_id

    except:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())
            instance.created_by = common_user_id


# Generate Random codes using Signals
@receiver(pre_save, sender=Poojas)
def pooja_code_gen(sender, instance, **kwargs):
    try:
        if not instance.code:
            instance.code = generate_random_code()
        if not instance.created_by:
            instance.created_by = common_user_id

    except:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())
            instance.created_by = common_user_id


@receiver(pre_save, sender=ServiceData)
def servcice_code_gen(sender, instance, **kwargs):
    try:
        if not instance.slug:
            instance.slug = generate_unique_slug(instance.name, instance.location)
        if not instance.created_by:
            instance.created_by = common_user_id

    except:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())
            instance.created_by = common_user_id
