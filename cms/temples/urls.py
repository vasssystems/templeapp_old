# webapp/cms/temples/urls.py
from django.urls import path
from .views import *

app_name = "temples"

urlpatterns = [
    path('temple-details/', TempleListCreateAPIView.as_view(), name='temple-details-list-create'),
    path('temple-details/<uuid:uuid>/', TempleDetailsAPIView.as_view(), name='temple-detailed-view'),
    path('service-details/', ServiceListCreateAPIView.as_view(), name='service-details-list-create'),
    path('service-details/<uuid:uuid>/', ServiceDetailsAPIView.as_view(), name='service-detailed-view'),

    path('temple-gallery-details/', TempleGalleryListCreateAPIView.as_view(), name='temple-gallery-list-create'),
    path('temple-gallery/<uuid:uuid>/', TempleGalleryDetailsAPIView.as_view(), name='temple-gallery-detailed-view'),
    path('service-gallery-details/', ServiceGalleryCreateAPIView.as_view(), name='service-gallery-list-create'),
    path('service-gallery-details/<uuid:uuid>/', ServiceGalleryDetailsAPIView.as_view(), name='service-gallery-details'),

    path('pooja-details/', PoojaListCreateAPIView.as_view(), name='pooja-details-list-create'),
    path('pooja-details/<uuid:uuid>/', PoojaDetailsAPIView.as_view(), name='pooja-detailed-view'),
    path('festivals-details/', FestivalListCreateAPIView.as_view(), name='festivals-details-list-create'),
    path('festivals-details/<uuid:uuid>/', FestivalDetailsAPIView.as_view(), name='festivals-detailed-view'),
    path('blog-details/', BlogListCreateAPIView.as_view(), name='blog-details-list-create'),
    path('blog-details/<uuid:uuid>/', BlogDetailsAPIView.as_view(), name='blog-detailed-view')

]

# Not Using APIs
#   path('with-fields/<uuid:uuid>/', GetCriterionFields.as_view(), name='criterion-with-fields'),
