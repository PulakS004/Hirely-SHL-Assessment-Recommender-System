from django.core.management.base import BaseCommand
from Hirely.utils import extract_assessments
import json 
import time

class Command(BaseCommand):
    help = "Scrapes SHL Individual Test Solutions from SHL website and saves to a JSON file"
    
    def handle(self, *args, **kwargs):
        all_data = []
        for start in range(0, 372+12, 12):
            self.stdout.write(f"Scraping start={start}...")
            page_data = extract_assessments(start)
            all_data.extend(page_data)
            time.sleep(1)
            
        with open("shl_assessments.json", "w") as f:
            json.dump(all_data, f, indent=4)
            
        self.stdout.write(self.style.SUCCESS(f"Scraped and saved {len(all_data)} to shl_assessments.json"))
            