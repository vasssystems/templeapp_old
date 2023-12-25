# webapp/features/views.py
from django.db.models import Q
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from utils.rbac.permissions import IsPortalManager, IsGetOrIsAdmin
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from utils.common.custom_response import CustomResponseMixin
from rest_framework.filters import SearchFilter
from utils.common.general_functions import err_msg
import logging

from .models import (
    Departments, Clubs, Batch, Faq, NoticeBoard)

from .serializers import (
    DepartmentSerializer, ClubsSerializer,
    BatchSerializer, FaqSerializer, NoticeBoardSerializer)

logger = logging.getLogger(__name__)


class DepartmentListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = Departments.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = DepartmentSerializer
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


class DepartmentRetrieveUpdateDestroyAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = Departments.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = DepartmentSerializer
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


class ClubsListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = Clubs.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ClubsSerializer
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


class ClubsRetrieveUpdateDestroyAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = Clubs.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ClubsSerializer
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


class BatchListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = Batch.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = BatchSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'batch_no', 'uuid']
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
                res_data = {'count': self.paginator.count, 'next': self.paginator.get_next_link(),
                            'previous': self.paginator.get_previous_link(), 'results': serializer.data}
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


class BatchRetrieveUpdateDestroyAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = BatchSerializer
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


class FaqListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = Faq.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = FaqSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['question', 'tags', 'uuid']  # Adjust fields to search for

    permission_classes = [IsGetOrIsAdmin]  # Update with actual permissions

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


class FaqRetrieveUpdateDestroyAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = Faq.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = FaqSerializer
    permission_classes = [IsPortalManager, ]  # Update with actual permissions
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


class NoticeBoardListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = NoticeBoard.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = NoticeBoardSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'message', 'uuid']  # Fields to search for

    permission_classes = [IsGetOrIsAdmin]  # Adjust with actual permissions

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
            return self.server_error_response("Something went wrong !", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))


class NoticeBoardRetrieveUpdateDestroyAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = NoticeBoard.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = NoticeBoardSerializer
    permission_classes = [IsPortalManager, ]  # Adjust with actual permissions
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.success_response("Updated successfully", data=serializer.data)
            return self.bad_request_response("Invalid data provided", data=serializer.errors)
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return self.no_content_response("Deleted successfully", {"uuid": instance.uuid})
        except Exception as e:
            return self.server_error_response("Something went wrong !", err_msg(e))
