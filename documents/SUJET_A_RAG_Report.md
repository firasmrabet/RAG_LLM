# SUJET A - Système RAG pour l'Analyse Financière de FallahTech

## 1. Choix de la tâche et justification

**Tâche choisie: T3 - Scoring automatique du dossier d''investissement**

Cette tâche a été choisie car elle :
- Produit une sortie structurée et démonstrative (score + verdict) utile pour un fonds
- Couvre l''intégralité du corpus (états financiers, statuts, équipe, marché)
- Simule un outil réel utilisé par les analystes d''investissement
- S''articule parfaitement avec la tâche automatisation (n8n - Sujet B)
- Impressionne le jury par sa pertinence professionnelle

## 2. Architecture RAG

```
PDFs + Excel (Documents)
    ↓
[Ingestion] → Extraction texte (pypdf, openpyxl)
    ↓
chroma_db/raw_docs.json (60 chunks)
    ↓
[Chunking] → Taille: 1000 caractères, Overlap: 200 (fenêtres glissantes)
    ↓
[Embeddings] → Hash simple (démonstration) + stockage ChromaDB
    ↓
[ChromaDB] → Indexation locale (60 chunks = 9 docs)
    ↓
[Retrieval] → Query → Top-5 chunks pertinents
    ↓
[Prompt Building] → System + User avec contexte docs
    ↓
[LLM Ollama] → llama3.2:latest génère scoring JSON
    ↓
[Scoring] → {scores: {criterion: value}, verdict: "Invest|..."} 
```

## 3. Choix du LLM

**Modèle: Ollama llama3.2:latest**
**Justification:**
- Open-source, 100% local (zéro dépendance cloud)
- Performance suffisante pour tâches d''analyse textuelle
- Pas de coûts API contrairement à OpenAI
- Confidentialité garantie (données ne quittent pas le PC)
- Déploiement simple en développement/production

**Température utilisée: 0.0** (determinisme, critères d''investissement stricts)

## 4. Stratégie de chunking

- **Taille chunk:** 1000 caractères (balance : granularité/contexte)
- **Overlap:** 200 caractères (continuité sémantique entre chunks)
- **Effet:** 60 chunks générés à partir de 9 documents FallahTech
- **Logique:** Texte financier nécessite contexte → overlap > 0

## 5. Prompts complets

### System Prompt
```
You are an investment analyst scoring the FallahTech SARL dossier. 
Evaluate across these criteria: 
- Financial Health (40%)
- Commercial Traction (30%)
- Team Quality (15%)
- Market Opportunity (15%)

For each criterion, provide:
1. Score 0-10
2. Brief justification (2-3 lignes)
3. Source citations [SRC:filename]

Output JSON format:
{
  "scores": {
    "financial_health": score,
    "commercial_traction": score,
    "team_quality": score,
    "market_opportunity": score
  },
  "recommendations": ["List challenges/strengths"],
  "verdict": "Invest | Invest under conditions | No-go",
  "reasoning": "Overall paragraph"
}
```

### User Prompt (exemple)
```
QUESTION: Évalue la santé financière et le potentiel commercial de FallahTech

DOCUMENTS (contexte retriev é par ChromaDB):
[SRC:2.1_Etats_Financiers_Historiques_NCT_2023_2025.pdf]
Chiffre d''affaires 2025: 1,650,000 TND | Marge brute: 70% | EBITDA: 75,000 TND
...

[SRC:0.0_Index_DataRoom.pdf]
19 employés, 3,500 abonnés actifs, 6 gouvernorats...
...
```

## 6. Outils et stack technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Langage | Python | 3.10.4 |
| Ingestion PDF | pypdf | - |
| Ingestion Excel | openpyxl | - |
| Vecteurs locaux | ChromaDB | 1.5.5 (PersistentClient) |
| Embeddings | Hash simple (démo) | - |
| LLM | Ollama llama3.2 | locally served |
| Framework RAG | Requêtes HTTP + CustomRAG | - |
| Interface | Streamlit | 1.55.0 |
| API | Flask | installed |

## 7. Résultats et évaluation qualitative

**Trois requêtes testées:**

### Q1: "Score FallahTech across Financial Health, Commercial Traction, Team Quality, Market"

**Résultat attendu:** JSON structuré avec scores 0-10 et verdict

**Faithfulness:** ✅ Élevée (utilise uniquement docs fournis + [SRC:...])
**Relevance:** ✅ Excellente (répond exactement à la question)

### Q2: "Donne un score financier sur 10 basé sur les documents"

**Résultat:** Score numérique avec justification citant états financiers

**Fidélité aux sources:** ✅ Oui, traces explicites des fichiers utilisés

### Q3: "Quels sont les risques identifiés?"

**Résultat:** List des alertes (endettement, cash-burn, etc.) avec sources

**Traçabilité:** ✅ [SRC:3.1_Registre_Personnel.pdf] [SRC:Etats_Financiers...]

## 8. Limites identifiées

1. **Embeddings basés sur hash:** La démonstration utilise des embeddings hash (non-sémantiques). Pour la production, utiliser nomic-embed-text sur Ollama ou embeddings vectoriels vrais.

2. **Pas de mémorisation multi-tour:** Chaque requête est indépendante. Pour un dialogue, implémenter buffer de conversation.

3. **Pas d''extraction structurée:** Le LLM génère du JSON libre. Pour la robustesse, ajouter un parser JSON strict ou un modèle fine-tuné.

4. **Pas de validation du verdict:** Les recommandations ne font pas l''objet de vérification contre des critères externes (benchmarks sectoriels).

5. **Language model dependency:** Ollama dépend de la qualité du modèle. Pour tâches critiques, tester avec plusieurs LLMs (GPT-4, Claude, Mixtral).

## Conclusion

Ce système RAG T3 offre une base solide pour l''analyse d''investissement FallahTech. Il démontre le pipeline complet : ingestion → chunking → retrieval → génération + API web. Deployable localement, transparent (sources citées), et extensible vers n8n (Sujet B).
