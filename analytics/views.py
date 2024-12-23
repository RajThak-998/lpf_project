from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from participants.models import Participant
from assignments.models import Review, Assignment
from django.db.models import Count, Q
from django.db.models.functions import Greatest


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def participant_progress(request):
    MIN_REVIEWS_GIVEN = 3

    uid = request.query_params.get('uid', None)
    participants_qs = Participant.objects.all()

    # Filter by 'uid' if provided -- /participant-progress/?uid=UID123
    if uid:
        participants_qs = participants_qs.filter(uid=uid)

    participants = participants_qs.annotate(
        reviews_given_count=Count(
            'reviews_given',
            filter=~Q(reviews_given__feedback='')
        ),
        reviews_remaining=Greatest(
            MIN_REVIEWS_GIVEN - Count(
                'reviews_given',
                filter=~Q(reviews_given__feedback='')
            ),
            0
        ),
        reviews_received_count=Count(
            'assignments__reviews',
            filter=~Q(assignments__reviews__feedback='')
        ),
    ).values(
        'uid',
        'name',
        'reviews_given_count',
        'reviews_remaining',
        'reviews_received_count'
    )

    return Response({'participants': list(participants)})
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def assignment_status(request):
    # Assuming each assignment should receive MIN_REVIEWS_RECEIVED reviews
    MIN_REVIEWS_RECEIVED = 2

    id = request.query_params.get('id', None)
    assignments_qs = Assignment.objects.all()

    # Filter by 'id' if provided -- /assignment_status/?id=UID123
    if id:
        assignments_qs = assignments_qs.filter(id=id)

    assignments = assignments_qs.annotate(
        reviews_received=Count(
            'reviews',
            filter=~Q(reviews__feedback='')
        ),
        reviews_remaining=MIN_REVIEWS_RECEIVED - Count(
            'reviews',
            filter=~Q(reviews__feedback='')
        ),
    ).values('id', 'title', 'reviews_received', 'reviews_remaining')

    return Response({'assignments': list(assignments)})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def assignment_submission_status(request):
    # Get all participants
    all_participants = Participant.objects.all()

    # Participants who have submitted assignments
    submitted = Participant.objects.filter(assignments__isnull=False).distinct()

    # Participants who have not submitted assignments
    not_submitted = Participant.objects.filter(assignments__isnull=True)

    # Serialize the data
    submitted_data = submitted.values('uid', 'name', 'email')
    not_submitted_data = not_submitted.values('uid', 'name', 'email')

    return Response({
        'submitted': list(submitted_data),
        'not_submitted': list(not_submitted_data),
    })