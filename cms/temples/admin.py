# webapp/cms/temples/admin.py
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    TempleGallery, ServiceGallery, Poojas, TempleData,
    ServiceData, Festivals, Blog, Bookings
)


# Temple Master
class TempleResource(resources.ModelResource):
    class Meta:
        model = TempleData


class TempleAdmin(ImportExportModelAdmin):
    readonly_fields = ('uuid',)
    resource_class = TempleResource


# Service Details
class ServiceResource(resources.ModelResource):
    class Meta:
        model = ServiceData


class ServiceAdmin(ImportExportModelAdmin):
    readonly_fields = ('uuid',)
    resource_class = ServiceResource


# Select Box Fields Details
class PoojaResource(resources.ModelResource):
    class Meta:
        model = Poojas


class PoojaAdmin(ImportExportModelAdmin):
    readonly_fields = ('uuid',)
    resource_class = PoojaResource


# File fields Details
class FestivalResource(resources.ModelResource):
    class Meta:
        model = Festivals


class FestivalAdmin(ImportExportModelAdmin):
    readonly_fields = ('uuid',)
    resource_class = FestivalResource


# CriterionFields Details
class BookingResource(resources.ModelResource):
    class Meta:
        model = Bookings


class BookingAdmin(ImportExportModelAdmin):
    readonly_fields = ('uuid',)
    resource_class = BookingResource


# CriterionFields Details
class BlogResource(resources.ModelResource):
    class Meta:
        model = Blog


class BlogAdmin(ImportExportModelAdmin):
    readonly_fields = ('uuid',)
    resource_class = BlogResource


# Register your models here.
admin.site.register(TempleData, TempleAdmin)
admin.site.register(ServiceData, ServiceAdmin)
admin.site.register(Poojas, PoojaAdmin)
admin.site.register(Festivals, FestivalAdmin)
admin.site.register(Bookings, BookingAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(TempleGallery)
admin.site.register(ServiceGallery)
