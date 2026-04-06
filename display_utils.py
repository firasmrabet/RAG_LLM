"""
display_utils.py — Affichage HTML professionnel pour FallahTech RAG Colab
"""
import re, textwrap
from IPython.display import display, HTML

# ── Palette de couleurs ────────────────────────────────────────────────────────
COLORS = {
    "green":  "#10b981", "green_bg":  "#d1fae5",
    "blue":   "#3b82f6", "blue_bg":   "#dbeafe",
    "amber":  "#f59e0b", "amber_bg":  "#fef3c7",
    "red":    "#ef4444", "red_bg":    "#fee2e2",
    "dark":   "#0f172a", "card":      "#1e293b",
    "border": "#334155", "text":      "#e2e8f0",
    "muted":  "#94a3b8",
}

CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  .ft-root { font-family: 'Inter', sans-serif; color: #e2e8f0; }
  .ft-card { background: #1e293b; border: 1px solid #334155; border-radius: 12px;
             padding: 20px 24px; margin: 12px 0; }
  .ft-header { background: linear-gradient(135deg,#064e3b,#065f46);
               border-radius:12px; padding:24px; margin-bottom:16px; }
  .ft-score-pill { display:inline-flex; align-items:center; gap:6px;
                   padding:4px 14px; border-radius:999px; font-weight:600;
                   font-size:0.85rem; }
  .ft-bar-bg { background:#334155; border-radius:999px; height:10px; width:100%; margin:8px 0; }
  .ft-bar-fill { border-radius:999px; height:10px; transition:width .4s; }
  .ft-table { width:100%; border-collapse:collapse; font-size:0.9rem; }
  .ft-table th { background:#0f172a; color:#94a3b8; padding:10px 14px;
                 text-align:left; font-weight:500; }
  .ft-table td { padding:10px 14px; border-top:1px solid #334155; }
  .ft-verdict { border-radius:12px; padding:20px 24px; margin:16px 0; }
  .ft-source-badge { display:inline-block; background:#1e3a5f; color:#93c5fd;
                     border:1px solid #3b82f6; border-radius:6px; padding:2px 10px;
                     font-size:0.75rem; margin:2px; }
  .ft-chunk-box { background:#0f172a; border:1px solid #1e40af; border-radius:8px;
                  padding:10px 14px; margin:6px 0; font-size:0.8rem; color:#94a3b8; }
  .ft-section-title { font-size:0.7rem; font-weight:700; letter-spacing:0.1em;
                      text-transform:uppercase; color:#64748b; margin-bottom:8px; }
  .ft-analysis { line-height:1.7; color:#cbd5e1; font-size:0.88rem; }
  .ft-analysis p { margin:8px 0; }
  .ft-tag { display:inline-block; padding:2px 8px; border-radius:4px;
            font-size:0.72rem; font-weight:600; margin-right:4px; }
  .ft-divider { border:none; border-top:1px solid #334155; margin:16px 0; }
  .ft-q-box { background:#1e293b; border-left:4px solid #3b82f6;
              border-radius:0 8px 8px 0; padding:14px 18px; margin:10px 0; }
  .ft-conf-badge { display:inline-flex; align-items:center; gap:6px;
                   padding:6px 16px; border-radius:8px; font-weight:600; font-size:0.85rem; }
  .ft-batch-row { background:#1e293b; border:1px solid #334155; border-radius:8px;
                  padding:14px 18px; margin:8px 0; }
  .ft-num-badge { display:inline-flex; align-items:center; justify-content:center;
                  width:28px; height:28px; border-radius:50%; background:#1e40af;
                  color:#93c5fd; font-weight:700; font-size:0.85rem; flex-shrink:0; }
</style>
"""

def _score_meta(s):
    if s >= 7.5: return COLORS["green"],  COLORS["green_bg"],  "🟢", "Excellent"
    if s >= 6.0: return COLORS["blue"],   COLORS["blue_bg"],   "🔵", "Bon"
    if s >= 4.5: return COLORS["amber"],  COLORS["amber_bg"],  "🟡", "Moyen"
    return             COLORS["red"],    COLORS["red_bg"],    "🔴", "Faible"

def _fmt_analysis(text):
    """Convert plain text analysis to styled HTML paragraphs."""
    lines = text.strip().split("\n")
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Bold [SOURCE: ...] citations
        line = re.sub(r'\[SOURCE:\s*([^\]]+)\]',
                      r'<span style="color:#60a5fa;font-weight:500">[📄 \1]</span>', line)
        # Bullet points
        if line.startswith(("- ", "• ", "* ")):
            out.append(f'<li style="margin:4px 0">{line[2:]}</li>')
        else:
            out.append(f'<p>{line}</p>')
    html = "\n".join(out)
    # Wrap consecutive <li> in <ul>
    html = re.sub(r'(<li.*?</li>\n?)+',
                  lambda m: f'<ul style="margin:6px 0 6px 16px;padding:0">{m.group()}</ul>', html)
    return html


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION A — Affichage Évaluation Standard
# ═══════════════════════════════════════════════════════════════════════════════

def display_evaluation_header(num_chunks):
    display(HTML(CSS + f"""
    <div class="ft-root">
      <div class="ft-header">
        <div style="display:flex;align-items:center;gap:12px">
          <span style="font-size:2rem">🌿</span>
          <div>
            <div style="font-size:1.4rem;font-weight:700;color:#fff">FallahTech SARL — Évaluation RAG</div>
            <div style="color:#6ee7b7;font-size:0.85rem;margin-top:4px">
              Analyse de Dossier Série A · {num_chunks} chunks/critère · Groq Llama-3.1
            </div>
          </div>
        </div>
      </div>
    </div>
    """))


def display_criterion_result(r, index, total):
    col, bg, emoji, label = _score_meta(r["score"])
    pct = r["score"] * 10
    analysis_html = _fmt_analysis(r["analysis"])
    sources_html = "".join(
        f'<span class="ft-source-badge">📄 {s}</span>' for s in r["sources"]
    )
    chunks_html = "".join(
        f'<div class="ft-chunk-box">📄 <b style="color:#93c5fd">{ch["source"]}</b> — '
        f'{ch["text"][:160].strip()}…</div>'
        for ch in r["raw"][:3]
    )

    display(HTML(f"""
    <div class="ft-root">
      <div class="ft-card">
        <!-- En-tête critère -->
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
          <div style="display:flex;align-items:center;gap:10px">
            <span style="font-size:1.6rem">{r["icon"]}</span>
            <div>
              <div style="font-weight:700;font-size:1.05rem">{r["name"]}</div>
              <div style="color:{COLORS['muted']};font-size:0.78rem">
                Critère {index}/{total} · Poids <b style="color:#e2e8f0">{int(r['weight']*100)}%</b>
              </div>
            </div>
          </div>
          <div style="text-align:right">
            <div style="font-size:2rem;font-weight:800;color:{col}">{r["score"]:.1f}<span style="font-size:1rem;color:{COLORS['muted']}">/10</span></div>
            <span class="ft-score-pill" style="background:{bg}20;color:{col};border:1px solid {col}40">
              {emoji} {label}
            </span>
          </div>
        </div>

        <!-- Barre de progression -->
        <div class="ft-bar-bg" style="margin-top:14px">
          <div class="ft-bar-fill" style="width:{pct}%;background:{col}"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:{COLORS['muted']}">
          <span>0</span><span>Modèle: {r["model"]}</span><span>10</span>
        </div>

        <hr class="ft-divider">

        <!-- Analyse -->
        <div class="ft-section-title">💬 Analyse</div>
        <div class="ft-analysis">{analysis_html}</div>

        <hr class="ft-divider">

        <!-- Sources -->
        <div class="ft-section-title">📚 Sources documentaires</div>
        <div style="margin-bottom:12px">{sources_html}</div>

        <!-- Chunks RAG -->
        <div class="ft-section-title">🔬 Extraits RAG utilisés</div>
        {chunks_html}
      </div>
    </div>
    """))


def display_final_verdict(results, final):
    if final >= 7.5:
        v_color, v_bg, verdict = COLORS["green"], "#064e3b", "✅ INVESTIR"
        vdesc = "Le dossier présente un profil risque/rendement excellent."
    elif final >= 5.0:
        v_color, v_bg, verdict = COLORS["amber"], "#431a00", "⚠️ INVESTIR SOUS CONDITIONS"
        vdesc = ("Globalement favorable. Clauses de protection recommandées sur la liquidité "
                 "(ratio courant 1,56 en baisse) et les dettes fournisseurs (×15 en 1 an).")
    else:
        v_color, v_bg, verdict = COLORS["red"], "#450a0a", "❌ NO-GO"
        vdesc = "Risques significatifs identifiés. Ne pas investir."

    rows = ""
    for r in results:
        col, _, _, _ = _score_meta(r["score"])
        rows += f"""
        <tr>
          <td><b>{r['icon']}</b> {r['name']}</td>
          <td style="text-align:center"><b style="color:{col}">{r['score']:.1f}</b></td>
          <td style="text-align:center;color:{COLORS['muted']}">{int(r['weight']*100)}%</td>
          <td style="text-align:center"><b>{r['score']*r['weight']:.2f}</b></td>
        </tr>"""

    display(HTML(f"""
    <div class="ft-root">
      <!-- Verdict card -->
      <div class="ft-verdict" style="background:{v_bg};border:1px solid {v_color}40;margin-top:24px">
        <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
          <div>
            <div style="font-size:2.4rem;font-weight:900;color:{v_color}">{final:.2f}<span style="font-size:1rem;color:{COLORS['muted']}">/10</span></div>
            <div style="font-size:1.1rem;font-weight:700;color:#fff;margin-top:2px">Score Global Pondéré</div>
          </div>
          <div style="flex:1;min-width:220px">
            <div style="font-size:1.2rem;font-weight:800;color:{v_color}">{verdict}</div>
            <div style="color:#cbd5e1;font-size:0.85rem;margin-top:6px;line-height:1.5">{vdesc}</div>
          </div>
        </div>
      </div>

      <!-- Tableau de scoring -->
      <div class="ft-card" style="margin-top:12px">
        <div class="ft-section-title">📊 Tableau de Scoring Pondéré</div>
        <table class="ft-table">
          <thead>
            <tr>
              <th>Critère</th>
              <th style="text-align:center">Score /10</th>
              <th style="text-align:center">Poids</th>
              <th style="text-align:center">Pondéré</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
          <tfoot>
            <tr style="border-top:2px solid #475569">
              <td colspan="3" style="font-weight:700;color:#e2e8f0">Score Global Pondéré</td>
              <td style="text-align:center;font-weight:800;font-size:1.05rem;color:{v_color}">{final:.2f}</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
    """))


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION B — Affichage Question Custom
# ═══════════════════════════════════════════════════════════════════════════════

def display_qa_result(question, answer, sources_txt, conf_txt, srcs, raw_chunks, model):
    cl = conf_txt.lower()
    if "élevée" in cl or "elevee" in cl:
        conf_color, conf_label = COLORS["green"], "🟢 Confiance Élevée"
    elif "basse" in cl:
        conf_color, conf_label = COLORS["red"],   "🔴 Confiance Basse"
    else:
        conf_color, conf_label = COLORS["amber"],  "🟡 Confiance Modérée"

    answer_html = _fmt_analysis(answer)
    srcs_badges = "".join(f'<span class="ft-source-badge">📄 {s}</span>' for s in srcs)
    chunks_html = "".join(
        f'<div class="ft-chunk-box">📄 <b style="color:#93c5fd">{ch["source"]}</b> — '
        f'{ch["text"][:160].strip()}…</div>'
        for ch in raw_chunks[:4]
    )
    src_lines = "".join(
        f'<li>{l.strip()}</li>' for l in sources_txt.split("\n") if l.strip()
    )

    display(HTML(f"""
    <div class="ft-root">
      <div class="ft-card">
        <!-- Question -->
        <div class="ft-section-title">❓ Question</div>
        <div class="ft-q-box" style="font-size:1rem;font-weight:500;color:#e2e8f0">
          {question}
        </div>
        <div style="color:{COLORS['muted']};font-size:0.78rem;margin-top:4px">
          Modèle: {model} · {len(raw_chunks)} chunks récupérés depuis {len(srcs)} document(s)
        </div>

        <hr class="ft-divider">

        <!-- Réponse -->
        <div class="ft-section-title">💬 Réponse</div>
        <div class="ft-analysis">{answer_html}</div>

        <hr class="ft-divider">

        <!-- Sources -->
        <div style="display:flex;gap:24px;flex-wrap:wrap">
          <div style="flex:1;min-width:200px">
            <div class="ft-section-title">📚 Sources citées</div>
            <ul style="margin:0;padding-left:16px;color:#cbd5e1;font-size:0.85rem;line-height:1.8">
              {src_lines}
            </ul>
          </div>
          <div>
            <div class="ft-section-title">🎯 Niveau de confiance</div>
            <span class="ft-conf-badge" style="background:{conf_color}20;color:{conf_color};border:1px solid {conf_color}40">
              {conf_label}
            </span>
            <div style="color:{COLORS['muted']};font-size:0.78rem;margin-top:8px;max-width:300px;line-height:1.5">
              {conf_txt[:250] if conf_txt else "—"}
            </div>
          </div>
        </div>

        <hr class="ft-divider">

        <!-- Documents sources -->
        <div class="ft-section-title">🗂️ Documents sources</div>
        <div style="margin-bottom:10px">{srcs_badges}</div>

        <!-- Chunks RAG -->
        <div class="ft-section-title">🔬 Extraits RAG récupérés</div>
        {chunks_html}
      </div>
    </div>
    """))


# ═══════════════════════════════════════════════════════════════════════════════
#  BONUS — Affichage Batch Q&A
# ═══════════════════════════════════════════════════════════════════════════════

def display_batch_header(n):
    display(HTML(f"""
    <div class="ft-root">
      <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:12px;
                  padding:20px 24px;margin-bottom:4px">
        <div style="font-size:1.2rem;font-weight:700;color:#a5b4fc">
          🔁 Batch Q&A — {n} questions
        </div>
        <div style="color:#818cf8;font-size:0.82rem;margin-top:4px">
          Réponses concises · Groq Llama-3.1
        </div>
      </div>
    </div>
    """))


def display_batch_result(i, total, item):
    srcs_badges = "".join(
        f'<span class="ft-source-badge">📄 {s}</span>' for s in item["sources"][:3]
    )
    answer_html = _fmt_analysis(item["answer"])
    display(HTML(f"""
    <div class="ft-root">
      <div class="ft-batch-row">
        <div style="display:flex;align-items:flex-start;gap:12px">
          <span class="ft-num-badge">{i}</span>
          <div style="flex:1">
            <div style="font-weight:600;color:#e2e8f0;margin-bottom:8px">{item['question']}</div>
            <div class="ft-analysis" style="font-size:0.85rem">{answer_html}</div>
            <div style="margin-top:8px">{srcs_badges}</div>
            <div style="color:{COLORS['muted']};font-size:0.72rem;margin-top:6px">
              Modèle: {item['model']}
            </div>
          </div>
        </div>
      </div>
    </div>
    """))


def display_batch_footer(n, filename):
    display(HTML(f"""
    <div class="ft-root">
      <div style="background:#14532d;border:1px solid #16a34a;border-radius:10px;
                  padding:14px 20px;margin-top:8px;color:#bbf7d0;font-size:0.9rem">
        ✅ <b>{n}</b> réponses générées et exportées → <code>{filename}</code>
      </div>
    </div>
    """))
