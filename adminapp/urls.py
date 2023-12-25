# webapp/adminapp/urls.py
from django.urls import path, include

from . import views

app_name = "adminapp"

urlpatterns = [
    path('usersagreements/', views.AgreementsListCreateAPIView.as_view(), name='users-agreements'),
    path('usersagreements/<uuid:uuid>/', views.AgreementsDetailsAPIView.as_view(), name='users-agreements-detail'),
    path('adminconfig/', views.AdminConfigListCreateAPIView.as_view(), name='admin-config'),
    path('adminconfig/<uuid:uuid>/', views.AdminConfigDetailsAPIView.as_view(), name='admin-config-detail'),
    path('logos/', views.LogosListCreateAPIView.as_view(), name='logos'),
    path('logos/<uuid:uuid>/', views.LogosDetailsAPIView.as_view(), name='logos-detail'),
    path('payments/', views.PaymentsListCreateAPIView.as_view(), name='payments'),
    path('payments/<uuid:uuid>/', views.PaymentsDetailsAPIView.as_view(), name='payments-detail'),
    path('generalsettings/', views.GeneralSettingsListCreateAPIView.as_view(), name='general-settings'),
    path('generalsettings/<uuid:uuid>/', views.GeneralSettingsDetailsAPIView.as_view(), name='general-settings-detail'),
]
