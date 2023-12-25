# webapp/utils/views.py
from rest_framework.exceptions import NotFound
from rest_framework.views import exception_handler
from django.http import JsonResponse
from django.apps import apps
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from utils.rbac.permissions import IsPortalManager, IsGetOrIsAdmin
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def custom_404(request, exception):
    response = {
        'success': False,
        'message': 'The requested resource was not found',
        'status': 404,
        'data': 'Not Found'
    }
    return JsonResponse(response, status=404)


def index(request):
    response = {
        'success': True,
        'message': 'Welcome to API index',
        'status': 200,
        'data': {}
    }
    return JsonResponse(response, status=200)


def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = exception_handler(exc, context)

    # If it's a 404 error, override the response
    if isinstance(exc, NotFound):
        response.data = {
            "detail": "Not Found.",
            "error_code": "404",
        }
        response.status_code = 404

    return response


def get_app_name_from_slug(slug):
    # Define a dictionary with slugs and their corresponding app names
    slug_to_app = {
        'customuser': 'user',
        'notifications': 'user',
        'wallet': 'user',
        'departments': 'features',
        'clubs': 'features',
        'batch': 'features',
        'faq': 'features',
        'eventuploader': 'features',
        'students': 'features',
        'staff': 'features',
        'noticeboard': 'features',
        'adminconfig': 'adminapp',
        'payments': 'adminapp',
        'generalsettings': 'adminapp',
        'logos': 'adminapp',
        'usersgreements': 'adminapp',
        'templedata': 'cms',
        'servicedata': 'cms',
        'templegallery': 'cms',
        'servicegallery': 'cms',
        'poojas': 'cms',
        'festivals': 'cms',
        'blog': 'cms',
        'bookings': 'cms',
    }

    return slug_to_app.get(slug, None)


# Function to List all Objects based on slug passed for Select box API's
def get_api_objects(slug):
    try:
        option_list = []
        app_name = get_app_name_from_slug(slug)
        model = apps.get_model(app_label=app_name, model_name=slug)
        object_list = model.objects.filter(is_deleted=False, status=True).order_by("id")
        for obj in object_list:
            obj_dict = {'id': obj.id, 'name': obj.name, 'code': obj.code, 'uuid': obj.uuid}
            option_list.append(obj_dict)
        return option_list
    except model.DoesNotExist:
        logger.error(f"get_api_objects | Model Doesn't exist for given slug")
        return []
    except Exception as ex:
        logger.error(f" get_api_objects | Somthing went wrong : {ex}")
        return []


# Toggle status of Objects based on Slug and object UUID
class ToggleStatusView(APIView):
    permission_classes = [IsGetOrIsAdmin]

    def get_object(self, app_name, model_name, obj_id):
        try:
            model = apps.get_model(app_label=app_name, model_name=model_name)
            return model.objects.get(uuid=obj_id)
        except model.DoesNotExist:
            logger.error(f"ToggleStatusView | Model Doesn't exist for given slug")
            return None
        except Exception as ex:
            logger.error(f" ToggleStatusView | Somthing went wrong : {ex}")
            return None

    def get(self, request):
        return Response({'success': False, 'message': 'Invalid Method'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            json_data = json.loads(request.body)
            slug = str(json_data.get('slug')) if 'slug' in json_data else None
            obj_id = json_data.get('obj_id') if 'obj_id' in json_data else None
            status_ = json_data.get('status') if 'status' in json_data else None

            if obj_id is not None:
                app_name = get_app_name_from_slug(slug)
                if app_name:
                    model_name = slug.capitalize()
                    obj = self.get_object(app_name, model_name, obj_id)
                    if obj:
                        if status_ is not None:
                            obj.status = status_
                            obj.save()
                            res_data = {'id': obj.id, 'uuid': obj.uuid, 'status': obj.status}
                            return Response(
                                {'success': True, 'message': 'Status updated successfully', 'data': res_data},
                                status=status.HTTP_202_ACCEPTED)
                        else:
                            return Response({'success': False, 'message': 'Invalid data', 'data': {}},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'success': False, 'message': 'Object not found', 'data': {}},
                                        status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'success': False, 'message': 'Invalid slug', 'data': {}},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success': False, 'message': 'Object ID not found', 'data': {}},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response({'success': False, 'message': 'Something went wrong', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)


class BulkStatusView(APIView):
    permission_classes = [IsGetOrIsAdmin]

    def get_object(self, app_name, model_name, obj_id):
        try:
            model = apps.get_model(app_label=app_name, model_name=model_name)
            return model.objects.get(uuid=obj_id)
        except model.DoesNotExist:
            logger.error(f"BulkStatusView | Model Doesn't exist for given slug")
            return None
        except Exception as ex:
            logger.error(f" BulkStatusView | Something went wrong: {ex}")
            return None

    def post(self, request):
        try:
            json_data = request.data  # Access data directly from request.data instead of parsing request.body
            slug = json_data.get('slug')
            obj_ids = json_data.get('obj_ids', [])  # Assuming obj_ids is a list of object IDs
            status_ = json_data.get('status')

            if not slug or not obj_ids or status_ is None:
                return Response({'success': False, 'message': 'Invalid data', 'data': {}},
                                status=status.HTTP_400_BAD_REQUEST)

            app_name = get_app_name_from_slug(slug)
            if not app_name:
                return Response({'success': False, 'message': 'Invalid slug', 'data': {}},
                                status=status.HTTP_400_BAD_REQUEST)

            model_name = slug.capitalize()
            successful_updates = []
            failed_updates = []

            for obj_id in obj_ids:
                obj = self.get_object(app_name, model_name, obj_id)
                if obj:
                    obj.status = status_
                    obj.save()
                    res_data = {'id': obj.id, 'uuid': obj.uuid, 'status': obj.status}
                    successful_updates.append(res_data)
                else:
                    failed_updates.append({'obj_id': obj_id, 'message': 'Object not found'})

            response_data = {
                'success': True,
                'message': 'Status updated successfully for objects',
                'data': {
                    'successful_updates': successful_updates,
                    'failed_updates': failed_updates
                }
            }

            return Response(response_data, status=status.HTTP_202_ACCEPTED)

        except Exception as ex:
            logger.error(ex)
            return Response({'success': False, 'message': 'Something went wrong', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)
