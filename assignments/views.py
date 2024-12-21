from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Assignment, Review
from .serializers import AssignmentSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['participant']
    search_fields = ['title', 'content']
    ordering_fields = ['submitted_at']

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['assignment', 'reviewer']
    search_fields = ['feedback']
    ordering_fields = ['reviewed_at']

    def get_queryset(self):
        # Participants can only see their own review assignments
        if self.request.user.is_superuser:
            return Review.objects.all()
        else:
            return Review.objects.filter(reviewer__email=self.request.user.email)

    def perform_update(self, serializer):
        # Ensure that only the assigned reviewer can update the review
        review = self.get_object()
        if review.reviewer.email != self.request.user.email:
            raise PermissionDenied("You do not have permission to edit this review.")
        serializer.save()