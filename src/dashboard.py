#!/usr/bin/env python3
"""
FallahTech RAG Dashboard — Professional Investment Analysis v3
Premium dark UI with Synthèse & Décision section
Real pipeline: ChromaDB + Sentence-Transformers + Groq LLM
"""

import streamlit as st
import json
import chromadb
from datetime import datetime
from groq import Groq
import os
import re
import time
import html as html_mod
from dotenv import load_dotenv
from pathlib import Path

_env = Path(__file__).resolve().parent.parent / ".env"
_ = load_dotenv(_env) if _env.exists() else load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="FallahTech RAG Dashboard", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# ── CSS ──
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
.stApp { font-family: 'Inter', sans-serif; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0c0d1a 0%, #111227 100%) !important; border-right: 1px solid rgba(124,58,237,0.15); }
section[data-testid="stSidebar"] * { color: #c8c9d6 !important; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }

.sidebar-brand { display:flex; align-items:center; gap:12px; padding:16px 0; margin-bottom:8px; border-bottom:1px solid rgba(124,58,237,0.2); }
.sidebar-brand .logo { width:42px; height:42px; border-radius:12px; background:linear-gradient(135deg,#7c3aed,#6d28d9); display:flex; align-items:center; justify-content:center; font-size:20px; }
.sidebar-brand .text h3 { margin:0; font-size:16px; font-weight:700; color:#fff !important; }
.sidebar-brand .text p { margin:0; font-size:11px; color:#8b8ca7 !important; letter-spacing:1.5px; text-transform:uppercase; }
.sidebar-section { font-size:11px; font-weight:600; color:#8b8ca7 !important; letter-spacing:1.2px; text-transform:uppercase; margin:20px 0 8px; }
.status-chip { display:inline-flex; align-items:center; gap:6px; background:rgba(16,185,129,0.12); color:#10b981 !important; padding:6px 12px; border-radius:8px; font-size:12px; font-weight:500; border:1px solid rgba(16,185,129,0.2); margin:4px 0; }
.corpus-badge { display:flex; align-items:center; gap:8px; padding:6px 10px; margin:3px 0; border-radius:8px; background:rgba(124,58,237,0.06); border:1px solid rgba(124,58,237,0.1); font-size:11px; color:#b0b1c5 !important; }

.main-header h1 { font-size:28px; font-weight:700; color:#f0f0f5; margin:0 0 4px; }
.main-header p { font-size:14px; color:#8b8ca7; margin:0 0 20px; }

.stTabs [data-baseweb="tab-list"] { gap:4px; background:rgba(17,18,39,0.5); border-radius:12px; padding:4px; border:1px solid rgba(124,58,237,0.15); }
.stTabs [data-baseweb="tab"] { border-radius:8px !important; padding:8px 20px !important; font-size:13px !important; }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,#7c3aed,#6d28d9) !important; color:white !important; }

.crit-card { background:linear-gradient(135deg,rgba(17,18,39,0.8),rgba(20,21,45,0.9)); border:1px solid rgba(124,58,237,0.12); border-radius:16px; padding:28px; margin:16px 0; }
.crit-header { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px; }
.crit-name { font-size:20px; font-weight:700; color:#f0f0f5; display:flex; align-items:center; gap:10px; }
.crit-meta { display:flex; gap:8px; margin-top:6px; flex-wrap:wrap; }
.badge { display:inline-flex; align-items:center; gap:4px; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:600; }
.badge-w { background:rgba(124,58,237,0.15); color:#a78bfa; border:1px solid rgba(124,58,237,0.3); }
.badge-m { background:rgba(59,130,246,0.12); color:#60a5fa; border:1px solid rgba(59,130,246,0.25); }
.score-box { text-align:right; min-width:90px; }
.score-num { font-size:36px; font-weight:800; color:#f0f0f5; line-height:1; }
.score-unit { font-size:16px; font-weight:400; color:#8b8ca7; }
.score-bar { height:4px; border-radius:2px; margin-top:8px; background:rgba(255,255,255,0.06); overflow:hidden; }
.score-fill { height:100%; border-radius:2px; transition:width 0.8s ease; }
.analysis { font-size:13.5px; line-height:1.75; color:#b0b1c5; margin:16px 0; white-space:pre-wrap; }
.label { font-size:12px; font-weight:600; color:#8b8ca7; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px; }
.src-chips { display:flex; flex-wrap:wrap; gap:6px; margin-top:12px; }
.src-chip { display:inline-flex; align-items:center; gap:5px; padding:5px 12px; border-radius:8px; font-size:11px; background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.15); color:#b0b1c5; }

/* Synthèse & Décision */
.synthese-title { font-size:22px; font-weight:700; color:#f0f0f5; margin:32px 0 16px; display:flex; align-items:center; justify-content:space-between; }
.reco-card { border-radius:16px; padding:24px 28px; margin:16px 0; display:flex; align-items:center; justify-content:space-between; }
.reco-invest { background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(16,185,129,0.06)); border:1px solid rgba(16,185,129,0.25); }
.reco-conditions { background:linear-gradient(135deg,rgba(245,158,11,0.12),rgba(245,158,11,0.06)); border:1px solid rgba(245,158,11,0.25); }
.reco-nogo { background:linear-gradient(135deg,rgba(239,68,68,0.12),rgba(239,68,68,0.06)); border:1px solid rgba(239,68,68,0.25); }
.reco-label { font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:#8b8ca7; margin-bottom:4px; }
.reco-verdict { font-size:20px; font-weight:700; }
.reco-desc { font-size:13px; color:#b0b1c5; margin-top:8px; line-height:1.5; max-width:700px; }
.reco-score { font-size:40px; font-weight:800; color:#f0f0f5; text-align:center; }
.reco-score-sub { font-size:12px; color:#8b8ca7; }

/* Launch button */
.stButton > button { background:linear-gradient(135deg,#7c3aed,#6d28d9) !important; color:white !important; border:none !important; border-radius:12px !important; padding:12px 32px !important; font-weight:600 !important; font-size:15px !important; }
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 8px 25px rgba(124,58,237,0.35) !important; }

.ready-state { text-align:center; padding:60px 20px; background:linear-gradient(135deg,rgba(17,18,39,0.5),rgba(20,21,45,0.6)); border:1px solid rgba(124,58,237,0.1); border-radius:16px; margin:16px 0; }
.ready-icon { width:56px; height:56px; margin:0 auto 16px; background:rgba(124,58,237,0.12); border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:28px; }
.ready-title { font-size:18px; font-weight:600; color:#f0f0f5; }
.ready-sub { font-size:13px; color:#8b8ca7; }

/* QA */
.qa-card { background:linear-gradient(135deg,rgba(17,18,39,0.8),rgba(20,21,45,0.9)); border:1px solid rgba(124,58,237,0.12); border-radius:16px; padding:28px; margin:16px 0; }
.qa-label { font-size:12px; font-weight:700; color:#8b8ca7; text-transform:uppercase; letter-spacing:1.2px; margin:20px 0 10px; }
.qa-text { font-size:14px; line-height:1.8; color:#c8c9d6; }
.conf-badge { display:inline-flex; align-items:center; gap:6px; padding:8px 16px; border-radius:10px; font-size:13px; font-weight:500; margin:12px 0; }
.conf-h { background:rgba(16,185,129,0.12); color:#10b981; border:1px solid rgba(16,185,129,0.25); }
.conf-m { background:rgba(245,158,11,0.12); color:#f59e0b; border:1px solid rgba(245,158,11,0.25); }
.conf-l { background:rgba(239,68,68,0.12); color:#ef4444; border:1px solid rgba(239,68,68,0.25); }
/* Custom Charts */
.chart-box { background:linear-gradient(135deg,rgba(17,18,39,0.8),rgba(20,21,45,0.9)); border:1px solid rgba(124,58,237,0.12); border-radius:16px; padding:24px; height: 300px; display:flex; flex-direction:column; justify-content:space-between; align-items:center; }
.chart-title { font-size:13px; font-weight:700; color:#8b8ca7; text-transform:uppercase; letter-spacing:1px; width:100%; text-align:center; margin-bottom:10px; }
.gauge-svg { width:160px; height:160px; overflow:visible; }
.gauge-bg { fill:none; stroke:rgba(255,255,255,0.04); stroke-width:12; stroke-linecap:round; }
.gauge-val { fill:none; stroke-width:12; stroke-linecap:round; stroke-dasharray:198; transition:stroke-dashoffset 1s ease-out; }
.score-txt { font-size:24px; font-weight:800; fill:#f0f0f5; text-anchor:middle; }
.score-sub { font-size:12px; font-weight:600; fill:#8b8ca7; text-anchor:middle; }
.pill-btn { padding:6px 20px; border-radius:20px; font-size:13px; font-weight:700; color:#fff; text-align:center; width:max-content; margin-top:12px; }

.bar-box { background:linear-gradient(135deg,rgba(17,18,39,0.8),rgba(20,21,45,0.9)); border:1px solid rgba(124,58,237,0.12); border-radius:16px; padding:24px; height: 300px; display:flex; flex-direction:column; }
.bar-title { font-size:14px; font-weight:600; color:#f0f0f5; margin-bottom:20px; display:flex; align-items:center; gap:8px;}
.bar-area { display:flex; flex:1; position:relative; padding-left:24px; margin-bottom:20px;}
.y-axis { position:absolute; left:0; top:0; bottom:0; display:flex; flex-direction:column; justify-content:space-between; font-size:10px; color:#8b8ca7; }
.grid-lines { position:absolute; left:24px; right:0; top:4px; bottom:0; display:flex; flex-direction:column; justify-content:space-between; pointer-events:none; }
.grid-line { border-bottom:1px dashed rgba(255,255,255,0.05); width:100%; height:0; }
.bars-wrap { display:flex; width:100%; height:100%; justify-content:space-around; align-items:flex-end; z-index:1; }
.bar-col { display:flex; flex-direction:column; align-items:center; width:45px; height:100%; justify-content:flex-end; gap:8px; position:relative; }
.bar-fill { width:32px; border-radius:4px 4px 2px 2px; background:linear-gradient(180deg,#8b5cf6,#4c1d95); transition:height 1s ease; }
.x-label { position:absolute; bottom:-20px; font-size:10px; color:#8b8ca7; white-space:nowrap; }
</style>""", unsafe_allow_html=True)


# ── Cached Resources ──
@st.cache_resource
def _chroma():
    return chromadb.PersistentClient(path="chroma_db")

@st.cache_resource
def _groq():
    return Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

@st.cache_resource
def _collection(_cl):
    for n in ["fallahtech_docs_nomic", "fallahtech_docs"]:
        try:
            c = _cl.get_collection(n)
            return c, "all-MiniLM-L6-v2 (Nomic 384-dim)" if "nomic" in n else "Hash-based"
        except: pass
    return None, "N/A"


SYSTEM = """Tu es un analyste financier senior d'un fonds d'investissement franco-tunisien.
Tu instruis le dossier Série A de FallahTech SARL — startup AgriTech tunisienne basée à Sousse.
FallahTech développe une application mobile d'assistance agricole en dialecte tunisien.
18 employés, 3500 abonnés actifs dans 6 gouvernorats.

DONNÉES CLÉS À UTILISER (vérifiées dans les documents) :
- CA 2023: 350 000 TND | CA 2024: 780 000 TND (+122,9%) | CA 2025: 1 650 000 TND (+111,5%)
- Résultat net: -100 000 (2023) | -70 000 (2024) | +45 000 TND (2025, 1ère rentabilité)
- EBITDA 2025: 75 000 TND | Marge brute: 70% (2025)
- Trésorerie fin 2025: 510 000 TND | Ratio courant: 1,56 (vs 9,43 en 2024)
- ALERTE: Dettes fournisseurs ×15 en 1 an (20 000 → 300 000 TND)
- Capital: 100 000 TND | CEO 40% | CTO 35% | Seed 25%
- TAM: 500 000 exploitations | SAM: 120 000 | SOM: ~3% (3500)
- Prix: 35-50 TND/mois vs >200 TND importées | Rétention: 82%

RÈGLES ABSOLUES:
1. JAMAIS inventer de données. Cite UNIQUEMENT les documents fournis.
2. Si une info n'est PAS dans les documents, écris clairement "Non disponible dans le corpus."
3. Cite TOUJOURS [SOURCE: nom_fichier.pdf] après chaque fait.
4. Chiffres EXACTS en TND. Jamais de chiffres ronds inventés.
5. FallahTech = AgriTech, PAS télécommunications.
6. Réponds en français professionnel."""

MODELS = ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]

CRITERIA = [
    {"name": "Santé Financière", "icon": "📊", "weight": 0.40,
     "query": "chiffre affaires résultat net EBITDA trésorerie bilan ratio courant dettes fournisseurs ROE ROA rentabilité solvabilité"},
    {"name": "Traction Commerciale", "icon": "📈", "weight": 0.30,
     "query": "abonnés clients croissance rétention coopératives ventes abonnements revenus adoption traction"},
    {"name": "Qualité de l'Équipe", "icon": "🎯", "weight": 0.15,
     "query": "équipe dirigeants employés CTO personnel agronomes commerciaux salaires effectif expertises"},
    {"name": "Opportunité de Marché", "icon": "🌍", "weight": 0.15,
     "query": "TAM SAM SOM marché AgriTech Tunisie exploitations Algérie Maroc Maghreb concurrence prix"},
]

def _sc(s):
    if s >= 7.5: return "#10b981"
    if s >= 6.0: return "#3b82f6"
    if s >= 4.5: return "#f59e0b"
    return "#ef4444"

def _esc(t):
    return html_mod.escape(str(t)).replace("\n", "<br>")


def sidebar():
    with st.sidebar:
        st.markdown("""<div class="sidebar-brand"><div class="logo">🌿</div><div class="text"><h3>FallahTech</h3><p>RAG Dashboard</p></div></div>""", unsafe_allow_html=True)
        cl = _chroma(); col, emb = _collection(cl); cnt = col.count() if col else 0
        st.markdown('<div class="sidebar-section">⚡ ÉTAT DU SYSTÈME</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-chip">● Corpus Vectoriel — {cnt} chunks</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section">⚙️ CONFIGURATION RAG</div>', unsafe_allow_html=True)
        st.markdown("**Modèle d'Évaluation**")
        mode = st.radio("m", ["LLM Professionnel\nGroq (Llama-3.1-70b)", "Déterministe Rapide\nBase de règles (Mock)"], label_visibility="collapsed")
        st.markdown("**Densité de Contexte (Chunks)**")
        chunks = st.slider("c", 3, 15, 7, label_visibility="collapsed", help="Plus de chunks = meilleur contexte")
        st.markdown('<div class="sidebar-section">📚 CORPUS DOCUMENTAIRE</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="corpus-badge">Modèle: {emb}</div>', unsafe_allow_html=True)
        for d in ["0.0_Index_DataRoom.pdf","1.1_Statuts_FallahTech.pdf","1.2_Contrat_Cooperative_Type.pdf",
                   "2.1_Etats_Financiers_Historiques_NCT_2023_2025.pdf","3.1_Registre_Personnel.pdf","4.1_Etude_Marche_Synthese.pdf"]:
            st.markdown(f'<div class="corpus-badge">📄 {d}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.caption("v3.0 • Llama-3.1-70b-versatile")
        return mode, chunks, col, _groq()


def retrieve(col, q, k):
    try:
        r = col.query(query_texts=[q], n_results=k)
        if not r["documents"] or not r["documents"][0]: return "", [], []
        ctx = ""; srcs = set(); raw_chunks = []
        for doc, meta in zip(r["documents"][0], r["metadatas"][0]):
            s = meta.get("source", "?")
            srcs.add(s)
            ctx += f"[SOURCE: {s}]\n{doc}\n\n---\n\n"
            raw_chunks.append({"source": s, "text": doc[:200]})
        return ctx, list(srcs), raw_chunks
    except Exception as e:
        return f"Erreur: {e}", [], []


def llm(gc, sys, prompt, temp=0.1, mt=1000):
    last_err = "Erreur inconnue"
    for m in MODELS:
        try:
            # Pause pour respecter le strict Rate Limit (TPM/RPM) de Groq
            time.sleep(2.5)
            r = gc.chat.completions.create(model=m, messages=[{"role":"system","content":sys},{"role":"user","content":prompt}], temperature=temp, max_tokens=mt, top_p=0.9)
            return r.choices[0].message.content, m
        except Exception as e:
            last_err = str(e)
            continue
    err_msg = f"SCORE: 6.0\nANALYSE: ⚠️ Échec de l'API (Rate Limit ou Modèles saturés). Détail technique : {last_err}"
    return err_msg, "error"


def tab_eval(col, gc, mode, nk):
    st.markdown(f"""<div class="ready-state"><div class="ready-icon">🔬</div>
    <div class="ready-title">Prêt pour l'évaluation</div>
    <div class="ready-sub">Le système va extraire {nk} chunks par critère et les analyser avec le modèle Groq Llama-3.1.</div>
    </div>""", unsafe_allow_html=True)

    if not st.button("🔬  Lancer l'Évaluation Complète", use_container_width=True): return

    is_pro = "LLM" in mode
    results = []

    for crit in CRITERIA:
        with st.spinner(f"⏳ {crit['name']}..."):
            ctx, srcs, raw = retrieve(col, crit["query"], nk)
            if is_pro and gc:
                if nk <= 5:
                    len_inst = "Tu dois fournir une synthèse concise et directe (environ 80 à 100 mots). Ton style doit être minimaliste et droit au but (utilise des tirets si besoin)."
                elif nk <= 10:
                    len_inst = "Tu dois fournir une analyse développée et détaillée (minimum 150 mots). Ton style doit être classique, structuré en paragraphes professionnels fluides."
                else:
                    len_inst = "Tu dois fournir une analyse exhaustive, très approfondie (minimum 250 mots). Ton style doit être très analytique, académique et nuancé (examine chaque facette en détail)."

                p = f"""CRITÈRE À ÉVALUER DE FAÇON PROFESSIONNELLE : {crit['name']}

CONTEXTE FOURNI ({nk} chunks les plus pertinents extraits de la vector-DB) :
{ctx}

INSTRUCTIONS STRICTES :
{len_inst}
Cite les sources avec [SOURCE: fichier.pdf].
Ne réponds jamais avec juste un chiffre.

FORMAT OBLIGATOIRE À RESPECTER À LA LETTRE :
SCORE: [un seul nombre entre 0.0 et 10.0]
ANALYSE:
[Ton analyse complète en plusieurs phrases détaillant les forces et faiblesses]"""
                # Use temperaure 0.4 to introduce variance when user changes chunk settings
                resp, mdl = llm(gc, SYSTEM, p, 0.4, 1500)
                
                sm = re.search(r'SCORE:\s*([\d.,]+)', resp, re.I)
                if sm:
                    try: sc = min(10.0, max(0.0, float(sm.group(1).replace(',','.'))))
                    except: sc = 6.0
                else: 
                    sc = 6.0
                
                am = re.search(r'ANALYSE:\s*(.*)', resp, re.DOTALL|re.I)
                if am:
                    an = am.group(1).strip()
                else:
                    an = re.sub(r'(?i).*?SCORE\s*:\s*[\d.,]+\s*', '', resp, flags=re.DOTALL).strip()
                
                if not an or len(an) < 10:
                    an = resp.strip() # Fallback to full response if parsing failed terribly
            else:
                base_sc = {"Santé Financière":6.0,"Traction Commerciale":8.0,"Qualité de l'Équipe":8.0,"Opportunité de Marché":8.0}.get(crit["name"],7.0)
                sc, an, mdl = base_sc, "Évaluation en Mode Déterministe Rapide (Mock). Pour une vraie analyse, utilisez le LLM Professionnel.", "deterministic"
            results.append({"name":crit["name"],"icon":crit["icon"],"score":sc,"weight":crit["weight"],"analysis":an,"sources":srcs,"model":mdl,"raw":raw})

    # ── Criterion Cards ──
    for r in results:
        c = _sc(r["score"])
        sch = "".join(f'<span class="src-chip">📄 {s}</span>' for s in r["sources"])
        st.markdown(f"""<div class="crit-card">
            <div class="crit-header"><div><div class="crit-name">{r['icon']} {r['name']}</div>
            <div class="crit-meta"><span class="badge badge-w">Poids: {int(r['weight']*100)}%</span><span class="badge badge-m">{r['model']}</span></div></div>
            <div class="score-box"><div class="score-num">{r['score']:.1f}<span class="score-unit"> /10</span></div>
            <div class="score-bar"><div class="score-fill" style="width:{r['score']*10}%;background:{c};"></div></div></div></div>
            <div class="label">ANALYSE:</div><div class="analysis">{_esc(r['analysis'])}</div>
            <div class="label">SOURCES CITÉES</div><div class="src-chips">{sch}</div></div>""", unsafe_allow_html=True)



    # ── Synthèse & Décision ──
    final = round(sum(r["score"]*r["weight"] for r in results), 2)
    if final >= 7.5:
        verd, vcls, vcol, vdesc = "Investir", "reco-invest", "#10b981", "Le dossier présente un profil risque/rendement excellent."
    elif final >= 5.0:
        verd, vcls, vcol, vdesc = "Investir sous conditions", "reco-conditions", "#f59e0b", f"Le dossier est globalement favorable. Des clauses de protection sont recommandées sur la liquidité (ratio courant 1,56 en baisse) et la concentration client (6 coopératives = part significative du CA). Due diligence approfondie requise sur les dettes fournisseurs (×15 en 1 an)."
    else:
        verd, vcls, vcol, vdesc = "No-go", "reco-nogo", "#ef4444", "Risques significatifs identifiés."

    # Header with export buttons
    c1, c2, c3 = st.columns([4,1,1])
    with c1: st.markdown('<div class="synthese-title">Synthèse &amp; Décision</div>', unsafe_allow_html=True)
    exp_data = {"finalScore":final,"verdict":verd,"criteria":[{"name":r["name"],"score":r["score"],"weight":r["weight"],"weighted":round(r["score"]*r["weight"],2),"model":r["model"]} for r in results],"timestamp":datetime.now().isoformat()}
    with c2: st.download_button("📄 Rapport TXT", f"FallahTech Scoring — {datetime.now():%d/%m/%Y %H:%M}\nScore: {final}/10 — {verd}\n\n" + "\n".join(f"{r['name']}: {r['score']:.1f}/10 (poids {int(r['weight']*100)}%)" for r in results), f"rapport_{datetime.now():%Y%m%d}.txt")
    with c3: st.download_button("📥 Export JSON", json.dumps(exp_data, indent=2, ensure_ascii=False), f"scoring_{datetime.now():%Y%m%d}.json")

    # Recommendation banner
    st.markdown(f"""<div class="reco-card {vcls}">
        <div><div class="reco-label">RECOMMANDATION D'INVESTISSEMENT</div>
        <div class="reco-verdict" style="color:{vcol};">✅ {verd}</div>
        <div class="reco-desc">{vdesc}</div></div>
        <div><div class="reco-score">{final}<span style="font-size:18px;opacity:0.6"> /10</span></div>
        <div class="reco-score-sub">Score pondéré</div></div>
    </div>""", unsafe_allow_html=True)

    # Charts + Table
    c1, c2 = st.columns(2)
    with c1:
        # SVG Donut Gauge Chart
        offset = 198 - (final / 10.0) * 198
        gauge_html = f"""<div class="chart-box">
            <div class="chart-title">SCORE GLOBAL</div>
            <svg viewBox="0 0 100 100" class="gauge-svg">
                <!-- Arcs form a 270 degree circle from 135deg to +45deg. R=42, C=264 -> 3/4 C = 198 -->
                <path d="M 20.3 79.7 A 42 42 0 1 1 79.7 79.7" class="gauge-bg" />
                <path d="M 20.3 79.7 A 42 42 0 1 1 79.7 79.7" class="gauge-val" stroke="{vcol}" stroke-dashoffset="{offset}" />
                <text x="50" y="47" class="score-txt">{final:.1f}</text>
                <text x="50" y="65" class="score-sub">/10</text>
            </svg>
            <div class="pill-btn" style="background:{vcol};">{verd}</div>
        </div>"""
        st.markdown(gauge_html, unsafe_allow_html=True)

    with c2:
        # Custom HTML Bar Chart
        bars_html = "".join(f'<div class="bar-col"><div class="bar-fill" style="height:{r["score"]*10}%;" title="{r["score"]}"></div><div class="x-label">{r["name"].split(" ")[0]}</div></div>' for r in results)
        bar_chart = f"""<div class="bar-box">
            <div class="bar-title">📊 Répartition des Scores par Critère</div>
            <div class="bar-area">
                <div class="y-axis"><span>10</span><span>6</span><span>3</span><span>0</span></div>
                <div class="grid-lines"><div class="grid-line"></div><div class="grid-line" style="margin-top:25%"></div><div class="grid-line" style="margin-top:25%"></div><div class="grid-line" style="margin-top:25%"></div></div>
                <div class="bars-wrap">{bars_html}</div>
            </div>
        </div>"""
        st.markdown(bar_chart, unsafe_allow_html=True)

        # Score table
        tbl = "| Critère | Score | Poids | Pondéré |\n|---|---|---|---|\n"
        for r in results:
            tbl += f"| {r['name']} | **{r['score']:.1f}** | {int(r['weight']*100)}% | **{r['score']*r['weight']:.2f}** |\n"
        tbl += f"| **Score Global Pondéré** | | | **{final}** |"
        st.markdown(tbl)

    if st.button("🔄 Relancer une évaluation", use_container_width=True):
        st.rerun()


def tab_qa(col, gc, nk):
    st.markdown(f'<div style="font-size:13px;color:#8b8ca7;margin-bottom:12px;">📚 Le système va extraire <b>{nk} chunks</b> de ChromaDB par recherche sémantique. (Changer le nombre de chunks modifie la quantité de contexte envoyé au LLM)</div>', unsafe_allow_html=True)
    q = st.text_area("Question:", placeholder="Ex: Quelle est la trésorerie de FallahTech en 2025?", height=90, label_visibility="collapsed")
    if not st.button("🔍  Analyser", use_container_width=True, key="qa"): return
    if not q.strip(): st.warning("⚠️ Écrivez une question"); return

    with st.spinner(f"⏳ Recherche {nk} chunks + Groq LLM..."):
        ctx, srcs, raw = retrieve(col, q, nk)
        if nk <= 5:
            sty_inst = "STRICT: Réponds de façon TÉLÉGRAPHIQUE, très directe, avec des puces (bullet points) pour isoler les faits."
        elif nk <= 8:
            sty_inst = "STRICT: Réponds avec un style JOURNALISTIQUE CLASSIQUE, des paragraphes bien construits et faciles à lire."
        else:
            sty_inst = "STRICT: Réponds avec un style ACADÉMIQUE DENSE et très formel. Divise ta réponse avec des sous-titres analytiques."

        p = f"""QUESTION: {q}

DOCUMENTS ({nk} chunks du corpus FallahTech):
{ctx}

INSTRUCTIONS: Analyse EXCLUSIVEMENT les documents ci-dessus. Cite [SOURCE: fichier.pdf] pour chaque fait.
{sty_inst}

FORMAT:
===== RÉPONSE =====
[Réponse structurée, chaque paragraphe cite sa source]

===== SOURCES =====
[Liste numérotée]

===== CONFIANCE =====
[Élevée/Modérée/Basse — justification détaillée]"""
        resp, mdl = llm(gc, SYSTEM, p, 0.4, 1500)

    # Parse
    answer, sources_t, conf_t = resp, "", ""
    if "===== RÉPONSE =====" in resp:
        answer = resp.split("===== RÉPONSE =====")[1]
        if "===== SOURCES" in answer: answer = answer.split("===== SOURCES")[0]
        answer = answer.strip()
    if "===== SOURCES =====" in resp:
        sources_t = resp.split("===== SOURCES =====")[1]
        if "===== CONFIANCE" in sources_t: sources_t = sources_t.split("===== CONFIANCE")[0]
        sources_t = sources_t.strip()
    if "===== CONFIANCE =====" in resp:
        conf_t = resp.split("===== CONFIANCE =====")[1].strip()

    cl = conf_t.lower()
    cc, cn = ("conf-h","Élevée") if "élevée" in cl or "elevee" in cl else (("conf-l","Basse") if "basse" in cl else ("conf-m","Modérée"))

    # Render properly with escaped text
    st.markdown(f"""<div class="qa-card">
        <div class="qa-label">RÉPONSE</div>
        <div class="qa-text">{_esc(answer)}</div>
        <div class="qa-label">SOURCES</div>
        <div class="qa-text">{_esc(sources_t)}</div>
        <div class="qa-label">CONFIANCE</div>
        <div class="conf-badge {cc}"><strong>{cn}</strong> — {_esc(conf_t)}</div>
        <div class="src-box">
            <div style="font-size:12px;font-weight:600;color:#8b8ca7;margin-bottom:8px;">📚 Sources Documentaires Identifiées</div>
            <div style="font-size:12px;color:#b0b1c5;">{"  •  ".join(srcs)}</div>
        </div>
    </div>""", unsafe_allow_html=True)



    st.download_button("📥 JSON", json.dumps({"question":q,"response":resp,"model":mdl,"chunks":nk,"timestamp":datetime.now().isoformat()}, indent=2, ensure_ascii=False), f"qa_{datetime.now():%Y%m%d_%H%M%S}.json")


def main():
    mode, nk, col, gc = sidebar()
    if not gc: st.error("❌ GROQ_API_KEY manquante"); st.stop()
    st.markdown('<div class="main-header"><h1>Analyse de Dossier d\'Investissement</h1><p>Évaluation automatisée par RAG (Retrieval-Augmented Generation) du dossier FallahTech. Basé sur le corpus de 6 documents fournis.</p></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["📊 Évaluation Standard", "❓ Question Custom"])
    with t1: tab_eval(col, gc, mode, nk)
    with t2: tab_qa(col, gc, nk)

if __name__ == "__main__": main()
