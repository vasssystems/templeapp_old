# webapp/cms/urls.py
from django.urls import path, include
from .views import WelcomeAPIView

app_name = "cms"


urlpatterns = [
    path('', WelcomeAPIView.as_view(), name='welcome'),
    path('temples/', include("cms.temples.urls", namespace='temples')),
    path('crm/', include("cms.crm.urls", namespace='crm')),
]
