import random
from django.core.management.base import BaseCommand
from django.db import transaction
from assignments.models import Assignment, Review
from participants.models import Participant

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
            default=3,
            help='Minimum number of reviews each assignment should receive.'
        )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                reviews_per_participant = options['reviews_per_participant']
                reviews_per_assignment = options['reviews_per_assignment']

                self.stdout.write('Fetching participants and assignments...')
                participants = list(Participant.objects.all())
                assignments = list(Assignment.objects.all())

                if not participants or not assignments:
                    self.stdout.write(self.style.WARNING('No participants or assignments found. Exiting.'))
                    return

                # Initialize review counts
                self.stdout.write('Initializing review counts...')
                assignment_review_counts = {
                    a.id: Review.objects.filter(assignment=a).count() for a in assignments
                }
                participant_review_counts = {
                    p.id: Review.objects.filter(reviewer=p).count() for p in participants
                }

                # Build a map of participant to assignments they can review
                self.stdout.write('Building assignable assignments list...')
                assignable_assignments = {}
                for participant in participants:
                    # Exclude the participant's own assignment
                    assignable = [a for a in assignments if a.participant != participant]
                    assignable_assignments[participant.id] = assignable

                # Shuffle assignments for randomness
                for assignment_list in assignable_assignments.values():
                    random.shuffle(assignment_list)

                total_reviews_assigned = 0

                # Assign reviews to participants
                self.stdout.write('Assigning reviews...')
                for participant in participants:
                    current_review_count = Review.objects.filter(reviewer=participant, feedback='').count()

                    # Skip if participant has already been assigned the required number of reviews
                    if current_review_count >= reviews_per_participant:
                        continue

                    # Get assignments not yet assigned to this participant
                    potential_assignments = [
                        a for a in assignable_assignments[participant.id]
                        if not Review.objects.filter(assignment=a, reviewer=participant).exists()
                    ]

                    # Sort potential assignments by least number of reviews to balance
                    potential_assignments.sort(key=lambda a: assignment_review_counts[a.id])

                    reviews_needed = reviews_per_participant - current_review_count

                    for assignment in potential_assignments:
                        if reviews_needed <= 0:
                            break
                        if assignment_review_counts[assignment.id] >= reviews_per_assignment:
                            continue  # Skip assignments that already have enough reviews

                        # Assign the review without feedback or reviewed_at
                        Review.objects.create(
                            assignment=assignment,
                            reviewer=participant,
                            feedback=''  # Feedback will be provided later by the participant
                            # reviewed_at remains null
                        )
                        assignment_review_counts[assignment.id] += 1
                        participant_review_counts[participant.id] += 1
                        reviews_needed -= 1
                        total_reviews_assigned += 1

                self.stdout.write(self.style.SUCCESS(f'Total reviews assigned: {total_reviews_assigned}'))

        except Exception as e:
            import traceback
            self.stderr.write('An error occurred:')
            self.stderr.write(str(e))
            traceback.print_exc()