from django.shortcuts import render

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Participant
from .serializers import ParticipantSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['uid', 'email']  # Fields you want to filter on
    search_fields = ['name', 'email']    # Fields you want to enable search on
    ordering_fields = ['name', 'uid']    # Fields you can order by
