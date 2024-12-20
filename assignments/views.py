from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Assignment, Review
from .serializers import AssignmentSerializer, ReviewSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['participant']
    search_fields = ['title', 'content']
    ordering_fields = ['submitted_at']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['assignment', 'reviewer']
    search_fields = ['feedback']
    ordering_fields = ['reviewed_at']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
