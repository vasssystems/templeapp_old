# webapp/utils/urls.py
from django.urls import path
from .views import *
from .views import ToggleStatusView, BulkStatusView

app_name = "utils"

handler404 = custom_404

urlpatterns = [
    path('', IndexAPIView.as_view(), name="index"),
    path('toggle-status/', ToggleStatusView.as_view(), name='toggle_status'),
    path('bulk-status/', BulkStatusView.as_view(), name='bulk_status'),
]
