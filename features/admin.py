# webapp/features/admins.py
from django.contrib import admin
from .models import (
    Departments, Clubs,  Batch, Faq, NoticeBoard)

# Register your models here.
admin.site.register(Departments)
admin.site.register(Clubs)
admin.site.register(Batch)
admin.site.register(Faq)
admin.site.register(NoticeBoard)