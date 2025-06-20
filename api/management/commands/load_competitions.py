# api/management/commands/load_competitions.py
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import Competition

class Command(BaseCommand):
    help = 'Loads competition data from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the competitions.json file.')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        self.stdout.write(self.style.SUCCESS(f'Starting to load competitions from {json_file_path}'))

        Competition.objects.all().delete()
        self.stdout.write(self.style.WARNING('Deleted all existing competitions.'))

        with open(json_file_path, 'r') as f:
            competitions_data = json.load(f)
            
            for item in competitions_data:
                # --- Data Cleaning and Transformation ---

                # Convert array fields to comma-separated strings
                tags_str = ", ".join(item.get('tags', []))
                benefits_str = ", ".join(item.get('benefits', []))
                rewards_str = ", ".join(item.get('nonMonetaryRewards', []))

                # Handle date conversion for "YYYY-MM-DD" or empty strings
                deadline_str = item.get('deadline')
                deadline_obj = None
                if deadline_str:
                    try:
                        deadline_obj = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                    except ValueError:
                        self.stdout.write(self.style.ERROR(f"Could not parse date: {deadline_str} for '{item.get('title')}'"))
                
                # Map difficulty from JSON values to model choices
                difficulty_mapping = {'High': 'Hard', 'Medium': 'Medium', 'Low': 'Easy'}
                difficulty_val = difficulty_mapping.get(item.get('difficulty'), 'Medium')

                # Map team requirement from JSON values to model choices
                team_req_mapping = {'team': 'Team', 'any': 'Both'}
                team_req_val = team_req_mapping.get(item.get('teamRequirement'), 'Both')

                # --- Create Competition Object ---
                Competition.objects.create(
                    title=item.get('title'),
                    description=item.get('description'),
                    domain=item.get('domain'),
                    tags=tags_str,
                    prizeAmount=item.get('prizeAmount'),
                    nonMonetaryRewards=rewards_str,
                    deadline=deadline_obj,
                    benefits=benefits_str,
                    difficulty=difficulty_val,
                    website=item.get('website'),
                    organizer=item.get('organizer'),
                    timeCommitment=item.get('timeCommitment'),
                    teamRequirement=team_req_val,
                    targetAudience=item.get('targetAudience')
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all competitions into the database.'))

