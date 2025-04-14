from django.core.management.base import BaseCommand
from Hirely.models import Assessment
from qdrant_client import QdrantClient
from Hirely.qdrant_utils import create_collection, upsert_embeddings_to_qdrant

class Command(BaseCommand):
    help = "Migrate saved embeddings from PostgreSQL to Qdrant"
    
    def handle (self, *args, **kwargs):
        create_collection()
        assessments = Assessment.objects.exclude(embedding = None)
        upsert_embeddings_to_qdrant(assessments)
        