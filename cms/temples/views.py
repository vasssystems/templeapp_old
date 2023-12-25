# webapp/cms/temples/views.py
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from utils.rbac.permissions import IsPortalManager, IsGetOrIsAdmin, IsDataOwner
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from utils.common.custom_response import CustomResponseMixin
from rest_framework.filters import SearchFilter
from utils.common.general_functions import err_msg
import logging

from .models import (TempleData, ServiceData, TempleGallery, ServiceGallery, Poojas, Festivals, Blog, Bookings)
from .serializers import (TempleGallerySerializer, ServiceGallerySerializer, TempleSerializer, ServiceSerializer,
                          PoojaSerializer, BookingSerializer,BlogSerializer, GetTempleDetailedSerializer,
                          FestivalSerializer, GetServiceDetailedSerializer)

logger = logging.getLogger(__name__)


# Temple CRUD APIs
class TempleListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = TempleData.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = TempleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'deity', 'uuid']  # Add fields to search for

    permission_classes = [IsGetOrIsAdmin]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            filter_field = self.request.query_params.get('filter_field')  # Get the dynamic filter field
            filter_value = self.request.query_params.get('filter_value')  # Get the filter value

            if filter_field and filter_value:
                filter_args = {filter_field: filter_value}
                queryset = queryset.filter(**filter_args)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res_data = {
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data
                }
                return self.success_response("Retrieved successfully", res_data)

            serializer = self.get_serializer(queryset, many=True)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))


class TempleDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = TempleData.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = TempleSerializer
    # For below permission class, AI Needs to generate a logic for Pass object as instance
    permission_classes = [IsDataOwner, IsAuthenticated]
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # serializer = self.serializer_class(instance)
            serializer = GetTempleDetailedSerializer(instance)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.success_response("Updated successfully", data=serializer.data)
            return self.bad_request_response("Invalid data provided", data=serializer.errors)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return self.no_content_response("Deleted successfully", {"uuid": instance.uuid})
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))


# Service CRUD API's
class ServiceListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = ServiceData.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ServiceSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'category', 'uuid']  # Add fields to search for

    permission_classes = [IsAuthenticated, IsDataOwner]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            filter_field = self.request.query_params.get('filter_field')  # Get the dynamic filter field
            filter_value = self.request.query_params.get('filter_value')  # Get the filter value

            if filter_field and filter_value:
                filter_args = {filter_field: filter_value}
                queryset = queryset.filter(**filter_args)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res_data = {
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data
                }
                return self.success_response("Retrieved successfully", res_data)

            serializer = self.get_serializer(queryset, many=True)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))


class ServiceDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = ServiceData.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ServiceSerializer
    # For below permission class, AI Needs to generate a logic for Pass object as instance
    permission_classes = [IsDataOwner, IsAuthenticated]
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # serializer = self.serializer_class(instance)
            serializer = GetServiceDetailedSerializer(instance)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.success_response("Updated successfully", data=serializer.data)
            return self.bad_request_response("Invalid data provided", data=serializer.errors)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return self.no_content_response("Deleted successfully", {"uuid": instance.uuid})
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))


# Temple Gallery API
class TempleGalleryListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = TempleGallery.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = TempleGallerySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'temple_uuid', 'uuid']  # Add fields to search for

    permission_classes = [IsAuthenticated, IsDataOwner]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            filter_field = self.request.query_params.get('filter_field')  # Get the dynamic filter field
            filter_value = self.request.query_params.get('filter_value')  # Get the filter value

            if filter_field and filter_value:
                filter_args = {filter_field: filter_value}
                queryset = queryset.filter(**filter_args)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res_data = {
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data
                }
                return self.success_response("Retrieved successfully", res_data)

            serializer = self.get_serializer(queryset, many=True)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))


class TempleGalleryDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = TempleGallery.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = TempleGallerySerializer
    # For below permission class, AI Needs to generate a logic for Pass object as instance
    permission_classes = [IsDataOwner, IsAuthenticated]
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.success_response("Updated successfully", data=serializer.data)
            return self.bad_request_response("Invalid data provided", data=serializer.errors)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return self.no_content_response("Deleted successfully", {"uuid": instance.uuid})
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))


