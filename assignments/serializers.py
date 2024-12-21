from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Assignment, Review
from participants.models import Participant
from django.utils import timezone

class AssignmentSerializer(serializers.ModelSerializer):
    participant = serializers.SlugRelatedField(
        slug_field='uid',
        queryset=Participant.objects.all()
    )

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ('submitted_at',)

class ReviewSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all())
    reviewer = serializers.SlugRelatedField(
        slug_field='uid',
        queryset=Participant.objects.all()
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('assigned_at', 'reviewed_at')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['assignment', 'reviewer'],
                message="This assignment has already been reviewed by this participant."
            )
        ]

    def validate(self, data):
        assignment = data.get('assignment')
        reviewer = data.get('reviewer')

        # Prevent self-review
        if assignment.participant == reviewer:
            raise serializers.ValidationError("Participants cannot review their own assignments.")

        return data

    def update(self, instance, validated_data):
        # Set the reviewed_at field when feedback is provided
        if 'feedback' in validated_data and validated_data['feedback']:
            instance.reviewed_at = timezone.now()
        return super().update(instance, validated_data)