# webapp/management/commands/clean_admin_logs.py
from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger("django")


class Command(BaseCommand):
    help = 'Cleans up the django_admin_log table by removing invalid user entries'

    def handle(self, *args, **options):
        invalid_logs = LogEntry.objects.exclude(user__in=User.objects.all())
        invalid_logs.delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleaned up django_admin_log table'))
