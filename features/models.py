# webapp/features/models.py
import time
from django.db import models
from django.contrib.auth import get_user_model
from django.db import connection
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from utils.common.generators import generate_random_code, ChoiceMenu
from utils.base_model import CommonFields

User = get_user_model()


def default_blank_fields():
    fields = []
    return fields


def get_user_id(instance):
    try:
        if instance.created_by:
            user_id = instance.created_by.id if instance.created_by.id else 0
        else:
            user_id = 0
        return user_id
    except:
        return 0


def get_upload_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Schema/uploads/faq_uploads/user_<id>/<filename>
    user_id = get_user_id(instance)
    schema_name = connection.get_schema()
    path = f"{schema_name}/uploads/general/user_{user_id}/{filename}"
    return path


# Create your models here.
class Departments(CommonFields):
    name = models.CharField(max_length=30, unique=True)
    code = models.CharField(max_length=10, null=True, blank=True, unique=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    established_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Clubs(CommonFields):
    name = models.CharField(max_length=50, unique=True)
    user = models.ManyToManyField(User, related_name="club_user", blank=True)
    code = models.CharField(max_length=10, null=True, blank=True, unique=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    established_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Batch(CommonFields):
    name = models.CharField(max_length=12, null=True)
    batch_no = models.IntegerField(unique=True, blank=True, )
    established_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Faq(CommonFields):
    faq_no = models.IntegerField(null=True, unique=True)
    question = models.CharField(max_length=225, null=True, blank=True, unique=True)
    tags = models.CharField(max_length=220, null=True, unique=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    jdoc = models.JSONField(default=default_blank_fields, null=True, blank=True)
    image = models.ImageField(upload_to=get_upload_directory_path, null=True, blank=True)
    files = models.FileField(upload_to=get_upload_directory_path, null=True, blank=True)
    urls = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.faq_no)


class NoticeBoard(CommonFields):
    id_no = models.IntegerField(null=True, unique=True)
    title = models.CharField(max_length=220, null=True, unique=True, blank=True)
    message = models.TextField(null=True, blank=True)
    jdoc = models.JSONField(default=default_blank_fields, null=True, blank=True)
    files = models.FileField(upload_to=get_upload_directory_path, null=True, blank=True)
    urls = models.URLField(null=True, blank=True)
    link_to = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id_no)


class Advertisements(CommonFields):
    name = models.CharField(max_length=12, null=True)
    code = models.CharField(max_length=225, null=True, blank=True, unique=True)
    created_at = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    package = models.CharField(max_length=220, null=True, choices=ChoiceMenu.PACKAGES)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    amount = models.FloatField(default=0.00, blank=True)
    is_paid = models.BooleanField(default=False, blank=True)
    transaction_id = models.CharField(max_length=225, null=True, blank=True)
    payment_remarks = models.TextField(null=True, blank=True)
    ad_content = models.TextField(null=True, blank=True)
    ad_image = models.FileField(upload_to=get_upload_directory_path, null=True, blank=True)
    ad_url = models.URLField(null=True, blank=True)
    ad_remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Transaction(CommonFields):
    user_uuid = models.UUIDField(null=True, blank=True)
    user_ref = models.CharField(max_length=120, null=True)
    code = models.CharField(max_length=225, null=True, blank=True, unique=True)
    transaction_date = models.DateField(null=True, blank=True)
    txn_from = models.CharField(max_length=220, null=True, choices=ChoiceMenu.TXN_TYPES)
    txn_to = models.CharField(max_length=220, null=True, choices=ChoiceMenu.TXN_TYPES)
    amount = models.FloatField(default=0.00, blank=True)
    is_paid = models.BooleanField(default=False, blank=True)
    transaction_id = models.CharField(max_length=225, null=True, blank=True)
    payment_remarks = models.TextField(null=True, blank=True)
    account_number = models.CharField(max_length=120, null=True, blank=True)
    ifsc_code = models.CharField(max_length=40, null=True, blank=True)
    upi_id = models.CharField(max_length=180, null=True, blank=True)

    def __str__(self):
        return str(self.code)


# Generate code using Signals
@receiver(pre_save, sender=NoticeBoard)
def task_code_gen(sender, instance, **kwargs):
    try:
        if not instance.id_no:
            instance.code = generate_random_code()
    except Exception as ex:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())


# Generate code using Signals
@receiver(pre_save, sender=Transaction)
def txn_code_gen(sender, instance, **kwargs):
    try:
        if not instance.code:
            instance.code = generate_random_code()
    except Exception as ex:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())


# Generate code using Signals
@receiver(pre_save, sender=Advertisements)
def ads_code_gen(sender, instance, **kwargs):
    try:
        if not instance.code:
            instance.code = generate_random_code()
    except Exception as ex:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())
