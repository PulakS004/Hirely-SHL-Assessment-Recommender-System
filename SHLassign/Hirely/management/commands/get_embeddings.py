from django.core.management.base import BaseCommand
from Hirely.models import Assessment
from Hirely.utils import get_embedding_text, generate_embedding

class Command(BaseCommand):
    help = "Generate and save embeddings for assessments."
    
    def handle(self, *args, **kwargs):
        assessments = Assessment.objects.filter(embedding__isnull = True)
        for a in assessments:
            try:
                embedding_text = get_embedding_text(a)
                embedding = generate_embedding(embedding_text)
                a.embedding = embedding
                a.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed for {a.title}: {e}"))
                break
        return self.stdout.write(self.style.SUCCESS(f"Successfully saved embeddings"))