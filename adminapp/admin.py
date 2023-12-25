from django.contrib import admin
from .models import AdminConfig,GeneralSettings,Logos,Payments,UserAgreements
# Register your models here.

admin.site.register(AdminConfig)
admin.site.register(GeneralSettings)
admin.site.register(Logos)
admin.site.register(Payments)
admin.site.register(UserAgreements)