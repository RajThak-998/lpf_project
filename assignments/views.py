from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Assignment, Review
from participants.models import Participant
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

    def get_queryset(self):
        # Filter reviews based on 'reviewer_uid' query parameter
        reviewer_uid = self.request.query_params.get('reviewer_uid')
        if reviewer_uid:
            return Review.objects.filter(reviewer__uid=reviewer_uid)
        return super().get_queryset()

# Participants fetch their assigned reviews using their uid:
# GET /api/assignments/reviews/?reviewer_uid=UID044

# Participants submit feedback by updating the feedback field of the review:
# PATCH /api/assignments/reviews/{review_id}/

# note: review_id is the id that represent the uniqueness of a reviewer and the assignment, donot think it as the reviewer_id