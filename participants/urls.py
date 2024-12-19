from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import ParticipantViewSet

router = SimpleRouter()
router.register(r'', ParticipantViewSet)

app_name = 'participants'

urlpatterns = [
    path('', include(router.urls)),
]