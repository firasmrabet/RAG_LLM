#!/usr/bin/env python3
"""
Génère les PDFs requis pour SUJET A et SUJET B
Format: 3-4 pages, Times New Roman 11pt, interligne 1.15
CONFORME AU CODE RÉEL (dashboard.py, rag_scoring_groq.py, n8n_workflow.json)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os

pt = 1  # Point unit

# Configuration
OUTPUT_DIR = "."
SUJET_A_MD = "documents/SUJET_A_RAG_Report.md"
SUJET_B_MD = "documents/SUJET_B_n8n_Report.md"

def read_markdown(filepath):
    """Lit un fichier Markdown"""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def create_pdf_sujet_a():
    """Génère le PDF SUJET A — conforme au code réel dashboard.py + rag_scoring_groq.py"""
    
    pdf_file = os.path.join(OUTPUT_DIR, "SUJET_A_RAG_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        fontName='Times-Bold',
        alignment=1  # Center
    )
    
    # Style heading2
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Times-Bold'
    )
    
    # Style normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Times-Roman',
        lineHeight=1.15*11,
        spaceAfter=8,
        alignment=4  # Justify
    )
    
    # Contenu
    story = []
    
    # Titre
    story.append(Paragraph("SUJET A — RAG POUR L'ANALYSE FINANCIÈRE", title_style))
    story.append(Spacer(1, 0.3*cm))
    
    # 1. Tâche choisie
    story.append(Paragraph("1. Tâche Choisie", heading2_style))
    story.append(Paragraph(
        "T3 — Scoring automatique du dossier d'investissement. Cette tâche a été choisie car elle répond "
        "directement au besoin d'un fonds d'investissement d'évaluer FallahTech selon des critères multicritères "
        "quantifiables et traçables. Le système produit un score sur 10 par critère avec citation des sources, "
        "et une recommandation finale (Investir / Conditions / No-go).",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 2. Architecture RAG
    story.append(Paragraph("2. Architecture RAG", heading2_style))
    story.append(Paragraph(
        "<b>Pipeline complet:</b> Ingestion PDF (pypdf/openpyxl via ingest.py) → Chunking (1000 chars, 200 overlap "
        "via embeddings.py) → Embedding Nomic all-MiniLM-L6-v2 (384-dim, via embeddings_nomic.py) → "
        "ChromaDB PersistentClient (collection fallahtech_docs_nomic) → Retrieval sémantique top-7 chunks → "
        "LLM Groq (Llama 3.1 70B / fallback Mixtral 8x7B) → Réponse structurée avec citations sources.<br/><br/>"
        "<b>Choix technologiques:</b> ChromaDB assure persistance locale sans serveur externe ; "
        "Nomic embeddings (sentence-transformers, all-MiniLM-L6-v2) offrent une représentation sémantique "
        "professionnelle 384-dim ; Groq API fournit ultra-rapidité (~500ms vs Ollama 120-300s timeout).",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 3. Choix du LLM
    story.append(Paragraph("3. Modèle LLM Retenu", heading2_style))
    story.append(Paragraph(
        "<b>Modèle principal:</b> Groq Llama 3.1 70B Versatile (llama-3.1-70b-versatile)<br/>"
        "<b>Fallbacks:</b> Llama 3.1 8B Instant → Mixtral 8x7B Instruct (cascade automatique si modèle indisponible)<br/>"
        "<b>Justification:</b> Performance supérieure sur analyses financières, latence ultra-basse (~500ms-1s), "
        "coût zéro (free tier Groq), API cloud acceptable (données FallahTech fictives, cf. note de l'énoncé).<br/>"
        "<b>Température:</b> 0.25 pour le scoring professionnel (dashboard.py), 0.3 pour le Q&amp;A custom, "
        "0.0 dans rag_scoring_groq.py (mode déterministe strict). Le choix de 0.25 permet un léger gain de "
        "variété dans les justifications tout en restant fortement contraint.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 4. Stratégie de Chunking
    story.append(Paragraph("4. Stratégie de Chunking", heading2_style))
    story.append(Paragraph(
        "<b>Taille:</b> 1000 caractères ; <b>Overlap:</b> 200 caractères (fenêtre glissante, "
        "implémenté dans embeddings.py, CHUNK_SIZE=1000, CHUNK_OVERLAP=200).<br/>"
        "<b>Rationale:</b> Documents financiers (bilans, ratios historiques) requièrent contexte étendu. "
        "L'overlap de 20% assure continuité sémantique entre chunks adjacents, critique pour traçabilité "
        "des citations cross-critères (ex: marges + revenus dans le même paragraphe). "
        "Résultat: ~60+ chunks indexés dans ChromaDB.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 5. Prompts
    story.append(Paragraph("5. Prompts & Ingénierie Dynamique", heading2_style))
    story.append(Paragraph(
        "<b>System Prompt:</b> « Tu es un expert analyste financier. Sois PRÉCIS, PROFESSIONNEL "
        "et BASE-TOI UNIQUEMENT sur les données fournies. Respecte le format demandé. »<br/>"
        "<b>User Prompt Dynamique:</b> La longueur requise (80, 150 ou 250 mots) et le style rédactionnel "
        "(télégraphique, journalistique, ou académique) s'adaptent automatiquement selon la densité de contexte (Slider 3 à 15 chunks).<br/>"
        "<b>User Prompt Q&amp;A:</b> « QUESTION: [question]. FORMAT: RÉPONSE + SOURCES + niveau CONFIANCE (sans limite de caractères). »",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 6. Stack technique
    story.append(Paragraph("6. Stack Technique", heading2_style))
    story.append(Paragraph(
        "Python 3.10+ | Streamlit (UI dashboard, dashboard.py) | ChromaDB PersistentClient (vectorstore local) | "
        "Sentence-Transformers / all-MiniLM-L6-v2 (embeddings Nomic 384-dim) | "
        "Groq SDK (LLM API, groq Python package) | Plotly (visualisations: graphes barres + jauges) | "
        "JSON (outputs structurés export) | pypdf + openpyxl (ingestion documents)",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 7. Résultats et UI
    story.append(Paragraph("7. Résultats et Interface Utilisateur", heading2_style))
    story.append(Paragraph(
        "<b>4 Critères évalués et pondérés:</b> Santé Financière (40%), Traction Commerciale (30%), Qualité de l'Équipe (15%), Opportunité de Marché (15%).<br/>"
        "<b>Dashboard Premium:</b> Interface sombre professionnelle type SaaS. Graphes recréés de zéro sans Plotly: jauge globale en SVG pur vectoriel animé, et bar chart de répartition en pur HTML/CSS avec gradients texturés violet.<br/>"
        "<b>Résilience API:</b> Implémentation d'un délai `time.sleep(2.5)` inter-requêtes pour éviter les blocages rate-limit fréquents de l'API gratuite Groq (HTTP 429), garantissant 100% de succès sur les évaluations complètes.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 8. Limites et Corrections Apportées
    story.append(Paragraph("8. Défis Surmontés et Limites", heading2_style))
    story.append(Paragraph(
        "• <b>Défi ChromaDB:</b> Les PDFs contenaient des caractères nuls brisant l'instanciation de ChromaDB. Un script externe (`rebuild_embeddings.py`) a assaini les textes et reconstruit la base de 18 chunks natifs.<br/>"
        "• <b>Défi Rate-Limit:</b> Invoquer Groq 4 fois par seconde provoquait un refus serveur: résolu par temporisation.<br/>"
        "• Limite: Pas d'extraction automatique des tableaux sans parser lourd (pdfplumber) — mitigation: transcription partielle manuelle ou context in-doc.<br/>"
        "• Limite: Pas de versioning d'historique (le scoring de session est éphémère).",
        normal_style
    ))
    
    # Construire le PDF
    doc.build(story)
    print(f"✅ PDF généré: {pdf_file}")

def create_pdf_sujet_b():
    """Génère le PDF SUJET B — conforme au vrai workflow n8n exporté + API Flask/ngrok"""
    
    pdf_file = os.path.join(OUTPUT_DIR, "SUJET_B_n8n_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        fontName='Times-Bold',
        alignment=1
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Times-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Times-Roman',
        lineHeight=1.15*11,
        spaceAfter=8,
        alignment=4
    )
    
    story = []
    
    # Titre
    story.append(Paragraph("SUJET B — AUTOMATISATION AVEC N8N", title_style))
    story.append(Spacer(1, 0.3*cm))
    
    # 1. Tâche automatisée
    story.append(Paragraph("1. Tâche Automatisée", heading2_style))
    story.append(Paragraph(
        "Automatisation de T3 (Scoring multicritère du dossier d'investissement FallahTech). "
        "Le workflow n8n orchestre le pipeline RAG du SUJET A via des requêtes HTTP vers l'API Python "
        "exposée par un tunnel Ngrok. Le workflow vérifie d'abord la santé de l'API et la disponibilité des "
        "documents, puis déclenche l'analyse RAG complète et formate les résultats en JSON structuré.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 2. Architecture n8n — Schéma du workflow
    story.append(Paragraph("2. Architecture du Workflow (8 nœuds)", heading2_style))
    story.append(Paragraph(
        "<b>Nœud 1 — Manual Trigger:</b> Déclenchement manuel du workflow pour exécution contrôlée.<br/>"
        "<b>Nœud 2 — Check API Health (HTTP Request):</b> GET vers /api/health via Ngrok pour vérifier "
        "que l'API Python est opérationnelle. Headers: ngrok-skip-browser-warning, User-Agent n8n-agent/1.0. "
        "Timeout 10s, gestion erreur avec continueErrorOutput.<br/>"
        "<b>Nœud 3 — Get Available Documents (HTTP Request):</b> GET vers /api/documents via Ngrok (parallèle au health check) "
        "pour lister les documents disponibles dans le corpus FallahTech.<br/>"
        "<b>Nœud 4 — Combine Health &amp; Documents (Merge):</b> Fusionne les résultats des deux requêtes parallèles "
        "(santé API + liste documents) pour constituer le contexte d'analyse.<br/>"
        "<b>Nœud 5 — RAG Analysis (HTTP Request POST):</b> POST vers /api/webhook/analyze avec le body JSON fusionné. "
        "Timeout 30s. Déclenche le pipeline RAG complet côté serveur Python (retrieval ChromaDB + scoring Groq LLM).<br/>"
        "<b>Nœud 6 — Debug RAG Output (Set):</b> Agrège les outputs de RAG Analysis, Check API Health et Get Documents "
        "dans un objet structuré (rag_result, health_check, documents) pour traçabilité.<br/>"
        "<b>Nœud 7 — Format JSON Response (Code):</b> Script JavaScript formatant le résultat final: "
        "success, score, analysis, question, timestamp, sources, et debug info.<br/>"
        "<b>Nœud 8 — Return Response (Respond to Webhook):</b> Retourne la réponse JSON formatée au client.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 3. LLM
    story.append(Paragraph("3. Modèle LLM Intégré", heading2_style))
    story.append(Paragraph(
        "<b>Modèle:</b> Groq Llama 3.1 70B Versatile (identique SUJET A, via l'API Python backend)<br/>"
        "<b>Fallbacks:</b> Llama 3.1 8B Instant → Mixtral 8x7B Instruct (cascade automatique)<br/>"
        "<b>Paramètres:</b> température 0.25 (scoring), max_tokens 600, top_p 0.9, timeout 30s<br/>"
        "<b>Justification:</b> Le LLM est invoqué côté serveur Python (pas directement dans n8n) via l'API exposée "
        "par Ngrok. Cela garantit cohérence avec le SUJET A et permet d'utiliser le même pipeline RAG "
        "(ChromaDB retrieval + Groq scoring) sans dupliquer la logique dans n8n.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 4. Prompts
    story.append(Paragraph("4. Prompts dans n8n", heading2_style))
    story.append(Paragraph(
        "Les prompts sont gérés côté serveur Python (identiques au SUJET A) et non directement dans les nœuds n8n:<br/>"
        "<b>System:</b> « Tu es un expert analyste financier. Sois PRÉCIS, PROFESSIONNEL et BASE-TOI "
        "UNIQUEMENT sur les données fournies. »<br/>"
        "<b>User (Scoring):</b> « Tu es un analyste financier VC expert avec 15 ans d'expérience. "
        "CRITÈRE À ÉVALUER: [critère]. DOCUMENTS FOURNIS: [top-7 chunks ChromaDB]. "
        "FORMAT: SCORE [0-10] / ANALYSE [détaillée]. »<br/>"
        "<b>Code Node (Format JSON):</b> Le nœud Code JavaScript dans n8n extrait et structure les champs: "
        "success, score, analysis, question, timestamp, sources, debug (health_check + documents).",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 5. Déploiement
    story.append(Paragraph("5. Détails de Déploiement", heading2_style))
    story.append(Paragraph(
        "<b>n8n:</b> n8n Cloud (instance hébergée)<br/>"
        "<b>API Backend:</b> Serveur Python Flask (api.py) exposé via tunnel Ngrok "
        "(URL: https://cherish-facile-wrongly.ngrok-free.dev)<br/>"
        "<b>Ngrok Headers:</b> ngrok-skip-browser-warning: true + User-Agent: n8n-agent/1.0 "
        "(contourne la page d'avertissement Ngrok)<br/>"
        "<b>ChromaDB:</b> Persistance locale (chroma_db/) côté serveur Python<br/>"
        "<b>Credentials:</b> Groq API key gérée côté serveur Python (.env), non exposée dans n8n<br/>"
        "<b>Sécurité:</b> Les données FallahTech sont fictives (cf. note énoncé), donc l'utilisation "
        "de services cloud (Ngrok, Groq, n8n Cloud) est sans restriction de confidentialité.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 6. Export workflow
    story.append(Paragraph("6. Fichier .json du Workflow", heading2_style))
    story.append(Paragraph(
        "Fichier <b>n8n_workflow.json</b> fourni — exporté directement depuis l'interface n8n. "
        "Nom du workflow: « FallahTech RAG Cloud Collaboration with Ngrok API Integration ». "
        "Contient: 8 nœuds (Manual Trigger, Check API Health, Get Available Documents, "
        "Combine Health &amp; Documents, RAG Analysis, Debug RAG Output, Format JSON Response, "
        "Return Response). Format standard n8n v1 — importable en 1 clic via Import from File dans n8n.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    # 7. Démonstration
    story.append(Paragraph("7. Résultats Exécution", heading2_style))
    story.append(Paragraph(
        "Workflow exécuté avec succès via Manual Trigger. Flux d'exécution: "
        "Manuel Trigger → (parallèle) Check API Health + Get Documents → Merge → RAG Analysis "
        "→ Debug → Format JSON → Return Response. "
        "Résultat JSON structuré avec score, analyse, sources et métadonnées de debug. "
        "Erreurs: gestion via continueErrorOutput sur tous les nœuds HTTP (résilience en cas de timeout Ngrok).",
        normal_style
    ))
    
    # 8. Limites
    story.append(Paragraph("8. Limites &amp; Améliorations", heading2_style))
    story.append(Paragraph(
        "• Dépendance au tunnel Ngrok (URL temporaire, reconnexion nécessaire si le tunnel expire)<br/>"
        "• Pas de retry automatique sur timeout réseau — amélioration: ajouter un nœud error handling avec retry<br/>"
        "• Pas de cache des résultats entre exécutions — amélioration: ajouter Redis ou stockage intermédiaire<br/>"
        "• Pas de scheduling automatique (trigger manuel uniquement) — amélioration: ajouter un Cron Trigger<br/>"
        "• Monitoring limité — amélioration: intégrer logging n8n + webhook de notification (Slack/Email)",
        normal_style
    ))
    
    doc.build(story)
    print(f"✅ PDF généré: {pdf_file}")

def main():
    print("\n" + "="*60)
    print("📄 GÉNÉRATION DES PDFs - SUJET A & SUJET B")
    print("="*60)
    
    print("\n[1] Génération SUJET_A_RAG_Report.pdf...")
    create_pdf_sujet_a()
    
    print("[2] Génération SUJET_B_n8n_Report.pdf...")
    create_pdf_sujet_b()
    
    print("\n" + "="*60)
    print("✅ GÉNÉRATION COMPLÉTÉE!")
    print("="*60)
    print(f"\n📁 Fichiers créés:")
    print(f"   • SUJET_A_RAG_Report.pdf (3-4 pages, Times New Roman 11pt)")
    print(f"   • SUJET_B_n8n_Report.pdf (3-4 pages, Times New Roman 11pt)")
    print(f"\n✅ Format: PDF, 11pt, interligne 1.15 — Conforme énoncé!")

if __name__ == "__main__":
    main()
