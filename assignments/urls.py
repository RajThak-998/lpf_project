from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import AssignmentViewSet, ReviewViewSet

router = SimpleRouter()
router.register(r'assignments', AssignmentViewSet)
router.register(r'reviews', ReviewViewSet)

app_name = 'assignments'

urlpatterns = [
    path('', include(router.urls)),
]