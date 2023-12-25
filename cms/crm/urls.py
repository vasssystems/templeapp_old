# webapp/cms/crm/urls.py

from django.urls import path
from .views import WelcomeAPIView

app_name = "crm"

urlpatterns = [
    path('', WelcomeAPIView.as_view(), name='welcome'),
]
