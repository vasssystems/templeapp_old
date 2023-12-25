# webapp/adminapp/models.py
import time
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from utils.common.generators import generate_random_code
from utils.common.generators import ChoiceMenu

User = get_user_model()


def get_user_id(instance):
    try:
        if instance.created_by:
            user_id = instance.created_by.id if instance.created_by.id else 0
        else:
            user_id = 0
        return user_id
    except:
        return 0


def admin_file_upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Schema/uploads/faq_uploads/user_<id>/<filename>
    schema_name = "public"
    user_id = get_user_id(instance)
    path = f"{schema_name}/uploads/logo_uploads/user_{user_id}/{filename}"
    return path


def default_blank_fields():
    fields = []
    return fields


# Create your models here.
class Payments(models.Model):
    transaction_id = models.CharField(max_length=50)
    package_id = models.CharField(null=True, max_length=80, choices=ChoiceMenu.PACKAGES)
    code = models.CharField(null=True, blank=True, unique=True, max_length=80)
    created_on = models.DateField(auto_now_add=True, null=True)
    payment_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    amount = models.PositiveIntegerField(blank=True, default=0)
    description = models.TextField(null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  # Common UUID field for all models with autogenerate
    status = models.BooleanField(default=True)  # Common Status field for check active or disabled status of object
    is_deleted = models.BooleanField(default=False)  # Soft delete field
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)  # Store created user UUID
    updated_by = models.CharField(max_length=40, null=True, blank=True)  # Store Updated user UUID

    def __str__(self):
        return f"{self.code}"


class GeneralSettings(models.Model):
    id_no = models.IntegerField(null=True, unique=True, default=1)
    title = models.CharField(max_length=200, null=True, blank=True, unique=True)
    tags = models.CharField(max_length=20, null=True, unique=True, blank=True)
    input_version = models.CharField(max_length=20, null=True, unique=True, blank=True, choices=ChoiceMenu.VERSION)
    report_version = models.CharField(max_length=20, null=True, unique=True, blank=True, choices=ChoiceMenu.VERSION)
    description = models.TextField(null=True, blank=True)
    allow_signup = models.BooleanField(default=True, blank=True)
    allow_data_entry = models.BooleanField(default=True, blank=True)
    allow_change_roles = models.BooleanField(default=True, blank=True)
    enable_otp = models.BooleanField(default=False, blank=True)
    enable_captha = models.BooleanField(default=False, blank=True)
    enable_https = models.BooleanField(default=False, blank=True)
    other = models.BooleanField(default=True, blank=True)
    classic_ui = models.BooleanField(default=False, blank=True)
    is_app_active = models.BooleanField(null=True, default=True)  # Enabled by NAAC Admin
    admin_email = models.EmailField(null=True, blank=True)
    admin_phone = models.CharField(null=True, blank=True, max_length=25)
    admin_url = models.URLField(null=True, blank=True)
    admin_address = models.CharField(null=True, blank=True, max_length=225)
    jdoc = models.JSONField(default=default_blank_fields, null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  # Common UUID field for all models with autogenerate
    status = models.BooleanField(default=True)  # Common Status field for check active or disabled status of object
    is_deleted = models.BooleanField(default=False)  # Soft delete field
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)  # Store created user UUID
    updated_by = models.CharField(max_length=40, null=True, blank=True)  # Store Updated user UUID

    def __str__(self):
        return str(self.id_no)

    def save(self, *args, **kwargs):
        if self.status:  # If status is True for the current instance being saved
            # Check if any other object with status=True exists
            existing_active_object = GeneralSettings.objects.filter(status=True).exclude(pk=self.pk)
            if existing_active_object.exists():  # If there's another active object
                existing_active_object.update(status=False)  # Set its status to False

        super(GeneralSettings, self).save(*args, **kwargs)


# Special Model, Only Technical admin or Service Provider can Update
class AdminConfig(models.Model):
    code = models.CharField(null=True, blank=True, unique=True, max_length=80)
    package = models.CharField(null=True, max_length=80, choices=ChoiceMenu.PACKAGES)
    portal_type = models.CharField(null=True, unique=True, max_length=80, choices=ChoiceMenu.PORTAL_TYPE)
    user_limit = models.IntegerField(null=True, blank=True)
    criterion_limit = models.IntegerField(null=True, blank=True)
    data_limit = models.IntegerField(null=True, blank=True)
    file_size_limit = models.IntegerField(null=True, blank=True)
    other_limit = models.IntegerField(null=True, blank=True)
    admin_pin = models.IntegerField(null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  # Common UUID field for all models with autogenerate
    status = models.BooleanField(default=True)  # Common Status field for check active or disabled status of object
    is_deleted = models.BooleanField(default=False)  # Soft delete field
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)  # Store created user UUID
    updated_by = models.CharField(max_length=40, null=True, blank=True)  # Store Updated user UUID

    def __str__(self):
        return f"{self.code}"

    def save(self, *args, **kwargs):
        if self.status:  # If status is True for the current instance being saved
            # Check if any other object with status=True exists
            existing_active_object = AdminConfig.objects.filter(status=True).exclude(pk=self.pk)
            if existing_active_object.exists():  # If there's another active object
                existing_active_object.update(status=False)  # Set its status to False

        super(AdminConfig, self).save(*args, **kwargs)


class Logos(models.Model):
    code = models.CharField(null=True, blank=True, unique=True, max_length=80)
    id_no = models.IntegerField(null=True, unique=True)
    logo = models.ImageField(upload_to=admin_file_upload_directory_path, null=True, blank=True)
    fav_icon = models.ImageField(upload_to=admin_file_upload_directory_path, null=True, blank=True)
    image = models.ImageField(upload_to=admin_file_upload_directory_path, null=True, blank=True)
    files = models.FileField(upload_to=admin_file_upload_directory_path, null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  # Common UUID field for all models with autogenerate
    status = models.BooleanField(default=True)  # Common Status field for check active or disabled status of object
    is_deleted = models.BooleanField(default=False)  # Soft delete field
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)  # Store created user UUID
    updated_by = models.CharField(max_length=40, null=True, blank=True)  # Store Updated user UUID

    def __str__(self):
        return str(self.id_no)


class UserAgreements(models.Model):
    code = models.CharField(null=True, blank=True, unique=True, max_length=80)
    id_no = models.IntegerField(null=True, unique=True)
    title = models.CharField(max_length=20, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True, choices=ChoiceMenu.AGREEMENT, default="TOS")
    description = models.TextField(null=True, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  # Common UUID field for all models with autogenerate
    status = models.BooleanField(default=True)  # Common Status field for check active or disabled status of object
    is_deleted = models.BooleanField(default=False)  # Soft delete field
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)  # Store created user UUID
    updated_by = models.CharField(max_length=40, null=True, blank=True)  # Store Updated user UUID

    def __str__(self):
        return str(self.id_no)


@receiver(pre_save, sender=Payments)
def payments_code_gen(sender, instance, **kwargs):
    try:
        if not instance.code:
            instance.code = generate_random_code()
    except:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())


@receiver(pre_save, sender=AdminConfig)
def admin_config_code_gen(sender, instance, **kwargs):
    try:
        if not instance.code:
            instance.code = generate_random_code()
    except:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())


@receiver(pre_save, sender=UserAgreements)
def agreement_code_gen(sender, instance, **kwargs):
    try:
        if not instance.code:
            instance.code = generate_random_code()
    except:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())


@receiver(pre_save, sender=Logos)
def logos_code_gen(sender, instance, **kwargs):
    try:
        if not instance.code:
            instance.code = generate_random_code()
    except:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())
