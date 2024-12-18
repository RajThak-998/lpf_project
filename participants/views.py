from django.shortcuts import render

from rest_framework import viewsets
from .models import Participant
from .serializers import ParticipantSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
