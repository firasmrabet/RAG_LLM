"""
embeddings.py — Phase 2 : Chunking + Embeddings Gratuits + ChromaDB
Lit raw_docs.json, découpe en chunks, crée les vrais embeddings
via sentence-transformers (libre & gratuit) et les stocke dans ChromaDB
"""

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

# ── Config ────────────────────────────────────────────────
ROOT         = Path(__file__).parent.parent
RAW_DOCS     = ROOT / "chroma_db" / "raw_docs.json"
PERSIST_DIR  = ROOT / "chroma_db"
EMBED_MODEL  = "all-MiniLM-L6-v2"  # Modèle léger gratuit Hugging Face
CHUNK_SIZE   = 1000  # Conforme à l'énoncé: 1000 caractères
CHUNK_OVERLAP= 200   # Conforme à l'énoncé: 200 caractères overlap
COLLECTION   = "fallahtech_docs"

# Charger le modèle sentence-transformers une seule fois
print("📦 Chargement du modèle d'embeddings...")
embedder = SentenceTransformer(EMBED_MODEL)

# ── Chunking ──────────────────────────────────────────────
def chunk_text(text: str, size: int = CHUNK_SIZE,
               overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Découpe le texte en chunks de taille fixe avec overlap.
    CONFORME ÉNONCÉ:
    - Taille: 1000 caractères (balance granularité/contexte pour texte financier)
    - Overlap: 200 caractères (~20% chevauchement) pour continuité sémantique
    
    Logique fenêtres glissantes = continuité entre chunks
    Contexte préservé pour analyse cross-critères (marges + revenus, etc.)
    """
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        start = end - overlap if end - overlap > start else end
    return chunks

# ── Embeddings Libre (sentence-transformers) ──────────────────────
def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Crée les embeddings gratuitement avec sentence-transformers.
    Pas de limite de quota, fonctionne hors-ligne.
    """
    print(f"  🔢 Création de {len(texts)} embeddings (gratuit)...")
    vectors = embedder.encode(texts, show_progress_bar=True)
    return vectors.tolist()

# ── Stockage ChromaDB ─────────────────────────────────────
def store_in_chroma(texts, metadatas, ids, embeddings):
    chroma = chromadb.PersistentClient(path=str(PERSIST_DIR))

    # Supprime la collection si elle existe déjà
    try:
        chroma.delete_collection(COLLECTION)
        print("  🗑️  Ancienne collection supprimée")
    except Exception:
        pass

    coll = chroma.create_collection(
        name     = COLLECTION,
        metadata = {"hnsw:space": "cosine"}
    )
    coll.add(
        ids        = ids,
        documents  = texts,
        metadatas  = metadatas,
        embeddings = embeddings
    )
    print(f"  ✅ {len(ids)} chunks stockés dans ChromaDB")

# ── Pipeline principal ────────────────────────────────────
def build_vectorstore():
    if not RAW_DOCS.exists():
        print("❌ raw_docs.json introuvable. Lance d'abord ingest.py")
        return

    with open(RAW_DOCS, "r", encoding="utf-8") as f:
        docs = json.load(f)

    print(f"📄 {len(docs)} documents chargés\n")

    texts, metadatas, ids = [], [], []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['id']}_chunk_{i}"
            texts.append(chunk)
            metadatas.append({
                "source"  : doc["source"],
                "doc_id"  : doc["id"],
                "chunk"   : i,
                "total"   : len(chunks)
            })
            ids.append(chunk_id)

    print(f"📦 {len(texts)} chunks créés\n")
    print("🔢 Création des embeddings OpenAI...\n")

    embeddings = get_embeddings(texts)

    print("\n💾 Stockage dans ChromaDB...\n")
    store_in_chroma(texts, metadatas, ids, embeddings)

    print(f"\n✅ VectorStore prêt ! "
          f"{len(texts)} chunks indexés.")

if __name__ == "__main__":
    build_vectorstore()
