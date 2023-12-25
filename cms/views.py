# webapp/cms/views.py
from rest_framework.views import APIView
from rest_framework.response import Response


class WelcomeAPIView(APIView):
    def get(self, request):
        # Return a welcome message for the blank endpoint
        welcome_message = "Welcome to the API endpoint of cms app. This is the index page."

        return Response({"status": True, "message": welcome_message, "data": {}})
