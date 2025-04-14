from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import Distance, VectorParams
import uuid

client = QdrantClient("http://localhost:6333")

def create_collection(collection_name = "assessments", vector_size=1536):
    if not client.collection_exists(collection_name):
        client.recreate_collection(
            collection_name= collection_name,
            vectors_config= VectorParams(size = vector_size, distance= Distance.COSINE)            
        )
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")
        
def upsert_embeddings_to_qdrant(assessments, collection_name = "assessments"):
    points = []

    for assessment in assessments:
        if assessment.embedding:
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=assessment.embedding,
                payload={
                    "title": assessment.title,
                    "link": assessment.link,
                    "description": assessment.description,
                    "duration_minutes": assessment.duration_min,
                    "test_type": assessment.test_type,
                }
            )
            points.append(point)
            
    if points:
        client.upsert(collection_name=collection_name, points=points)
        print(f"{len(points)} points uploaded to Qdrant.")
    else:
        print("No embeddings to upload.")
    