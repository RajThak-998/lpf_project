from django.urls import path
from . import views

urlpatterns = [
    path('participant-progress/', views.participant_progress, name='participant-progress'),
    path('assignment-status/', views.assignment_status, name='assignment-status'),
    path('assignment-submission-status/', views.assignment_submission_status, name='assignment-submission-status'),
]