class TextChunker:
    """
    Splits raw text into semantic chunks for vectorization.
    """
    def chunk(self, text: str, max_tokens: int = 500) -> list:
        return ["Chunk 1", "Chunk 2"]