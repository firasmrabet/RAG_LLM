# PROMPT COMPLET — Construire le Système RAG FallahTech avec Streamlit

## CONTEXTE DU PROJET

Tu dois construire un système RAG (Retrieval-Augmented Generation) complet pour l'analyse financière de **FallahTech SARL** — une startup AgriTech tunisienne basée à Sousse. FallahTech développe une application mobile d'assistance agricole en dialecte tunisien. Elle a 18 employés, 3500 abonnés actifs dans 6 gouvernorats, et dépose un dossier Série A auprès d'un fonds d'investissement franco-tunisien.

Ce projet est un mini-projet académique (ENISo — Module Technologie de Pointe) composé de deux sujets :
- **SUJET A** : Système RAG pour scoring automatique du dossier d'investissement (Tâche T3)
- **SUJET B** : Automatisation du même pipeline via n8n

---

## CORPUS DOCUMENTAIRE

Le dossier `documents/` contient les PDFs suivants (données fictives) :
- `0.0_Index_DataRoom.pdf` — Index du dossier
- `1.1_Statuts_FallahTech.pdf` — Statuts juridiques de la société
- `1.2_Contrat_Cooperative_Type.pdf` — Contrat coopérative type
- `2.1_Etats_Financiers_Historiques_NCT_2023_2025.pdf` — États financiers 2023-2025 (bilans, comptes de résultat, ratios)
- `3.1_Registre_Personnel.pdf` — Registre du personnel
- `4.1_Etude_Marche_Synthese.pdf` — Étude de marché AgriTech

