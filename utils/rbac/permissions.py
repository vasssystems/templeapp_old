# webapp/utils/Rbac/Permissions.py
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model, authenticate
import logging

User = get_user_model()
logger = logging.getLogger("django")


# Check for django staff user permissions
class IsTechStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        index_id = view.kwargs
        try:
            user_scope = request.user.user_scope
            if request.user.is_STAFF:
                return True
            else:
                return False
        except Exception as ex:
            logger.error(ex)
            return False


# Allow Get method for Everybody and Allow Post for Only Authenticated Users
class IsGetOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        logger.info(f"Logged user : {request.user}")
        filter_param = request.query_params.get('filter')
        # allow all GET requests
        if request.method == 'GET':
            if filter_param == "my_listing":
                return request.user.is_authenticated
            return True
        elif request.user and request.user.is_authenticated:
            return True
        else:
            return False


# Allow Get method for All user and Allow Post for Only Authenticated User Roles.
class IsGetOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        logger.info(f"Logged user : {request.user}")
        # allow all GET requests
        if request.method == 'GET':
            return True
        elif request.user and request.user.is_authenticated:

            try:
                user_scope = request.user.user_scope
                if str(user_scope) in ["2", "3"]:
                    return True
                else:
                    return False
            except Exception as ex:
                logger.error(ex)
                return False
        else:
            return False


# Check for portal Admin permissions
class IsPortalAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        index_id = view.kwargs
        try:
            user_scope = request.user.user_scope
            if user_scope == "2":
                return True
            else:
                return False
        except Exception as ex:
            logger.error(ex)
            return False


# Check for portal Manager permissions
class IsPortalManager(permissions.BasePermission):
    def has_permission(self, request, view):
        index_id = view.kwargs
        try:
            user_scope = request.user.user_scope
            if user_scope in ("2" or "3"):
                return True
            else:
                return False
        except Exception as ex:
            logger.error(ex)
            return False


# Check for portal STAFF Coordinator permissions
class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        index_id = view.kwargs
        try:
            user_scope = request.user.user_scope
            if user_scope == "6":
                return True
            else:
                return False
        except Exception as ex:
            logger.error(ex)
            return False


# Check for portal Admin or Object Owner (Creator)
class IsDataOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        index_id = view.kwargs
        try:
            user_scope = request.user.user_scope if request.user.is_authenticated else None
            if request.method == 'GET':
                return True
            elif user_scope in ("1", "2", "3"):
                return True
            # Check for the Instance or Object is owned by the current Logged user
            # AI Need to generate a logic for Access the instance here.
            elif str(obj.created_by) == str(request.user.uuid):
                return True
            else:
                return False
        except Exception as ex:
            logger.error(ex)
            return False
