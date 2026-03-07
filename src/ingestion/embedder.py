class VectorEmbedder:
    """
    Calls embedding models (e.g., OpenAI text-embedding-ada-002).
    """
    def embed(self, text_chunks: list) -> list:
        return [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]] # Mock vectors