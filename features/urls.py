# webapp/features/urls.py
from django.urls import path

from .views import (
    DepartmentListCreateAPIView, DepartmentRetrieveUpdateDestroyAPIView,
    ClubsListCreateAPIView, ClubsRetrieveUpdateDestroyAPIView,
    BatchListCreateAPIView, BatchRetrieveUpdateDestroyAPIView,
    FaqListCreateAPIView, FaqRetrieveUpdateDestroyAPIView,
    NoticeBoardListCreateAPIView, NoticeBoardRetrieveUpdateDestroyAPIView,
    )

app_name = "features"

urlpatterns = [
    path('departments/', DepartmentListCreateAPIView.as_view(), name='department-list-create'),
    path('departments/<uuid:uuid>/', DepartmentRetrieveUpdateDestroyAPIView.as_view(), name='department-detail'),

    path('clubs/', ClubsListCreateAPIView.as_view(), name='clubs-list-create'),
    path('clubs/<uuid:uuid>/', ClubsRetrieveUpdateDestroyAPIView.as_view(), name='clubs-detail'),

    path('batch/', BatchListCreateAPIView.as_view(), name='batch-list-create'),
    path('batch/<uuid:uuid>/', BatchRetrieveUpdateDestroyAPIView.as_view(), name='batch-detail'),

    path('faq/', FaqListCreateAPIView.as_view(), name='faq-list-create'),
    path('faq/<uuid:uuid>/', FaqRetrieveUpdateDestroyAPIView.as_view(), name='faq-detail'),

    path('noticeboard/', NoticeBoardListCreateAPIView.as_view(), name='notice-board-list-create'),
    path('noticeboard/<uuid:uuid>/', NoticeBoardRetrieveUpdateDestroyAPIView.as_view(), name='notice-board-detail'),

]
