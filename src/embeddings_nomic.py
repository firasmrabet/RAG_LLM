# -*- coding: utf-8 -*-
"""
Phase 1: Professional Embeddings using Nomic AI
Replaces hash-based embeddings with production-grade sentence transformers
"""

from sentence_transformers import SentenceTransformer
import json
import os
from chromadb.config import Settings
import chromadb

class NomicEmbeddingManager:
    """Professional embedding manager using sentence-transformers"""
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize nomic embeddings
        
        Args:
            model_name: HuggingFace sentence-transformer model
                - "all-MiniLM-L6-v2": Lightweight (384-dim), fast, good quality
                - "multi-qa-MiniLM-L6-cos-v1": Optimized for Q&A (384-dim)
                - "all-mpnet-base-v2": Larger (768-dim), better quality but slower
        """
        print(f"📥 Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print(f"✅ Model loaded: {self.model.get_sentence_embedding_dimension()}-dimensional")
    
    def embed_text(self, text: str) -> list:
        """Convert text to embedding vector"""
        return self.model.encode(text, convert_to_numpy=True).tolist()
    
    def embed_batch(self, texts: list) -> list:
        """Convert batch of texts to embedding vectors"""
        return self.model.encode(texts, convert_to_numpy=True).tolist()


def migrate_chromadb_to_nomic():
    """
    Migrate existing ChromaDB from hash-based to professional nomic embeddings
    This creates a fresh collection with proper embeddings
    """
    print("\n" + "="*60)
    print("PHASE 1: MIGRATING TO PROFESSIONAL EMBEDDINGS")
    print("="*60)
    
    # Initialize embedding manager
    embedder = NomicEmbeddingManager(model_name="all-MiniLM-L6-v2")
    
    # Load raw documents
    raw_docs_path = "chroma_db/raw_docs.json"
    if not os.path.exists(raw_docs_path):
        print("❌ raw_docs.json not found! Run ingest.py first.")
        return
    
    with open(raw_docs_path, 'r', encoding='utf-8') as f:
        raw_docs = json.load(f)
    
    print(f"\n📚 Loaded {len(raw_docs)} document chunks from raw_docs.json")
    
    # Initialize ChromaDB with professional settings
    chroma_path = "chroma_db"
    
    # Create fresh collection with custom embedding function
    client = chromadb.PersistentClient(path=chroma_path)
    
    # Remove old collection if exists
    try:
        client.delete_collection(name="fallahtech_docs_nomic")
        print("🗑️  Cleared old collection")
    except:
        pass
    
    # Create collection with nomic embeddings
    collection = client.get_or_create_collection(
        name="fallahtech_docs_nomic",
        metadata={"hnsw:space": "cosine"}
    )
    
    print("\n🔄 Re-embedding documents with Nomic professional embeddings...")
    
    # Prepare documents and embeddings
    ids = []
    embeddings = []
    documents = []
    metadatas = []
    
    for i, doc in enumerate(raw_docs):
        doc_id = f"doc_{i}"
        text = doc.get("content", "")
        source = doc.get("source", "unknown")
        
        # Generate nomic embedding
        embedding = embedder.embed_text(text)
        
        ids.append(doc_id)
        embeddings.append(embedding)
        documents.append(text)
        metadatas.append({
            "source": source,
            "chunk_index": str(i)
        })
        
        if (i + 1) % 10 == 0:
            print(f"  ✓ Embedded {i + 1}/{len(raw_docs)} chunks")
    
    # Add to collection
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    
    print(f"\n✅ Successfully migrated {len(raw_docs)} chunks to ChromaDB with Nomic embeddings!")
    print(f"📊 Embedding dimension: {len(embeddings[0])} (vs hash-based: 384)")
    print(f"🎯 Collection: fallahtech_docs_nomic")
    
    # Save migration info
    migration_info = {
        "model": "all-MiniLM-L6-v2",
        "dimension": len(embeddings[0]),
        "chunks_migrated": len(raw_docs),
        "collection_name": "fallahtech_docs_nomic",
        "status": "completed"
    }
    
    with open("chroma_db/migration_nomic.json", 'w', encoding='utf-8') as f:
        json.dump(migration_info, f, indent=2, ensure_ascii=False)
    
    print("\n💾 Migration info saved to: chroma_db/migration_nomic.json")
    
    return collection, embedder


if __name__ == "__main__":
    migrate_chromadb_to_nomic()
