from django.core.management.base import BaseCommand
from Hirely.models import Assessment
import json
import os

class Command(BaseCommand):
    help="Saves or updates scraped individual assessment data into PostgeSQL"
    
    def handle(self, *args, **kwargs):
        json_path = "shl_assessments.json"
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR("JSON file not found. Run scrape_assessments first."))
            return
        
        with open(json_path, "r") as f:
            assessments = json.load(f)
            
        self.stdout.write(f"Processing {len(assessments)} assessments...")
        
        created_count = 0
        updated_count = 0
        
        for item in assessments:
            obj, created = Assessment.objects.update_or_create(
                title=item["title"],  # Assuming title is unique
                defaults={
                    "link": item["link"],
                    "description": item["description"],
                    "remote_support": item["remote_support"],
                    "adaptive_support": item["adaptive_support"],
                    "test_type": item["test_type"],
                    "duration_min": item["duration_minutes"],
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done! Created: {created_count}, Updated: {updated_count} assessments."
        ))
            
            