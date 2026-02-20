"""
RAG (Retrieval Augmented Generation) System
Manages embeddings, FAISS indexing, and chunk retrieval
"""
import numpy as np
import pickle
import os
from typing import List, Tuple, Dict
import faiss
from config import (
    FAISS_INDEX_PATH,
    METADATA_PATH,
    EMBEDDING_MODEL,
    TOP_K_CHUNKS,
    OPENAI_API_KEY,
)

# Try to import SentenceTransformer; fall back to OpenAI embeddings if unavailable
try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

# Lazy import OpenAI when needed to avoid heavy imports at module load
OpenAI = None

class RAGSystem:
    def __init__(self, embedding_model_name: str = EMBEDDING_MODEL):
        self.embedding_model = None
        self.openai_client = None
        self.use_openai = False

        if SentenceTransformer is not None:
            try:
                self.embedding_model = SentenceTransformer(embedding_model_name)
            except Exception:
                self.embedding_model = None

        # If local sentence-transformers unavailable, use OpenAI embeddings
        if self.embedding_model is None:
            try:
                from openai import OpenAI as _OpenAI
            except Exception:
                _OpenAI = None

            if _OpenAI is None:
                raise ImportError(
                    "Neither sentence-transformers nor openai client is available."
                )
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set and no local embedding model available.")
            self.openai_client = _OpenAI(api_key=OPENAI_API_KEY)
            self.use_openai = True
        self.index = None
        self.metadata = []
        self.chunks = []
        
    def build_index(self, chunks: List[Tuple[str, Dict]]) -> None:
        """
        Build FAISS index from chunks
        chunks: List of (text, metadata) tuples
        """
        print(f"Building FAISS index from {len(chunks)} chunks...")
        
        self.chunks = chunks
        texts = [chunk[0] for chunk in chunks]
        self.metadata = [chunk[1] for chunk in chunks]
        
        # Generate embeddings
        if not self.use_openai:
            embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
            embeddings = np.array(embeddings).astype('float32')
        else:
            # Use OpenAI embeddings API
            resp = self.openai_client.embeddings.create(model="text-embedding-3-small", input=texts)
            embeddings = [r.embedding for r in resp.data]
            embeddings = np.array(embeddings).astype('float32')
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        print(f"✓ Index built with {self.index.ntotal} vectors")
        
    def save_index(self, index_path: str = FAISS_INDEX_PATH) -> None:
        """Save FAISS index and metadata to disk"""
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        faiss.write_index(self.index, index_path)
        with open(METADATA_PATH, 'wb') as f:
            pickle.dump({
                'metadata': self.metadata,
                'chunks': self.chunks
            }, f)
        
        print(f"✓ Index saved to {index_path}")
        
    def load_index(self, index_path: str = FAISS_INDEX_PATH) -> bool:
        """Load FAISS index and metadata from disk"""
        if not os.path.exists(index_path) or not os.path.exists(METADATA_PATH):
            return False
        
        try:
            self.index = faiss.read_index(index_path)
            with open(METADATA_PATH, 'rb') as f:
                data = pickle.load(f)
                self.metadata = data['metadata']
                self.chunks = data['chunks']
            
            print(f"✓ Index loaded from {index_path}")
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def retrieve_context(self, query: str, k: int = TOP_K_CHUNKS) -> List[Dict]:
        """
        Retrieve top-k relevant chunks for a query
        Returns: List of (chunk_text, metadata, similarity_score)
        """
        if self.index is None:
            raise ValueError("Index not initialized. Call build_index() first.")
        
        # Encode query
        if not self.use_openai:
            query_embedding = self.embedding_model.encode([query])[0].astype('float32').reshape(1, -1)
        else:
            resp = self.openai_client.embeddings.create(model="text-embedding-3-small", input=[query])
            query_embedding = np.array(resp.data[0].embedding).astype('float32').reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
        
        # Format results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx == -1:  # Invalid index
                continue
            
            result = {
                'text': self.chunks[idx][0],
                'metadata': self.metadata[idx],
                'similarity_score': float(1 / (1 + distance)),  # Convert L2 distance to similarity
                'rank': i + 1
            }
            results.append(result)
        
        return results

    def retrieve_by_role(self, role: str, query: str = None, k: int = TOP_K_CHUNKS) -> List[Dict]:
        """
        Retrieve context filtered by role
        """
        if query is None:
            query = role
        
        all_results = self.retrieve_context(query, k * 2)
        
        # Filter by role
        role_results = [
            r for r in all_results 
            if r['metadata'].get('role', '').lower() == role.lower()
        ]
        
        return role_results[:k]