**Données clés de FallahTech (2025) :**
- Chiffre d'affaires: 1 650 000 TND (+111,5% vs 2024)
- EBITDA: 75 000 TND
- Résultat net: 45 000 TND (première rentabilité)
- Marge brute: 70%
- Trésorerie fin 2025: 510 000 TND
- Dettes fournisseurs: 300 000 TND (×15 en un an — signal d'alerte)
- Ratio courant: 1,56 (vs 9,43 en 2024)
- Taux de rétention annuel: 82%
- Valorisation pré-money Série A: 12 000 000 TND pour 3 000 000 TND levés (20–25%)

### CONTENU COMPLET DE CHAQUE DOCUMENT

L'agent doit créer ces documents dans le dossier `documents/` pour que le pipeline RAG les ingère. Voici le contenu textuel de chaque document :

#### Document 1: `0.0_Index_DataRoom.pdf`
```
INDEX DE LA DATA ROOM FALLAHTECH
Dossier d'Investissement - Série A - Mise à jour : Mars 2025
1. Juridique
  1.1_Statuts_FallahTech.pdf : Statuts constitutifs de la société (SARL)
  1.2_Contrat_Cooperative_Type.pdf : Modèle de contrat de partenariat avec les coopératives agricoles
2. Financier
  2.1_Etats_Financiers_Historiques_NCT_2023_2025.pdf : Bilans, comptes de résultat et flux de trésorerie conformes aux NCT
  3.1_Business_Plan_Complet.xlsx : Modèle financier détaillé 2025-2028
3. Opérationnel
  3.1_Registre_Personnel.pdf : Liste des employés, salaires et organigramme
4. Commercial
  4.1_Etude_Marche_Synthese.pdf : Analyse du marché AgriTech au Maghreb, TAM/SAM/SOM et analyse concurrentielle
```

#### Document 2: `1.1_Statuts_FallahTech.pdf`
```
STATUTS DE LA SOCIÉTÉ FALLAHTECH SARL
Article 1 : Forme — SARL régie par la législation tunisienne
Article 2 : Objet — Développement et exploitation de solutions logicielles et d'IA appliquées à l'agriculture (AgriTech), conseil/formation/assistance aux agriculteurs, collecte et valorisation de données agricoles
Article 3 : Dénomination — FALLAHTECH SARL
Article 4 : Siège social — Pôle Technologique de Sousse, Novation City, 4054 Sousse, Tunisie
Article 5 : Durée — 99 années
Article 6 : Capital social — 100 000 TND, divisé en 10 000 parts de 10 TND
  - M. Sami BEN YOUSSEF (CEO) : 4 000 parts (40%)
  - Mme. Amira TRABELSI (CTO) : 3 500 parts (35%)
  - Seed Fund "AgriVentures TN" : 2 500 parts (25%)
Fait à Sousse, le 15 Janvier 2023.
```

#### Document 3: `1.2_Contrat_Cooperative_Type.pdf`
```
CONTRAT DE PARTENARIAT STRATÉGIQUE
ENTRE: FALLAHTECH SARL (M. Sami BEN YOUSSEF, "Le Prestataire")
ET: COOPÉRATIVE AGRICOLE "AL KHAYR" ("Le Partenaire")
Article 1 : Objet — Déploiement de solution d'assistance agricole intelligente
Article 2 : Engagements du Prestataire — Licences à tarif préférentiel (-30%), 4 sessions formation/an, tableau de bord agrégé
Article 3 : Engagements du Partenaire — Promotion auprès de 500 adhérents, collecte données agronomiques, centralisation facturation
Article 4 : Conditions financières — Commission de 15% sur le CA généré par les adhérents
Article 5 : Durée — 3 ans, renouvelable par tacite reconduction
```

#### Document 4: `2.1_Etats_Financiers_Historiques_NCT_2023_2025.pdf` (12 pages)
```
ÉTATS FINANCIERS HISTORIQUES (2023-2025) — Conformes aux NCT

COMPTES DE RÉSULTAT (TND):
                              2023        2024        2025
Ventes de services           350 000     780 000    1 650 000
  - Abonnements mensuels     280 000     630 000    1 350 000
  - Services complémentaires  70 000     150 000      300 000
TOTAL PRODUITS               350 000     780 000    1 650 000
Charges d'exploitation       450 000     850 000    1 575 000
  - Services externalisés    100 000     150 000      250 000
  - Infrastructure cloud      45 000      60 000      120 000
  - Charges de personnel     220 000     400 000      685 000
  - Marketing                 50 000     120 000      200 000
  - R&D                       55 000      80 000      150 000
  - Autres frais généraux     35 000      40 000       95 000
RÉSULTAT D'EXPLOITATION     -100 000     -70 000       75 000
RÉSULTAT NET                -100 000     -70 000       45 000

BILAN ACTIF (TND):           2023        2024        2025
Immobilisations              180 000     250 000      320 000
  - Logiciels/développements 120 000     180 000      250 000
  - Matériel informatique     45 000      55 000       60 000
Actif courant                170 000     450 000      750 000
  - Créances clients          50 000     100 000      180 000
  - Disponibilités           100 000     330 000      510 000
TOTAL ACTIF                  350 000     700 000    1 070 000

BILAN PASSIF (TND):          2023        2024        2025
Capitaux propres             400 000     640 000      685 000
  - Capital social           500 000     500 000      500 000
  - Résultat exercice       -100 000     -70 000       45 000
Passif courant              -50 000      60 000      385 000
  - Dettes fournisseurs           0      20 000      300 000
  - Dettes fiscales/sociales      0      25 000      60 000
TOTAL PASSIF                 350 000     700 000    1 070 000

RATIOS FINANCIERS:           2023        2024        2025
Marge brute                   50%         65%         70%
Marge d'exploitation        -28.6%       -9.0%        4.5%
Marge nette                 -28.6%       -9.0%        2.7%
Ratio courant (AC/PC)         —           9.43        1.56
Croissance CA                 —          122.9%      111.5%
Trésorerie fin de période   100 000     330 000      510 000

NOTES EXPLICATIVES:
- 2025 = première rentabilité (résultat net positif 45 000 TND)
- Croissance revenus: +111.5% (1.65M TND vs 780k TND en 2024)
- Trésorerie positive: 510 000 TND (vs 330 000 TND en 2024)
- ALERTE: Dettes fournisseurs ×15 en 1 an (20 000 → 300 000 TND)
- ALERTE: Ratio courant en forte baisse (9.43 → 1.56)
- 18 employés, masse salariale 685 000 TND
- Contrats avec 6 coopératives agricoles
```

#### Document 5: `3.1_Registre_Personnel.pdf`
```
REGISTRE DU PERSONNEL - FALLAHTECH (Décembre 2025)
ID  Département   Poste                    Date Embauche  Salaire Annuel Brut (TND)
01  Direction     CEO                      Jan-23         72 000
02  Tech          CTO                      Jan-23         65 000
03  Opérations    Head of Field Ops        Mar-23         48 000
04  Tech          Senior Backend Dev       Juin-23        42 000
05  Tech          Mobile Dev (Android)     Sep-23         38 000
06  Tech          Mobile Dev (iOS)         Sep-23         38 000
07  Agro          Lead Agronome            Jan-24         40 000
08  Sales         Field Sales Rep (Nord)   Fév-24         28 000 + Var
09  Sales         Field Sales Rep (Centre) Fév-24         28 000 + Var
10  Tech          Data Scientist           Avr-24         45 000
11  Agro          Agronome Junior          Juin-24        30 000
12  Tech          UI/UX Designer           Sep-24         35 000
13  Tech          QA Engineer              Nov-24         32 000
14  Sales         Field Sales Rep (Cap Bon) Jan-25        28 000 + Var
15  Sales         Field Sales Rep (Sud)    Mar-25         28 000 + Var
16  Agro          Agronome Junior          Mai-25         30 000
17  Agro          Agronome Junior          Sep-25         30 000
18  Sales         Customer Success Agent   Oct-25         28 000
Total Effectif: 18 employés — Masse Salariale Annuelle (hors variables): 655 000 TND
```

#### Document 6: `4.1_Etude_Marche_Synthese.pdf`
```
SYNTHÈSE: ÉTUDE DE MARCHÉ AGRITECH MAGHREB
1. Marché Tunisien (Marché Domestique)
  - TAM: 500 000 exploitations agricoles
  - SAM: 120 000 exploitations (connectivité smartphone + cultures adaptées)
  - Part de marché actuelle: ~3% du SAM
  - Concurrence: Faible. Principalement initiatives étatiques (Vulgarisation) ou solutions européennes non adaptées linguistiquement.

2. Opportunité d'Expansion (Algérie & Maroc)
  - Algérie: 1.2 million d'exploitations, fort soutien étatique, adaptation dialecte "Darja" (~70% similaire tunisien)
  - Maroc: 1.5 million d'exploitations, marché le plus mature d'Afrique du Nord, Plan "Génération Green", dialecte "Darija"

3. Positionnement Prix
  - FallahTech: 35-50 TND/mois (très accessible pour petit exploitant)
  - Solutions importées (xFarm, Cropin): >200 TND/mois (cible grands domaines)
  - Avantage compétitif: ROI pour l'agriculteur estimé à 3 mois grâce aux économies d'eau et d'intrants
```

**IMPORTANT:** L'agent doit créer ces documents en tant que texte dans les PDFs (ou directement utiliser le contenu pour le chunking). Les chiffres ci-dessus sont les données exactes que le RAG doit retrouver et citer.

---

## ARCHITECTURE TECHNIQUE REQUISE

### Stack technique
- **Python 3.10+**
- **Streamlit** — Interface utilisateur (dashboard interactif)
- **ChromaDB** — Base vectorielle locale (PersistentClient, collection `fallahtech_docs_nomic`)
- **Sentence-Transformers** — Embeddings (modèle `all-MiniLM-L6-v2`, 384 dimensions)
- **Groq API** — LLM cloud gratuit (modèle principal: `llama-3.1-70b-versatile`, fallbacks: `llama-3.1-8b-instant`, `mixtral-8x7b-32768`)
- **Plotly** — Graphiques (barres + jauge)
- **pypdf + openpyxl** — Ingestion documents
- **python-dotenv** — Gestion variables d'environnement

### Pipeline RAG (7 étapes)
```
PDF/XLSX → Ingestion (ingest.py) → Chunking 1000 chars / 200 overlap (embeddings.py)
→ Embeddings Nomic 384-dim (embeddings_nomic.py) → ChromaDB PersistentClient
→ Retrieval sémantique top-K chunks → Prompt building → LLM Groq → Réponse structurée avec citations
```

### Paramètres de chunking (CONFORME À L'ÉNONCÉ)
- **Taille chunk**: 1000 caractères
- **Overlap**: 200 caractères (fenêtre glissante)
- **Justification**: Documents financiers nécessitent contexte étendu, overlap 20% assure continuité sémantique

---

## FICHIERS À CRÉER

### 1. `src/ingest.py` — Ingestion des documents
- Lire tous les PDFs du dossier `documents/` avec pypdf
- Lire les fichiers Excel avec openpyxl
- Sauvegarder le texte brut dans `chroma_db/raw_docs.json`

### 2. `src/embeddings.py` — Chunking + Embeddings
- Chunking avec CHUNK_SIZE=1000 et CHUNK_OVERLAP=200 (fenêtre glissante)
- Embeddings via sentence-transformers `all-MiniLM-L6-v2` (384-dim, gratuit, offline)
- Stockage dans ChromaDB collection `fallahtech_docs` avec métadonnées (source, chunk_index)

### 3. `src/embeddings_nomic.py` — Migration embeddings professionnels
- Créer collection `fallahtech_docs_nomic` avec embeddings Nomic (all-MiniLM-L6-v2)
- Migrer depuis raw_docs.json

### 4. `src/rag_scoring_groq.py` — Scoring avec Groq LLM
- Classe `GroqRAGScorer` avec:
  - `retrieve_rich_context(query, num_chunks=7)` — retrieval ChromaDB
  - `score_with_groq(criterion, context)` — scoring via Groq API, température 0.1
  - `fallback_score(criterion)` — scoring déterministe si Groq échoue
  - `run_complete_evaluation()` — évaluation complète 3 critères
- 3 critères pondérés:
  - Santé Financière (60%)
  - Traction Commerciale (25%)
  - Opportunité de Marché (15%)
- Sauvegarde résultats dans `scoring_result_groq.json`

### 5. `src/api.py` — API Flask pour n8n (Sujet B)
- Endpoints: `/health` (GET), `/score` (POST), `/ask` (POST)
- Pipeline RAG identique au scoring Groq

### 6. `src/dashboard.py` — Dashboard Streamlit (FICHIER PRINCIPAL)

C'est le fichier le plus important. Voici les spécifications détaillées :

#### Configuration Streamlit
```python
st.set_page_config(
    page_title="FallahTech Investment Evaluation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

#### Classe `DashboardApp`
Utiliser `@st.cache_resource` pour cacher ChromaDB et Groq clients (évite rechargement lent).

#### Sidebar Configuration
- Radio: Mode d'Évaluation (Professionnel Groq LLM / Déterministe Rapide)
- Slider: Chunks par critère (3-10, défaut 7)
- Info: Versions disponibles (Nomic vs Hash-based)
- Info: Type d'embeddings actuel

#### Tab 1: "📊 Évaluation Standard"
- Bouton "🚀 Lancer l'Évaluation"
- 3 critères évalués avec scoring LLM:
  - Santé Financière (query: revenus, marges, trésorerie, solvabilité) — poids 60%
  - Traction Commerciale (query: croissance, clients, adoption, rétention) — poids 25%
  - Opportunité de Marché (query: TAM, croissance marché, concurrence) — poids 15%
- Pour chaque critère: afficher score /10, analyse complète, métadonnées (poids, source, chunks)
- Section Résumé avec:
  - Score final pondéré dans une box gradient
  - Verdict automatique (≥7.5 EXCELLENT / ≥6.5 BON / ≥5.0 PASSABLE / ≥3.5 FAIBLE / <3.5 TRÈS FAIBLE)
  - Graphique barres Plotly (scores par critère)
  - Graphique jauge Plotly (score global)
  - Tableau détaillé (critère, score, poids, contribution, source)
  - Export JSON + TXT

#### Tab 2: "❓ Question Custom"
- Afficher le nombre de chunks configuré
- TextArea pour question libre
- Bouton "🔍 Analyser"

**SYSTEM PROMPT ANTI-HALLUCINATION (CRITIQUE) :**
```
Tu es un analyste financier senior d'un fonds d'investissement franco-tunisien.
Tu analyses le dossier de FallahTech SARL — une startup AgriTech tunisienne basée à Sousse.
FallahTech développe une application mobile d'assistance agricole en dialecte tunisien.
Elle a 18 employés et 3500 abonnés actifs dans 6 gouvernorats tunisiens.

RÈGLES ABSOLUES:
1. Tu ne dois JAMAIS inventer de données, chiffres ou faits.
2. Utilise UNIQUEMENT les informations présentes dans les DOCUMENTS FOURNIS.
3. Si une information n'est pas dans les documents, dis: "Cette information n'est pas disponible dans le corpus documentaire."
4. Cite TOUJOURS le nom exact du document source: [SOURCE: nom_du_fichier.pdf]
5. Sois QUANTITATIF: cite les montants exacts en TND, les pourcentages, les ratios.
6. FallahTech est une entreprise AgriTech/AgriFood, PAS une entreprise de télécommunications.
7. Ne confonds JAMAIS les données de différents documents.
8. Réponds en français professionnel.
```

**Paramètres LLM pour Q&A :**
- Température: **0.1** (strict, anti-hallucination)
- max_tokens: **1500** (réponses complètes)
- top_p: 0.9
- Modèles (cascade): llama-3.1-70b-versatile → llama-3.1-8b-instant → mixtral-8x7b-32768

**Format réponse obligatoire :**
```
===== RÉPONSE =====
[Réponse professionnelle structurée, minimum 200 mots, chaque paragraphe cite sa source]

===== SOURCES =====
[Liste numérotée des documents utilisés]

===== CONFIANCE =====
[Élevée/Modérée/Basse — justification]
```

**Affichage résultat :**
- Barre métadonnées: modèle utilisé, nombre de chunks, température
- Réponse détaillée (colonne principale)
- Niveau de confiance (badge coloré: vert/orange/rouge)
- Sources citées (info box)
- Expander "Contexte récupéré (N chunks de ChromaDB)" — montre le contexte brut
- Bouton télécharger réponse JSON

#### Styling CSS
```css
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px; border-radius: 10px; color: white; text-align: center;
}
.verdict-excellent { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.verdict-good { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.verdict-passable { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
.verdict-weak { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
```

### 7. `src/n8n_workflow.json` — Workflow n8n (Sujet B)
Workflow exporté de n8n avec 8 nœuds:
1. Manual Trigger
2. Check API Health (GET /api/health via Ngrok)
3. Get Available Documents (GET /api/documents via Ngrok)
4. Combine Health & Documents (Merge)
5. RAG Analysis (POST /api/webhook/analyze via Ngrok)
6. Debug RAG Output (Set — agrège résultats)
7. Format JSON Response (Code JavaScript)
8. Return Response (Respond to Webhook)

### 8. `generate_pdf_reports.py` — Générateur PDFs livrables
Génère deux PDFs (Times New Roman 11pt, interligne 1.15, 3-4 pages):
- `SUJET_A_RAG_Report.pdf` — 8 sections (tâche, architecture, LLM, chunking, prompts, stack, résultats, limites)
- `SUJET_B_n8n_Report.pdf` — 8 sections (tâche, workflow, LLM, prompts, déploiement, JSON, démonstration, limites)

### 9. `.env` — Variables d'environnement
```
GROQ_API_KEY=gsk_votre_clé_groq_ici
```

### 10. `.streamlit/config.toml` — Thème Streamlit
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#1a1f2e"
textColor = "#fafafa"
```

---

## EXIGENCES DE L'ÉNONCÉ (OBLIGATOIRE)

### Sujet A — Livrable PDF (3-4 pages)
1. Choix de la tâche (T3) et justification
2. Architecture RAG: schéma de la chaîne (ingestion → chunking → embedding → retrieval → génération)
3. Choix du LLM: modèle, version, justification (performance, coût, confidentialité), température
4. Stratégie de chunking: taille 1000, overlap 200, logique documents financiers
5. Prompts complets: system prompt et user prompt exacts
6. Stack technique: framework, base vectorielle, modèle d'embedding
7. Résultats: trois questions testées avec réponses et évaluation qualitative
8. Limites identifiées

### Sujet B — Livrable PDF + JSON
1. Tâche automatisée et lien avec SUJET A
2. Schéma du workflow: capture d'écran annotée, description fonctionnelle de chaque nœud
3. Choix du LLM: modèle, justification, paramètres (température, max_tokens)
4. Prompts utilisés dans les nœuds LLM
5. Détails de déploiement: n8n cloud/self-hosted, credentials, clés API
6. Fichier .json du workflow exporté de n8n
7. Démonstration: capture d'écran ou vidéo d'une exécution
8. Limites identifiées et pistes d'amélioration

### Exigences communes
- Justification du LLM (modèle exact, version, motif du choix)
- Prompts complets (pas de descriptions vagues)
- Niveau de confidentialité (FallahTech est fictive → cloud OK)
- Format PDF: 3 pages minimum, 4 pages maximum, Times New Roman 11pt, interligne 1,15

---

## COMMENT LANCER

```bash
# 1. Installer les dépendances
pip install streamlit chromadb sentence-transformers groq plotly python-dotenv pypdf openpyxl reportlab flask

# 2. Configurer la clé API Groq (gratuite: https://console.groq.com)
echo "GROQ_API_KEY=gsk_..." > .env

# 3. Ingestion des documents
python src/ingest.py

# 4. Chunking + Embeddings
python src/embeddings.py

# 5. Migration Nomic
python src/embeddings_nomic.py

# 6. Lancer le dashboard
streamlit run src/dashboard.py --server.port 8504

# 7. Générer les PDFs livrables
python generate_pdf_reports.py
```
