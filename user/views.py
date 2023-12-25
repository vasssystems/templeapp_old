# webapp/user/views.py
import json
import logging
from rest_framework import generics, status, permissions
from django.db.models import Sum, Q
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.filters import SearchFilter
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from decouple import config
# User Forgot password reset
from rest_framework.response import Response
from utils.rbac.permissions import IsPortalManager
from utils.common.custom_response import CustomResponseMixin
from utils.common.general_functions import err_msg
from .serializers import RegisterSerializer, UserLoginSerializer, UserProfileSerializer, ChangePasswordSerializer, \
    CustomUserSerializer, NotificationSerializer, WalletSerializer
from .models import CustomUser, Notifications, Wallet

User = get_user_model()

logger = logging.getLogger("django")


# User registration view
class UserRegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.save()
                # Success part of the code # Single line dictionary for response with info logs
                res_data = {"success": True, "message": "Registration Successful, Please Login",
                            "data": UserProfileSerializer(user, context=self.get_serializer_context()).data, }
                logger.info(f"Successfully created user {user}")
                return Response(res_data, status=status.HTTP_201_CREATED)
            else:
                # Error handling part of the code # Single line dictionary for response with error logs
                err_data = str(serializer.errors)
                res_data = {"success": False, "message": "Something went wrong", "data": {"error": err_data}}
                logger.warning(err_data)
                return Response(res_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            # Exception handling part of the code # Single line dictionary for response with error logs
            logger.error(ex)
            res_data = {"success": False, "message": " Something went wrong !", "data": {"error": str(ex)}, }
            return Response(res_data, status=status.HTTP_400_BAD_REQUEST)


# User login view
class UserLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            data_ = request.data
            serializer = self.serializer_class(data=data_)
            serializer.is_valid(raise_exception=True)

            identifier = data_.get("identifier")
            password = data_.get("password")
            user_obj = User.objects.filter(
                Q(username=identifier) | Q(email=identifier) | Q(mobile_number=identifier)).first()
            if not user_obj:
                res_data = {"success": False, "message": "Login Failed !", "data": {"error": "User not Found"}, }
                return Response(res_data, status=status.HTTP_404_NOT_FOUND)

            username = user_obj.username
            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                update_last_login(None, user)

                user_data = {'id': user.id, 'uuid': str(user.uuid),
                             'username': user.username, 'scope': user.user_scope}
                res_data = {'success': True, 'message': 'User logged Successfully',
                            'data': user_data, 'token': str(refresh.access_token)}
                return Response(res_data, status=status.HTTP_200_OK)
            else:
                err_data = "Invalid Username or Password"
                res_data = {"success": False, "message": "Login Failed !", "data": {"error": err_data}, }
                return Response(res_data, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as ex:
            logger.error(ex)
            res_data = {"success": False, "message": "Something went wrong !", "data": {"error": str(ex)}, }
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Logout view for logged users
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                blacklisted = token.blacklist()
                res_data = {"success": True, "message": "Logout Successfully !", "data": {}}
                return Response(res_data, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"message": "Invalid token ", "success": False, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            res_data = {"success": False, "message": "Something went wrong !", "data": {"error": str(ex)}, }
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User change password
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.update(request.user, serializer.validated_data)
                return Response({'success': True, 'message': 'Password updated successfully', 'data': {}},
                                status=status.HTTP_200_OK)

            res_data = {"error": err_msg(serializer.errors)}
            return Response({'success': False, 'message': 'Failed to updated Password', 'data': res_data},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            res_data = {'success': False, "message": 'Some thing went wrong', 'data': err_msg(ex)}
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object())
            return Response({'success': True, 'message': 'User details fetched successfully', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(ex)
            res_data = {'success': False, "message": 'Some thing went wrong', 'data': err_msg(ex)}
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'success': True, 'message': 'User details updated successfully', 'data': serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            logger.error(ex)
            res_data = {'success': False, "message": 'Some thing went wrong', 'data': err_msg(ex)}
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.is_deleted = True
            user.save()
            return Response({'success': True, 'message': 'User deleted successfully', 'data': {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.error(ex)
            res_data = {'success': False, "message": 'Some thing went wrong', 'data': err_msg(ex)}
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User wallet
class WalletListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    serializer_class = WalletSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['user', 'code', 'uuid']  # Add fields to search for

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Wallet.objects.filter(user=user, is_deleted=False).order_by('-id')
        return queryset

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
                    'user_balance': request.user.wallet_balance(),
                    'results': serializer.data
                }
                return self.success_response("Retrieved successfully", res_data)

            serializer = self.get_serializer(queryset, many=True)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            # Check if the user has enough balance for withdrawal
            points = request.data.get('points')
            if points:
                points = float(points)
                balance = request.user.wallet_balance(),
                user_balance = balance[0] if balance is not None else 0
                if not user_balance or user_balance < points:
                    err_txt = {"error": f"In sufficient points. Requested : {points} available : {user_balance}"}
                    return self.bad_request_response("Something went wrong !", err_txt)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.bad_request_response("Something went wrong !", err_msg(e))


"""
Admin app APIs are listed below
"""


# Admin can list and create new users
class UserListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    queryset = CustomUser.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = CustomUserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'uuid']
    pagination_class = LimitOffsetPagination
    permission_classes = [IsPortalManager]  # Replace with appropriate permissions

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            filter_field = self.request.query_params.get('filter_field')
            filter_value = self.request.query_params.get('filter_value')

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
            logger.error(e)
            return self.server_error_response("Something went wrong!", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            logger.error(e)
            return self.server_error_response("Something went wrong!", err_msg(e))


# Admin can List and Update users.
class UserRetrieveUpdateDestroyAPIView(CustomResponseMixin, RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = CustomUserSerializer
    permission_classes = [IsPortalManager]  # Replace with appropriate permissions
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return self.success_response("Retrieved successfully", serializer.data)
        except Exception as e:
            logger.error(e)
            return self.server_error_response("Something went wrong!", err_msg(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.success_response("Updated successfully", data=serializer.data)
            return self.bad_request_response("Invalid data provided", data=serializer.errors)
        except Exception as e:
            logger.error(e)
            return self.server_error_response("Something went wrong!", err_msg(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
            return self.server_error_response("Something went wrong!", err_msg(e))


# Reset Use Password to "Pass@123"
class ResetUserPassword(APIView):
    permission_classes = [IsPortalManager]

    def get_object(self, uuid):
        try:
            obj = User.objects.get(uuid=id)
            return obj
        except:
            return None

    def post(self, request):
        try:
            json_data = json.loads(request.body)
            uuid = str(json_data['uuid'])
            object = self.get_object(uuid)
            password = config('USER_PASSWORD', default='Pass@123')
            if object is not None:
                object.set_password(password)
                object.save()
                res_data = {
                    'success': True, 'data': 'User password reset to default Password',
                    'message': f'User password for {object.username} reset to : {password}'}
                return Response(res_data, status=status.HTTP_200_OK)
            else:
                res_data = {'success': False, 'message': 'Password reset failed', 'data': "No user objects found"}
                return Response(res_data, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            logger.error(ex)
            res_data = {'success': False, "message": 'Some thing went wrong', 'data': err_msg(ex)}
            return Response(res_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Notification serializer
class NotificationListCreateAPIView(CustomResponseMixin, ListCreateAPIView):
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'msg_id', 'uuid']
    ordering_fields = ['-id']  # Specify fields for ordering

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Notifications.objects.filter(is_deleted=False, user=self.request.user)
        filter_field = self.request.query_params.get('filter_field')
        filter_value = self.request.query_params.get('filter_value')

        if filter_field and filter_value:
            filter_args = {filter_field: filter_value}
            queryset = queryset.filter(**filter_args)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
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
            return self.server_error_response("Something went wrong!", err_msg(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.created_response("Successfully created", serializer.data)
        except Exception as e:
            return self.server_error_response("Something went wrong!", err_msg(e))
