from django.urls import path, include
from rest_framework.routers import DefaultRouter
from data_provider.api.views import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
]