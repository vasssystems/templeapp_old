# webapp/features/admins.py
from django.contrib import admin
from .models import (
    Departments, Faq, NoticeBoard, Advertisements, Transaction)

# Register your models here.
admin.site.register(Departments)
admin.site.register(Advertisements)
admin.site.register(Transaction)
admin.site.register(Faq)
admin.site.register(NoticeBoard)