from django.urls import include, path
from rest_framework import routers
from .views import ParticipantViewSet

router = routers.DefaultRouter()
router.register(r'participants', ParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
