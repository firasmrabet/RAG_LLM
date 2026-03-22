"""
api.py — API Flask pour n8n (Sujet B) - GRATUITE
Expose le pipeline RAG via HTTP avec Ollama local
"""

import json
import os
from pathlib import Path
import requests
from flask import Flask, request, jsonify
import chromadb

ROOT        = Path(__file__).parent.parent
PERSIST_DIR = ROOT / "chroma_db"
COLLECTION  = "fallahtech_docs"
OLLAMA_URL  = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL= os.environ.get("OLLAMA_CHAT_MODEL", "llama2:latest")

app    = Flask(__name__)

SCORING_GRID = {
    "Santé Financière":      {"weight": 0.40, "query": "ratio financier marge trésorerie bilan résultat"},
    "Traction Commerciale":  {"weight": 0.30, "query": "chiffre affaires clients abonnements croissance"},
    "Qualité de l'Équipe":   {"weight": 0.15, "query": "équipe personnel CEO CTO fondateurs"},
    "Opportunité de Marché": {"weight": 0.15, "query": "marché AgriTech TAM SAM concurrence"},
}

SYSTEM_PROMPT = """Tu es un analyste financier senior. Évalue FallahTech.
Scores 0-10. Citations [SOURCE: fichier]. FORMAT JSON :
{"scores": {"Santé Financière": {"score": X, "justification": "...", "alertes": []}, ...},
 "score_global": X.X, "verdict": "...", "recommandation": "..."}"""

def retrieve(query, n=5):
    chroma = chromadb.PersistentClient(path=str(PERSIST_DIR))
    coll   = chroma.get_collection(COLLECTION)
    res    = coll.query(query_texts=[query], n_results=n,
                        include=["documents","metadatas","distances"])
    return [
        {"text": d, "source": m.get("source","?"),
         "relevance": round(1-dist, 3)}
        for d, m, dist in zip(
            res["documents"][0],
            res["metadatas"][0],
            res["distances"][0]
        )
    ]

# ── Endpoints ─────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "FallahTech RAG API"})

@app.route("/score", methods=["POST"])
def score():
    """Endpoint principal pour n8n — scoring complet"""
    try:
        sections = []
        for criterion, cfg in SCORING_GRID.items():
            items = retrieve(cfg["query"], n=4)
            section = f"## {criterion}\n"
            for item in items:
                section += f"[SOURCE: {item['source']}]\n{item['text']}\n\n"
            sections.append(section)

        context     = "\n".join(sections)
        user_prompt = f"Analyse FallahTech et produis le scoring JSON.\n\n{context}"

        url = f"{OLLAMA_URL}/api/chat"
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt}
            ],
            "temperature": 0.0,
            "stream": False
        }
        resp = requests.post(url, json=payload, timeout=300)
        result_data = resp.json()
        raw = result_data.get("message", {}).get("content", "{}")
        result = json.loads(raw)

        total = sum(
            result["scores"][c]["score"] * cfg["weight"]
            for c, cfg in SCORING_GRID.items()
        )
        result["score_global"] = round(total, 2)

        return jsonify({"status": "success", "result": result})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/ask", methods=["POST"])
def ask():
    """Endpoint Q&A pour n8n"""
    data     = request.json or {}
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "question manquante"}), 400

    try:
        items   = retrieve(question, n=4)
        context = "\n\n".join(
            f"[SOURCE: {i['source']}]\n{i['text']}" for i in items
        )
        
        url = f"{OLLAMA_URL}/api/chat"
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": "Expert FallahTech. Réponds en citant [SOURCE:]. Si absent, dis-le."},
                {"role": "user",   "content": f"Question: {question}\n\nDocs:\n{context}"}
            ],
            "temperature": 0.1,
            "stream": False
        }
        
        resp = requests.post(url, json=payload, timeout=300)
        result_data = resp.json()
        answer = result_data.get("message", {}).get("content", "")
        
        return jsonify({
            "status":   "success",
            "question": question,
            "answer":   answer,
            "sources":  [i["source"] for i in items]
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("🚀 API FallahTech démarrée sur http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
