import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models


class QdrantManager:
    """Manage Qdrant connection and collection initialization."""

    def __init__(self) -> None:
        """Initialize Qdrant client and default collection."""
        load_dotenv()
        self.client = QdrantClient(
            url=os.getenv("QDRANT_HOST", "http://localhost:6333")
        )
        self.init_collection()

    def init_collection(
        self, collection_name: str = "knowledge_base", vector_size: int = 1536
    ) -> None:
        """Create collection if it does not exist."""
        try:
            if self.client.collection_exists(collection_name=collection_name):
                return

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE,
                ),
            )
        except Exception as error:
            print(f"[QdrantManager.init_collection] Collection init error: {error}")
class VectorStoreClient:
    """
    Adapter for Qdrant / FAISS.
    Handles Long-term Semantic Memory.
    """
    def __init__(self):
        pass # Initialize Qdrant client

    def search(self, query_vector: list, top_k: int = 3) -> list:
        return ["Relevant historical context 1", "Relevant historical context 2"]