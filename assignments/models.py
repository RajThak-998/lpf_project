from django.db import models
from participants.models import Participant
from rest_framework.validators import UniqueTogetherValidator

class Assignment(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.participant.name}"



class Review(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='reviews_given')
    feedback = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assignment', 'reviewer')

    def __str__(self):
        return f"Review of '{self.assignment.title}' by {self.reviewer.name}"

