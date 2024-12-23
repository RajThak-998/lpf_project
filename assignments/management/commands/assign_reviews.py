from django.core.management.base import BaseCommand
from django.db import transaction
from assignments.models import Assignment, Review
from participants.models import Participant
import random

class Command(BaseCommand):
    help = 'Assign peer reviews to participants.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reviews_per_participant',
            type=int,
            default=3,
            help='Number of reviews each participant should perform.'
        )
        parser.add_argument(
            '--reviews_per_assignment',
            type=int,
            default=2,
            help='Minimum number of reviews each assignment should receive.'
        )

    def handle(self, *args, **options):
        reviews_per_participant = options['reviews_per_participant']
        reviews_per_assignment = options['reviews_per_assignment']

        self.stdout.write('Fetching participants and assignments...')
        participants = list(Participant.objects.all())
        assignments = list(Assignment.objects.all())

        if not participants or not assignments:
            self.stdout.write(self.style.WARNING('No participants or assignments found. Exiting.'))
            return

        # Initialize review counts
        assignment_review_counts = {a.id: 0 for a in assignments}
        participant_review_counts = {p.id: 0 for p in participants}

        # Build a list of assignable assignments for each participant
        assignable_assignments = {}
        for participant in participants:
            # Exclude the participant's own assignment
            assignable = [a for a in assignments if a.participant != participant]
            random.shuffle(assignable)
            assignable_assignments[participant.id] = assignable

        total_reviews_assigned = 0

        # Assign reviews to participants
        self.stdout.write('Assigning reviews...')
        with transaction.atomic():
            for participant in participants:
                reviews_needed = reviews_per_participant - participant_review_counts[participant.id]
                assignments_to_review = assignable_assignments[participant.id]

                for assignment in assignments_to_review:
                    if reviews_needed <= 0:
                        break
                    if assignment_review_counts[assignment.id] >= reviews_per_assignment:
                        continue
                    # Create the review
                    Review.objects.create(
                        assignment=assignment,
                        reviewer=participant,
                        feedback=''  # Feedback will be added later by the participant
                    )
                    assignment_review_counts[assignment.id] += 1
                    participant_review_counts[participant.id] += 1
                    reviews_needed -= 1
                    total_reviews_assigned += 1

        self.stdout.write(self.style.SUCCESS(f'Total reviews assigned: {total_reviews_assigned}'))