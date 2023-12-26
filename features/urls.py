# webapp/features/urls.py
from django.urls import path

from .views import (
    DepartmentListCreateAPIView, DepartmentRetrieveUpdateDestroyAPIView,
    FaqListCreateAPIView, FaqRetrieveUpdateDestroyAPIView,
    NoticeBoardListCreateAPIView, NoticeBoardRetrieveUpdateDestroyAPIView,
    )

app_name = "features"

urlpatterns = [
    path('departments/', DepartmentListCreateAPIView.as_view(), name='department-list-create'),
    path('departments/<uuid:uuid>/', DepartmentRetrieveUpdateDestroyAPIView.as_view(), name='department-detail'),

    path('faq/', FaqListCreateAPIView.as_view(), name='faq-list-create'),
    path('faq/<uuid:uuid>/', FaqRetrieveUpdateDestroyAPIView.as_view(), name='faq-detail'),

    path('noticeboard/', NoticeBoardListCreateAPIView.as_view(), name='notice-board-list-create'),
    path('noticeboard/<uuid:uuid>/', NoticeBoardRetrieveUpdateDestroyAPIView.as_view(), name='notice-board-detail'),

]
