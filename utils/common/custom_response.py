# webapp/features/custom_response.py
from rest_framework.response import Response
from rest_framework import status


class CustomResponseMixin:
    def create_response(self, status_code, message, data=None):
        success = status.is_success(status_code)
        response_data = {
            'success': success,
            'message': message,
            'data': data if data is not None else {}
        }
        return Response(response_data, status=status_code)

    def success_response(self, message, data=None):
        return self.create_response(status.HTTP_200_OK, message, data)

    def created_response(self, message, data=None):
        return self.create_response(status.HTTP_201_CREATED, message, data)

    def no_content_response(self, message, data=None):
        return self.create_response(status.HTTP_204_NO_CONTENT, message, data)

    def bad_request_response(self, message, data=None):
        return self.create_response(status.HTTP_400_BAD_REQUEST, message, data)

    def unauthorized_response(self, message, data=None):
        return self.create_response(status.HTTP_401_UNAUTHORIZED, message, data)

    def forbidden_response(self, message, data=None):
        return self.create_response(status.HTTP_403_FORBIDDEN, message, data)

    def not_found_response(self, message, data=None):
        return self.create_response(status.HTTP_404_NOT_FOUND, message, data)

    def server_error_response(self, message, data=None):
        return self.create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message, data)
