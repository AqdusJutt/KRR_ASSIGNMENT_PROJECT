"""Vector store implementation using FAISS for similarity search."""

import os
import pickle
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer

class VectorStore:
    
    """FAISS-based vector store for semantic similarity search."""
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", dimension: int = 384):
        """Initialize vector store with embedding model."""
        self.embedding_model_name = embedding_model
        self.dimension = dimension
        self.embeddings = []
        self.metadata = []
        self.next_id = 0
        
        # Load embedding model
        try:
            self.model = SentenceTransformer(embedding_model)
            self.dimension = self.model.get_sentence_embedding_dimension()
        except Exception as e:
            print(f"Warning: Could not load embedding model: {e}")
            print("Using random embeddings as fallback.")
            self.model = None
    
    def add(self, text: str, metadata: Dict[str, Any]) -> int:
        """Add a text entry with metadata to the store."""
        embedding = self._get_embedding(text)
        
        self.embeddings.append(embedding)
        entry_metadata = {
            "id": self.next_id,
            "text": text,
            **metadata
        }
        self.metadata.append(entry_metadata)
        
        entry_id = self.next_id
        self.next_id += 1
        return entry_id
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Search for similar entries using vector similarity."""
        if not self.embeddings:
            return []
        
        query_embedding = self._get_embedding(query)
        embeddings_array = np.array(self.embeddings)
        query_array = np.array(query_embedding).reshape(1, -1)
        
        # Compute cosine similarity
        similarities = np.dot(embeddings_array, query_array.T).flatten()
        
        # Get top k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only return positive similarities
                results.append((self.metadata[idx], float(similarities[idx])))
        
        return results
    
    def get(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """Get an entry by ID."""
        for meta in self.metadata:
            if meta.get("id") == entry_id:
                return meta
        return None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all entries."""
        return self.metadata.copy()
    
    def clear(self):
        """Clear all entries."""
        self.embeddings = []
        self.metadata = []
        self.next_id = 0
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        if self.model:
            try:
                embedding = self.model.encode(text, convert_to_numpy=True)
                return embedding.tolist()
            except Exception as e:
                print(f"Error generating embedding: {e}")
        
        # Fallback: random embedding
        return np.random.rand(self.dimension).tolist()
    
    def save(self, filepath: str):
        """Save vector store to disk."""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        data = {
            "embeddings": self.embeddings,
            "metadata": self.metadata,
            "next_id": self.next_id,
            "dimension": self.dimension
        }
        with open(filepath, "wb") as f:
            pickle.dump(data, f)
    
    def load(self, filepath: str):
        """Load vector store from disk."""
        if not os.path.exists(filepath):
            return
        
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        
        self.embeddings = data.get("embeddings", [])
        self.metadata = data.get("metadata", [])
        self.next_id = data.get("next_id", 0)
        self.dimension = data.get("dimension", self.dimension)

