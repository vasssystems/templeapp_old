# webapp/adminapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from utils.common.custom_response import CustomResponseMixin
from utils.rbac.permissions import IsPortalManager, IsGetOrIsAdmin
from django.db import models as dmodels
from django.db.models import Q
from .serializers import *
from .models import UserAgreements, AdminConfig, Logos, GeneralSettings, Payments
from utils.common.general_functions import err_msg
import logging

logger = logging.getLogger(__name__)


class AgreementsListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = UserAgreements.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = UserAgreementSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code', 'uuid']  # Add fields to search for

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


class AgreementsDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = UserAgreements.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = UserAgreementSerializer
    permission_classes = [IsPortalManager, ]
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


class AdminConfigListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = AdminConfig.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = AdminConfigSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code', 'uuid']  # Add fields to search for

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


class AdminConfigDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = AdminConfig.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = AdminConfigSerializer
    permission_classes = [IsPortalManager, ]
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


class LogosListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = Logos.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = LogosSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code', 'uuid']  # Add fields to search for

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


class LogosDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = Logos.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = LogosSerializer
    permission_classes = [IsPortalManager, ]
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


class PaymentsListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = Payments.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = PaymentsSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code', 'uuid']  # Add fields to search for

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


class PaymentsDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):

    queryset = Payments.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = PaymentsSerializer
    permission_classes = [IsPortalManager, ]
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


class GeneralSettingsListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = GeneralSettings.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = GeneralSettingsSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code', 'uuid']  # Add fields to search for

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


class GeneralSettingsDetailsAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = GeneralSettings.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = GeneralSettingsSerializer
    permission_classes = [IsPortalManager, ]
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