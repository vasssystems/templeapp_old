# webapp/features/general_functions.py
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def err_msg(error_data):
    try:
        formatted_errors = str(error_data)
        return formatted_errors
    except Exception as e:
        logger.error(e)
        return "Unknown Error"


def get_user_from_uuid(uuid_string):
    try:
        user = User.objects.get(uuid=str(uuid_string))
        return user
    except ObjectDoesNotExist:
        logger.info(f"User not found with UUID : {uuid_string}")
        return None
    except Exception as e:
        logger.error(f" Something went wrong :{e}")
        return None


def create_notification_by_model(user_uuid, title, message):
    try:
        content_type = ContentType.objects.get(app_label='user', model='Notifications')
        model_class = content_type.model_class()
        user = get_user_from_uuid(user_uuid)
        if model_class:
            notification_object = model_class.objects.create(
                user=user,
                title=title,
                message=message,
                created_by=str(user_uuid),
                created_at=timezone.now()
            )
            return notification_object
    except ContentType.DoesNotExist:
        logger.error(f" Model object not found")
        return None
    except Exception as e:
        logger.error(f" Something went wrong :{e}")
        return None
