# SUJET B - Automatisation du Scoring FallahTech avec n8n

## 1. Tâche automatisée et lien avec Sujet A

Le workflow n8n automatise la même tâche T3 que le Sujet A (Scoring d''investissement structuré).

**Flux complet :**
```
Webhook Trigger → Lire documents → Chunker → Embeddings (Chroma)
    ↓
Scoring RAG (via API Python Flask) → Formater rapport → Email rapport
```

**Sujet A:** Implémentation manuelle du pipeline RAG (Python + ChromaDB + Ollama)
**Sujet B:** Orchestration automatisée du même pipeline (n8n + HTTP calls + Export PDF)

## 2. Schéma du workflow n8n

```
┌─────────────────┐
│ 1. Webhook      │ Récoit requête POST /fallahtech-scoring
│ Trigger         │
└────────┬────────┘
         │
┌────────v────────┐
│ 2. Read Docs    │ Lit PDFs/XLSX depuis dossier documents/
│ (Local Files)   │
└────────┬────────┘
         │
┌────────v────────┐
│ 3. Chunk Text   │ Divise en chunks (1000 chars, overlap=200)
│ (Function)      │ Accumule data pour retrieval
└────────┬────────┘
         │
┌────────v────────────────┐
│ 4. Call API /embeddings │ POST à Flask API
│ (HTTP Request)          │ Prépare ChromaDB + Embeddings
└────────┬────────────────┘
         │
┌────────v────────────┐
│ 5. Call API /score  │ POST query → LLM Ollama scoring
│ (HTTP Request)      │ Retour JSON avec scores + verdict
└────────┬───────────── ┘
         │
┌────────v────────┐
│ 6. Format PDF   │ FOrmate JSON en rapport PDF structuré
│ (Function)      │ Template: FallahTech_Report_YYYY-MM-DD.pdf
└────────┬────────┘
         │
┌────────v────────┐
│ 7. Send Email   │ Envoie PDF à stakeholder email
│ (Email)         │ CC: investor@fonds.tn
└─────────────────┘
```

## 3. Choix du LLM

**Modèle:** Ollama llama3.2:latest (même que Sujet A)
**Justification:** Open-source, performances acceptables, zéro coûts API, déploiement local

**Paramètres utilisés:**
- Temperature: 0.0 (determinisme strict pour scoring)
- max_tokens: 2000 (espace pour JSON + verbose)
- model: llama3.2:latest

## 4. Prompts utilisés dans les nœuds LLM

### Nœud "Score RAG" (Nœud 5)

**System Prompt:**
```
You are an expert investment analyst. Score the FallahTech SARL dossier using criteria:
- Financial Health (40%)
- Commercial Traction (30%)
- Team Quality (15%)
- Market Opportunity (15%)

Return VALID JSON only (no markdown, no extra text).
```

**User Prompt (dynamique de ChromaDB retrieval):**
```
Score FallahTech based on these documents:

[SRC:filename1]
<chunk_1_text>

[SRC:filename2]
<chunk_2_text>

Return JSON: {scores: {...}, verdict: string, reasoning: string}
```

## 5. Détails de déploiement

### Option A: n8n Self-Hosted (Local Docker)

```bash
# 1. Installer Docker + Docker Compose
# (instructions spécifiques à l''OS)

# 2. Créer docker-compose.yml:
version: '3'
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: fallahtech-n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - DB_TYPE=sqlite
    volumes:
      - ./n8n_data:/home/node/.n8n

# 3. Lancer
docker-compose up -d

# 4. Accéder: http://localhost:5678
```

### Option B: n8n Cloud (SaaS)

```
1. S''inscrire sur https://app.n8n.cloud
2. Créer nouveau workflow
3. Importer JSON depuis: src/n8n_workflow.json
4. Configurer credentials:
   - Flask API URL: http://fallahtech-api:5000
   - Email service: Gmail/SendGrid
```

### Gestion des credentials

**Variables d''environnement (sécurisées dans n8n):**
```
- PYTHON_API_URL: http://127.0.0.1:5000
- INVESTOR_EMAIL: analyst@fund.tn
- OLLAMA_URL: http://127.0.0.1:11434
- SMTP_PASSWORD: (secrets n8n)
```

**Sécurisation des clés API:**
- n8n offre Vault pour credentials
- Ne jamais commiter secrets en code source
- Utiliser environnement variables ou n8n Credentials Manager

## 6. Fichier .json du workflow

**Location:** `src/n8n_workflow.json`

**Nodes:**
1. **webhook-trigger** → Écoute POST requests
2. **file-read** → Lit documents locaux
3. **chunk-docs** → Divise en chunks (Function node)
4. **embed-chroma** → Appel API /embeddings
5. **score-rag** → Appel API /score (scoring principal)
6. **format-report** → Crée rapport structuré
7. **send-email** → Envoie PDF par email

**Imports disponibles:**
- À importer via n8n UI: "Import Workflow" → Upload JSON
- Ou via CLI: `n8n import --workflow src/n8n_workflow.json`

## 7. Démonstration (Capture d''écran / Scénario)

### Scénario d''exécution complet:

**Déclenchement:** Investisseur demande analyse FallahTech
```bash
curl -X POST http://localhost:5678/webhook/fallahtech-scoring \
  -H "Content-Type: application/json" \
  -d '{"investor": "Fonds_XYZ", "date": "2026-03-20"}'
```

**Résulté attendu dans 2-3 minutes:**
```
✅ 1. Webhook reçoit requête
✅ 2. PDFs lus (9 documents)
✅ 3. 60 chunks créés + indexés
✅ 4. ChromaDB embeddings stockés
✅ 5. LLM génère scoring JSON:
   {
     "scores": {
       "financial_health": 7.5,
       "commercial_traction": 8.0,
       "team_quality": 8.5,
       "market_opportunity": 7.0
     },
     "verdict": "Invest under conditions",
     "reasoning": "Solide croissance mais CA/charges à surveiller..."
   }
✅ 6. Rapport PDF généré: FallahTech_Scoring_2026-03-20.pdf
✅ 7. Email envoyé à analyst@fund.tn avec rapport attaché
✅ Workflow terminé en ~180 secondes
```

### Étapes visuelles (n8n UI):
- Nœud 1 (Webhook): "1 request received"
- Nœud 5 (Score): "Response: 200 OK" (JSON)
- Nœud 7 (Email): "Email sent successfully"

## 8. Limites et améliorations futures

### Limites actuelles:
1. **Pas de redirection d''erreurs:** Si LLM échoue, workflow s''arrêt. Ajouter "Error Workflow".
2. **Pas de retry logic:** Timeout Ollama → échec. Implémenter exponential backoff.
3. **PDF generation:** n8n n''a pas de nœud PDF natif. Utiliser externe (like wkhtmltopdf) ou templating.
4. **Pas de dashboard:** Résultats non centralisés. Ajouter nœud Database pour historique scores.

### Améliorations recommandées:
- **Ajout d''alertes:** Si score < 5 → Slack/Teams notification
- **Historique:** Stocker scores dans PostgreSQL → Dashboard analytique
- **Paramétrage:** Permettre tuning critères pondérés via UI
- **Multi-documents:** Supporter upload dynamique de documents zip
- **Rapports comparatifs:** N8N loope sur plusieurs startups → rapport comparatif

## Conclusion

Ce workflow n8n offre une solution end-to-end d''automatisation du scoring d''investissement. Intégré avec le pipeline RAG Python (Sujet A), il fournit une chaîne complète: ingest → score → report → distribution. Déployable en self-hosted ou cloud, scalable, et prêt pour production.
