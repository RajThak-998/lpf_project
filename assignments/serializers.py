from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Assignment, Review
from participants.models import Participant

# assigning serializer for  Assignmnet model

class AssignmentSerializer(serializers.ModelSerializer):
    participant = serializers.SlugRelatedField(
        slug_field='uid',
        queryset=Participant.objects.all()
    )

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ('submitted_at',)


# assigning serializer for Review model

class ReviewSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all())
    reviewer = serializers.SlugRelatedField(
        slug_field='uid',
        queryset=Participant.objects.all()
    )


    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('reviewed_at',)
        validators = [                          # prevent duplicate-review
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['assignment', 'reviewer'],
                message="This assignment has already been reviewed by this participant."
            )
        ]

    def validate(self,data):
        assignment = data.get('assignment')
        reviewer = data.get('reviewer')

        # Prevent self-review
        if assignment.participant == reviewer :
            raise serializers.ValidationError("Participant cannot review their own assignment")
        
        return data




