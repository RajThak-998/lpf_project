"""
Management command to import assignments from an Excel or CSV file.

Usage:
    python manage.py import_assignments --file=path/to/file.csv

Options:
    --dry-run       Run the import without making any changes to the database.
    --batch-size    Number of records to process in each batch (default: 1000).
"""

import pandas as pd
from django.core.management.base import BaseCommand
from assignments.models import Assignment
from participants.models import Participant
from django.db import transaction
from django.db import connections
import os
import sys

class Command(BaseCommand):
    help = 'Imports assignment data from an Excel or CSV file into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            required=True,
            help='Path to the Excel or CSV file containing assignment data.'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run the import in dry run mode without making any changes to the database.'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=200,
            help='Number of records to process in each batch.'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']
        batch_size = options['batch_size']

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        try:
            # Determine file format and set reader accordingly
            if file_path.endswith('.csv'):
                reader = pd.read_csv(
                    file_path,
                    chunksize=batch_size,
                    iterator=True,
                )
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                reader = pd.read_excel(
                    file_path,
                    chunksize=batch_size,
                    iterator=True,
                    engine='openpyxl' if file_path.endswith('.xlsx') else None,
                )
            else:
                self.stderr.write(self.style.ERROR('Unsupported file format. Please provide a .csv or .xlsx file.'))
                return

            # Initialize counters
            total_rows = 0
            created_count = 0
            updated_count = 0
            skipped_count = 0

            # Process data in chunks
            for chunk in reader:
                total_rows += len(chunk)

                # Validate required columns
                required_columns = {'participant_uid', 'title', 'content'}
                if not required_columns.issubset(set(chunk.columns)):
                    missing_columns = required_columns - set(chunk.columns)
                    self.stderr.write(self.style.ERROR(f'Missing required columns: {", ".join(missing_columns)}'))
                    return

                # Start a database transaction for each chunk
                with transaction.atomic():
                    for index, row in chunk.iterrows():
                        participant_uid = row['participant_uid']
                        title = row['title']
                        content = row['content']

                        # Skip rows with missing required data
                        if pd.isnull(participant_uid) or pd.isnull(title) or pd.isnull(content):
                            self.stderr.write(self.style.WARNING(f'Skipping row {index + 1}: Missing required data.'))
                            skipped_count += 1
                            continue

                        # Data cleanup
                        participant_uid = str(participant_uid).strip()
                        title = str(title).strip()
                        content = str(content).strip()

                        # Get the participant
                        try:
                            participant = Participant.objects.get(uid=participant_uid)
                        except Participant.DoesNotExist:
                            self.stderr.write(self.style.WARNING(f'Skipping row {index + 1}: Participant with UID {participant_uid} does not exist.'))
                            skipped_count += 1
                            continue

                        # Create the assignment
                        assignment = Assignment(
                            participant=participant,
                            title=title,
                            content=content
                        )

                        if not dry_run:
                            assignment.save()
                        created_count += 1
                        action = 'Would create' if dry_run else 'Created'

                        self.stdout.write(f'{action} assignment: {title} by {participant.name}')

                    if dry_run:
                        self.stdout.write(self.style.WARNING('Dry run completed for this batch. No changes were made to the database.'))
                        # Rollback the transaction
                        raise Exception('Dry run - rolling back transaction for this batch.')

                # Clear any database connections to avoid memory leaks
                connections.close_all()

            self.stdout.write(self.style.SUCCESS('Assignment data import completed successfully.'))
            self.stdout.write(f'Total rows processed: {total_rows}')
            self.stdout.write(f'Assignments created: {created_count}')
            self.stdout.write(f'Rows skipped: {skipped_count}')

        except Exception as e:
            if dry_run and 'rolling back transaction' in str(e):
                # Expected exception for dry run to rollback transaction
                pass
            else:
                self.stderr.write(self.style.ERROR(f'An error occurred: {str(e)}'))
                sys.exit(1)