# Service Gallery
class ServiceGalleryCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = ServiceGallery.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ServiceGallerySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'temple_uuid', 'uuid']  # Add fields to search for

    permission_classes = [IsAuthenticated, IsDataOwner]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            filter_field = self.request.query_params.get('filter_field')  # Get the dynamic filter field
            filter_value = self.request.query_params.get('filter_value')  # Get the filter value

            if filter_field and filter_value:
                filter_args = {filter_field: filter_value}
                queryset = queryset.filter(**filter_args)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res_data = {
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data
                }
                return self.success_response("Retrieved successfully", res_data)

            serializer = self.get_serializer(queryset, many=True)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))


class ServiceGalleryDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = ServiceGallery.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ServiceGallerySerializer
    # For below permission class, AI Needs to generate a logic for Pass object as instance
    permission_classes = [IsDataOwner, IsAuthenticated]
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.success_response("Updated successfully", data=serializer.data)
            return self.bad_request_response("Invalid data provided", data=serializer.errors)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return self.no_content_response("Deleted successfully", {"uuid": instance.uuid})
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))


# Pooja's API Views
class PoojaListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = Poojas.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = PoojaSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code', 'uuid']  # Add fields to search for

    permission_classes = [IsAuthenticated, IsDataOwner]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            filter_field = self.request.query_params.get('filter_field')  # Get the dynamic filter field
            filter_value = self.request.query_params.get('filter_value')  # Get the filter value

            if filter_field and filter_value:
                filter_args = {filter_field: filter_value}
                queryset = queryset.filter(**filter_args)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res_data = {
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data
                }
                return self.success_response("Retrieved successfully", res_data)

            serializer = self.get_serializer(queryset, many=True)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))


class PoojaDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = Poojas.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = PoojaSerializer
    # For below permission class, AI Needs to generate a logic for Pass object as instance
    permission_classes = [IsDataOwner, IsAuthenticated]
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.success_response("Updated successfully", data=serializer.data)
            return self.bad_request_response("Invalid data provided", data=serializer.errors)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return self.no_content_response("Deleted successfully", {"uuid": instance.uuid})
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))


# Festivals

class FestivalListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = Festivals.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = FestivalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'sub_title', 'uuid']  # Add fields to search for

    permission_classes = [IsAuthenticated, IsDataOwner]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            filter_field = self.request.query_params.get('filter_field')  # Get the dynamic filter field
            filter_value = self.request.query_params.get('filter_value')  # Get the filter value

            if filter_field and filter_value:
                filter_args = {filter_field: filter_value}
                queryset = queryset.filter(**filter_args)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res_data = {
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data
                }
                return self.success_response("Retrieved successfully", res_data)

            serializer = self.get_serializer(queryset, many=True)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))


class FestivalDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = Festivals.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = FestivalSerializer
    # For below permission class, AI Needs to generate a logic for Pass object as instance
    permission_classes = [IsDataOwner, IsAuthenticated]
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.success_response("Updated successfully", data=serializer.data)
            return self.bad_request_response("Invalid data provided", data=serializer.errors)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return self.no_content_response("Deleted successfully", {"uuid": instance.uuid})
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))


# Blog API Views

class BlogListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = Blog.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = BlogSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'category', 'uuid']  # Add fields to search for

    permission_classes = [IsAuthenticated, IsDataOwner]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            filter_field = self.request.query_params.get('filter_field')  # Get the dynamic filter field
            filter_value = self.request.query_params.get('filter_value')  # Get the filter value

            if filter_field and filter_value:
                filter_args = {filter_field: filter_value}
                queryset = queryset.filter(**filter_args)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res_data = {
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data
                }
                return self.success_response("Retrieved successfully", res_data)

            serializer = self.get_serializer(queryset, many=True)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))


class BlogDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = BlogSerializer
    # For below permission class, AI Needs to generate a logic for Pass object as instance
    permission_classes = [IsDataOwner, IsAuthenticated]
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.success_response("Updated successfully", data=serializer.data)
            return self.bad_request_response("Invalid data provided", data=serializer.errors)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return self.no_content_response("Deleted successfully", {"uuid": instance.uuid})
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))
