"""
╔══════════════════════════════════════════════════════════════════════════╗
║  SIRA M&A — AFRIQUE CENTRALE                                              ║
║  Copilote IA de Deal Flow & pré-Due Diligence pour la CEMAC              ║
║  Société Africaine de Participation (SAPA)                               ║
║                                                                            ║
║  Stack : Streamlit · Groq Cloud (Llama 3.3 / 3.1) · Docker               ║
╚══════════════════════════════════════════════════════════════════════════╝
"""
import datetime as dt
import json
import os

import streamlit as st
import plotly.graph_objects as go
from pypdf import PdfReader

from core.llm import get_client, llm, parse_json, MODELS, DEFAULT_MODEL
from core.reference_cemac import (
    CEMAC_COUNTRIES, REGULATORS_CONTEXT, NEWS_SOURCES, FOKAM_THESIS_AXES,
    WEAK_SIGNALS_HINTS, SECTOR_OPTIONS,
)

# ══════════════════════════════════════════════════════════════════════════
#  ✏️  À PERSONNALISER AVANT L'ENTRETIEN
# ══════════════════════════════════════════════════════════════════════════
AUTHOR_NAME = "Romuald MBANA"
AUTHOR_TITLE = "Candidat — Entretien SAPA · Ingénieur Informaticien & Concepteur de l'agent"

st.set_page_config(page_title="Sira M&A · Afrique Centrale", page_icon="🦅",
                   layout="wide", initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════════════════════════
#  🎨  DESIGN
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;800&family=Inter:wght@300;400;500;600&display=swap');
:root{--gold:#D4AF37;--gold2:#F5D77A;--emerald:#1FAE7A;--navy:#050B18;--card:rgba(255,255,255,.045);--line:rgba(212,175,55,.25);}
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:radial-gradient(1200px 600px at 88% -8%,rgba(212,175,55,.15),transparent 60%),
       radial-gradient(900px 500px at -8% 8%,rgba(31,174,122,.14),transparent 60%),var(--navy);color:#E8ECF6;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0A1226,#050B18);border-right:1px solid var(--line);}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#fff;}
.hero{position:relative;overflow:hidden;padding:40px 44px;border-radius:24px;border:1px solid var(--line);
      background:linear-gradient(135deg,rgba(212,175,55,.14),rgba(10,18,38,.92) 55%,rgba(31,174,122,.14));
      box-shadow:0 20px 60px rgba(0,0,0,.5);margin-bottom:22px;}
.hero:before{content:"";position:absolute;inset:-50%;background:conic-gradient(from 0deg,transparent,rgba(212,175,55,.10),transparent 30%);
      animation:spin 16s linear infinite;}
@keyframes spin{to{transform:rotate(360deg);}}
.hero>*{position:relative;z-index:1;}
.badge{display:inline-block;padding:5px 14px;border-radius:99px;font-size:.7rem;letter-spacing:.13em;text-transform:uppercase;
      color:var(--gold2);border:1px solid var(--line);background:rgba(212,175,55,.08);margin:2px 4px 2px 0;}
.hero h1{font-size:2.7rem;font-weight:800;margin:14px 0 6px;line-height:1.1;
      background:linear-gradient(90deg,#fff,var(--gold2),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero p{color:#B8C2DC;font-size:1.02rem;max-width:780px;margin:0;}
.author{margin-top:20px;display:flex;align-items:center;gap:10px;font-size:.88rem;color:#C9D2EA;}
.author b{color:var(--gold2);font-weight:600;}
.dot{width:8px;height:8px;border-radius:50%;background:#3DDC97;box-shadow:0 0 12px #3DDC97;}
.kpi{padding:18px 20px;border-radius:16px;background:var(--card);border:1px solid var(--line);backdrop-filter:blur(8px);height:100%;}
.kpi:hover{border-color:var(--gold);}
.kpi small{color:#93A0C0;text-transform:uppercase;letter-spacing:.09em;font-size:.65rem;}
.kpi h2{margin:6px 0 0;font-size:1.55rem;color:var(--gold2)!important;}
.verdict{padding:24px;border-radius:20px;text-align:center;border:1px solid var(--line);background:var(--card);}
.verdict .v{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:800;}
.pillbox{padding:16px 18px;border-radius:14px;background:var(--card);border:1px solid var(--line);margin-bottom:10px;}
.pillbox b{color:var(--gold2);}
.stButton>button{background:linear-gradient(90deg,#B8901F,var(--gold),var(--gold2));color:#111;font-weight:700;border:0;
     border-radius:12px;padding:.7rem 1.4rem;box-shadow:0 8px 24px rgba(212,175,55,.3);}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 32px rgba(212,175,55,.5);color:#000;}
.stTabs [data-baseweb="tab-list"]{gap:6px;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{background:transparent;border-radius:10px 10px 0 0;color:#93A0C0;padding:10px 16px;}
.stTabs [aria-selected="true"]{color:var(--gold2)!important;background:rgba(212,175,55,.08);}
.stTextInput input,.stTextArea textarea,.stSelectbox>div>div{background:rgba(255,255,255,.05)!important;border-radius:10px!important;}
.memo{padding:28px 34px;border-radius:18px;background:rgba(255,255,255,.04);border:1px solid var(--line);}
.step{display:flex;align-items:center;gap:14px;padding:14px 18px;border-radius:14px;background:var(--card);
      border:1px solid var(--line);margin-bottom:8px;}
.step .n{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,var(--gold),var(--gold2));
      color:#111;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.flag{font-size:1.3rem;margin-right:6px;}
.compl-ok{color:#3DDC97;font-weight:700;} .compl-warn{color:#F5D77A;font-weight:700;} .compl-bad{color:#FF6B6B;font-weight:700;}
.foot{text-align:center;color:#6F7C9E;font-size:.8rem;margin-top:36px;padding:18px;border-top:1px solid var(--line);}
.foot b{color:var(--gold2);}
</style>
""", unsafe_allow_html=True)

COUNTRY_FLAGS = {"Cameroun": "🇨🇲", "Gabon": "🇬🇦", "République du Congo": "🇨🇬", "Tchad": "🇹🇩",
                 "République Centrafricaine": "🇨🇫", "Guinée Équatoriale": "🇬🇶"}


# ══════════════════════════════════════════════════════════════════════════
#  🧰  UTILITAIRES
# ══════════════════════════════════════════════════════════════════════════
def read_docs(files, char_limit: int) -> str:
    out = []
    for f in files or []:
        try:
            if f.name.lower().endswith(".pdf"):
                pages = [p.extract_text() or "" for p in PdfReader(f).pages]
                out.append(f"### {f.name}\n" + "\n".join(pages))
            else:
                out.append(f"### {f.name}\n" + f.read().decode("utf-8", errors="ignore"))
        except Exception as e:  # noqa: BLE001
            out.append(f"### {f.name}\n[Lecture impossible : {e}]")
    return "\n\n".join(out)[:char_limit]


def fmt(v, suffix=""):
    if v in (None, "", "N/D"):
        return "N/D"
    try:
        return f"{float(v):,.1f}".replace(",", " ") + suffix
    except Exception:
        return str(v)


def compliance_badge(level: str) -> str:
    cls = {"Conforme": "compl-ok", "À vérifier": "compl-warn", "Non conforme": "compl-bad"}.get(level, "")
    return f"<span class='{cls}'>● {level}</span>"


# ══════════════════════════════════════════════════════════════════════════
#  ⚙️  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🦅 Analyste M&A et Deal Flow")
    st.caption("Afrique Centrale · Société Africaine de Participation")

    api_key = st.text_input("🔑 Clé API Groq", type="password", value=os.getenv("GROQ_API_KEY", ""),
                            placeholder="gsk_...")
    model_label = st.selectbox("Modèle Llama (Groq)", list(MODELS.keys()))
    model = MODELS[model_label]

    with st.expander("🔒 Souveraineté & sécurité des données"):
        st.markdown("""
Compte tenu du caractère stratégique des dossiers d'investissement de la SAPA :
- En production, cette application doit être déployée sur un **cloud privé / VPC dédié**
  (ou hybride) et non sur une instance publique partagée.
- Groq propose des accords de **Zero Data Retention** en offre entreprise : à activer
  contractuellement pour garantir qu'aucun document confidentiel n'entre dans un jeu
  d'entraînement public.
- Recommandation : chiffrement au repos des pitch decks/PDF, accès nominatif au
  Comité d'Investissement, journalisation des analyses (piste d'audit).
""")

    st.divider()
    st.markdown("#### 🎯 Thèse d'investissement SAPA")
    countries = st.multiselect("Pays CEMAC couverts", list(CEMAC_COUNTRIES.keys()),
                               default=list(CEMAC_COUNTRIES.keys()))
    sectors = st.multiselect("Secteurs prioritaires", SECTOR_OPTIONS,
                             default=["Agro-industrie & agro-transformation", "Industrie manufacturière",
                                      "BTP & matériaux de construction"])
    ticket = st.slider("Ticket d'investissement (M USD)", 1, 100, (2, 30))
    stake = st.selectbox("Type de participation", ["Minoritaire (10-49%)", "Majoritaire (>50%)",
                                                    "Contrôle total", "Flexible"])
    weights_note = st.text_area("Critères FOKAM additionnels", height=90,
        value="Priorité aux PME industrielles familiales à fort potentiel, encore peu visibles à "
              "l'international, avec impact emploi local démontrable.")
    thesis = (f"Pays couverts : {', '.join(countries)} | Secteurs : {', '.join(sectors)} | "
              f"Ticket : {ticket[0]}–{ticket[1]} M USD | Participation : {stake} | "
              f"Critères FOKAM : {weights_note}")

# ══════════════════════════════════════════════════════════════════════════
#  🏠  HERO
# ══════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <span class="badge">Agent IA autonome</span><span class="badge">Zone CEMAC</span>
  <span class="badge">Groq · Llama 3.3</span>
  <h1>Sira M&amp;A — Afrique Centrale</h1>
  <p>Copilote de deal flow cartographiant, auditant et notant le tissu économique de la CEMAC :
     ingestion SYSCOHADA/OHADA, analyse des risques réglementaires COBAC/BEAC, scoring selon la
     thèse d'investissement de la SAPA et génération automatique de la note de cadrage.</p>
  <div class="author"><span class="dot"></span>Conçu et développé par <b>{AUTHOR_NAME}</b> · {AUTHOR_TITLE}</div>
</div>
""", unsafe_allow_html=True)

st.session_state.setdefault("deals", [])
st.session_state.setdefault("res", None)

tab_run, tab_res, tab_pipe, tab_about = st.tabs(
    ["🚀 Nouvelle analyse", "📊 Résultats du deal", "🗂️ Deal Flow CEMAC", "ℹ️ Architecture"])

# ══════════════════════════════════════════════════════════════════════════
#  🚀  ONGLET 1 — NOUVELLE ANALYSE
# ══════════════════════════════════════════════════════════════════════════
with tab_run:
    st.markdown("""
<div class="step"><div class="n">1</div><div><b>Ingestion SYSCOHADA / OHADA</b><br>
<span style="color:#93A0C0;font-size:.85rem">Extraction des états financiers normalisés et des documents juridiques</span></div></div>
<div class="step"><div class="n">2</div><div><b>Analyse des risques CEMAC</b><br>
<span style="color:#93A0C0;font-size:.85rem">Conformité BEAC / COBAC, risque pays, signaux faibles PME</span></div></div>
<div class="step"><div class="n">3</div><div><b>Scoring Thèse SAPA</b><br>
<span style="color:#93A0C0;font-size:.85rem">Modèle FOKAM : emploi local, valeur ajoutée, gouvernance, endettement</span></div></div>
<div class="step"><div class="n">4</div><div><b>Génération de la note de cadrage</b><br>
<span style="color:#93A0C0;font-size:.85rem">Synthèse pré-Due Diligence prête pour le Comité d'Investissement</span></div></div>
""", unsafe_allow_html=True)
    st.markdown("&nbsp;")

    c1, c2 = st.columns([1.1, 1])
    with c1:
        st.markdown("### Cible à analyser")
        company = st.text_input("Nom de l'entreprise cible", placeholder="Ex : SOSUCAM, SIAT Gabon, CFAO Congo…")
        cc1, cc2 = st.columns(2)
        country = cc1.selectbox("Pays", list(CEMAC_COUNTRIES.keys()))
        sector = cc2.text_input("Secteur d'activité précis", placeholder="Ex : Transformation agro-industrielle")
        notes = st.text_area("Contexte / origine du deal (optionnel)", height=90,
                             placeholder="Origine du deal, contact, opération envisagée, signal capté…")
    with c2:
        st.markdown("### Documents reçus")
        files = st.file_uploader(
            "Pitch decks, états financiers SYSCOHADA, statuts, RCCM, PV d'AG (PDF / TXT)",
            type=["pdf", "txt", "md", "csv"], accept_multiple_files=True)
        st.caption("💡 Sans document, l'agent s'appuie sur la veille web et la presse spécialisée CEMAC.")
        st.caption(f"📰 Sources suivies : {', '.join(s['nom'] for s in NEWS_SOURCES[:6])}…")

    st.markdown("&nbsp;")
    go_btn = st.button("⚡ Lancer l'agent Sira M&A", use_container_width=True)

    if go_btn:
        if not api_key:
            st.error("Renseignez votre clé API Groq dans la barre latérale.")
        elif not company:
            st.error("Indiquez le nom de l'entreprise cible.")
        else:
            client = get_client(api_key)
            country_info = CEMAC_COUNTRIES[country]
            ctx = (f"Cible : {company} | Pays : {country} ({country_info['plan_national']}) | "
                   f"Secteur : {sector or 'N/D'} | Notes : {notes or '-'}")
            press_list = ", ".join(f"{s['nom']} ({s['url']})" for s in NEWS_SOURCES)

            with st.status("🦅 Sira M&A travaille sur le dossier…", expanded=True) as status:
                try:
                    # ── Étape 1 : ingestion SYSCOHADA / OHADA ────────────────────
                    st.write("📄 **Étape 1/4** — Ingestion SYSCOHADA / OHADA")
                    docs = read_docs(files, char_limit=60000)
                    ext_prompt = f"""{ctx}
Tu extrais des données financières et juridiques au format SYSCOHADA révisé / droit OHADA.
Réponds UNIQUEMENT par un JSON strict :
{{"entreprise":str,"pays":str,"secteur":str,"annee_reference":str,"devise":"XAF"|"USD"|str,
"chiffre_affaires_musd":num|null,"ebitda_musd":num|null,"resultat_net_musd":num|null,
"dette_nette_musd":num|null,"capitaux_propres_musd":num|null,"tresorerie_musd":num|null,
"croissance_ca_pct":num|null,"marge_ebitda_pct":num|null,"ratio_dette_ebitda":num|null,
"effectif":num|null,"emplois_locaux_pct":num|null,"forme_juridique_ohada":str,
"actionnariat":str,"dirigeants":str,"activites":str,
"points_forts":[str],"risques_identifies":[str],
"anomalies_syscohada":[str] // provisions sous-évaluées, comptes courants d'associés, engagements hors bilan, etc.
}}
Mets null si l'information est absente. N'invente aucun chiffre. Convertis en millions USD quand c'est possible
(indique le taux/l'hypothèse retenue implicitement dans "devise" sinon).
DOCUMENTS FOURNIS :
{docs if docs else "[Aucun document fourni — utilise tes connaissances générales et signale l'absence de source primaire]"}"""
                    fin = parse_json(llm(client, model, "Tu es un analyste financier senior spécialisé dans les "
                        "états financiers SYSCOHADA et le droit OHADA, pour un fonds de private equity en Afrique "
                        "Centrale.", ext_prompt, web=not docs))

                    # ── Étape 2 : risques CEMAC (BEAC/COBAC) + signaux faibles ──
                    st.write("🌐 **Étape 2/4** — Risques réglementaires CEMAC & signaux faibles")
                    risk_prompt = f"""Cible : {company} ({country}, secteur : {sector or fin.get('secteur','N/D')}).
Contexte pays : {country_info}
Cadre réglementaire de référence : {REGULATORS_CONTEXT}
Presse spécialisée à privilégier pour la recherche : {press_list}
Signaux faibles à rechercher (modèle FOKAM de détection des PME d'élite) : {', '.join(WEAK_SIGNALS_HINTS)}

Mène une veille structurée et réponds en Markdown avec ces sections courtes :
## Présentation & actualité récente (12 derniers mois)
## Actionnariat, registre du commerce (RCCM) et gouvernance
## Faisabilité des flux financiers (BEAC — réglementation des changes CEMAC)
Indique explicitement si l'opération envisagée (apport en capital entrant, versement de dividendes ou sortie de
capitaux sortante) est susceptible de nécessiter une déclaration ou une autorisation préalable BEAC, et sous quel seuil.
## Conformité sectorielle (COBAC si secteur financier, sinon N/A)
## Litiges, sanctions, adverse media, exposition PEP
## Signaux faibles détectés (PME d'élite)
Liste les signaux concrets trouvés (marché public gagné, extension d'usine, levée de fonds, etc.) avec source.
## Concurrents principaux dans le pays/la sous-région
Cite tes sources (nom du média + URL si possible). Signale clairement ce qui n'est pas vérifiable."""
                    intel = llm(client, model, "Tu es analyste risques et conformité M&A spécialisé en zone CEMAC "
                        "(BEAC, COBAC, OHADA).", risk_prompt, web=True)

                    # ── Étape 3 : scoring thèse SAPA (modèle FOKAM) ─────────────
                    st.write("📈 **Étape 3/4** — Scoring Thèse SAPA (modèle FOKAM)")
                    axes_txt = "\n".join(f"- {k} : {v}" for k, v in FOKAM_THESIS_AXES.items())
                    sc_prompt = f"""THÈSE SAPA : {thesis}
AXES DU MODÈLE FOKAM À NOTER (0 à 10 chacun) :
{axes_txt}
CIBLE : {company}
DONNÉES FINANCIÈRES : {json.dumps(fin, ensure_ascii=False)}
VEILLE RISQUES & SIGNAUX : {intel[:6000]}
Réponds UNIQUEMENT par un JSON strict :
{{"scores":{{"Alignement stratégique CEMAC":n,"Impact emploi local & ancrage territorial":n,
"Valeur ajoutée industrielle":n,"Solidité du management & gouvernance":n,
"Santé financière & endettement":n,"Conformité réglementaire CEMAC/OHADA":n,"Potentiel de sortie":n}},
"score_global":n,"niveau_conformite":"Conforme"|"À vérifier"|"Non conforme",
"recommandation":"GO"|"GO SOUS CONDITIONS"|"NO GO","justification":str}}"""
                    score = parse_json(llm(client, model, "Tu es membre du Comité d'Investissement de la SAPA, "
                        "rigoureux et exigeant sur la conformité CEMAC/OHADA.", sc_prompt))

                    # ── Étape 4 : note de cadrage ────────────────────────────────
                    st.write("📝 **Étape 4/4** — Génération de la note de cadrage")
                    memo_prompt = f"""Rédige en français une NOTE DE CADRAGE D'INVESTISSEMENT (pré-Due Diligence) pour
le Comité d'Investissement de la Société Africaine de Participation (SAPA), dans le cadre du projet Sira M&A -
Afrique Centrale.
THÈSE SAPA : {thesis}
CIBLE : {company} | {ctx}
DONNÉES FINANCIÈRES SYSCOHADA : {json.dumps(fin, ensure_ascii=False)}
SCORING FOKAM : {json.dumps(score, ensure_ascii=False)}
VEILLE RISQUES CEMAC & CONFORMITÉ : {intel[:7000]}
Structure imposée (Markdown) :
## 1. Synthèse exécutive (verdict en 5 lignes)
## 2. Présentation de la cible et ancrage local
## 3. Analyse financière SYSCOHADA (chiffres clés, anomalies éventuelles)
## 4. Alignement avec la thèse SAPA — modèle FOKAM (détailler chaque axe noté)
## 5. Cadrage réglementaire CEMAC (BEAC — faisabilité des flux, COBAC si applicable, OHADA)
## 6. Matrice des risques (tableau : risque | niveau | mitigation)
## 7. Signaux faibles & potentiel de développement (PME d'élite)
## 8. Points à vérifier en Due Diligence approfondie
## 9. Recommandation et prochaines étapes
Ton professionnel, factuel, chiffré, en français des affaires. Signale toute donnée non vérifiée.
N'invente aucun chiffre ni aucune source."""
                    memo = llm(client, model, "Tu es directeur des investissements de la SAPA, expert du droit OHADA "
                        "et de la réglementation CEMAC.", memo_prompt, temperature=0.3)

                    st.session_state.res = dict(company=company, country=country, sector=sector or fin.get("secteur", "N/D"),
                        fin=fin, intel=intel, score=score, memo=memo, date=dt.date.today().strftime("%d/%m/%Y"))
                    st.session_state.deals.append(dict(
                        Date=st.session_state.res["date"], Cible=company, Pays=country,
                        Secteur=sector or fin.get("secteur", "N/D"),
                        Score=score.get("score_global", "N/D"),
                        Conformité=score.get("niveau_conformite", "N/D"),
                        Décision=score.get("recommandation", "N/D")))
                    status.update(label="✅ Analyse terminée — consultez l'onglet « Résultats du deal »", state="complete")
                    st.balloons()
                except Exception as e:  # noqa: BLE001
                    status.update(label="❌ Erreur", state="error")
                    st.error(f"Erreur : {e}")

# ══════════════════════════════════════════════════════════════════════════
#  📊  ONGLET 2 — RÉSULTATS
# ══════════════════════════════════════════════════════════════════════════
with tab_res:
    R = st.session_state.res
    if not R:
        st.info("Lancez une analyse dans l'onglet « Nouvelle analyse » pour afficher les résultats ici.")
    else:
        fin, score = R["fin"], R["score"]
        flag = COUNTRY_FLAGS.get(R["country"], "")
        st.markdown(f"## {flag} {R['company']} <span class='badge'>{R['country']}</span>"
                    f"<span class='badge'>{R['sector']}</span>", unsafe_allow_html=True)

        k = st.columns(5)
        kpis = [("Chiffre d'affaires", fmt(fin.get("chiffre_affaires_musd"), " M$")),
                ("EBITDA", fmt(fin.get("ebitda_musd"), " M$")),
                ("Marge EBITDA", fmt(fin.get("marge_ebitda_pct"), " %")),
                ("Dette / EBITDA", fmt(fin.get("ratio_dette_ebitda"), "x")),
                ("Emplois locaux", fmt(fin.get("emplois_locaux_pct"), " %"))]
        for col, (lab, val) in zip(k, kpis):
            col.markdown(f"<div class='kpi'><small>{lab}</small><h2>{val}</h2></div>", unsafe_allow_html=True)
        st.markdown("&nbsp;")

        v1, v2 = st.columns([1, 1.3])
        reco = str(score.get("recommandation", "N/D"))
        niveau = str(score.get("niveau_conformite", "N/D"))
        color = {"GO": "#3DDC97", "GO SOUS CONDITIONS": "#F5D77A", "NO GO": "#FF5C6C"}.get(reco, "#B8C2DC")
        with v1:
            g = go.Figure(go.Indicator(mode="gauge+number", value=float(score.get("score_global", 0) or 0),
                number={"font": {"color": color, "size": 50}},
                gauge={"axis": {"range": [0, 10], "tickcolor": "#93A0C0"}, "bar": {"color": color},
                       "bgcolor": "rgba(255,255,255,.05)", "borderwidth": 0}))
            g.update_layout(height=230, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=15, b=0, l=20, r=20),
                            font={"color": "#fff"})
            st.plotly_chart(g, use_container_width=True)
            st.markdown(f"<div class='verdict'><small style='color:#93A0C0'>RECOMMANDATION</small>"
                        f"<div class='v' style='color:{color}'>{reco}</div>"
                        f"<p style='margin:6px 0 0'>Conformité CEMAC/OHADA : {compliance_badge(niveau)}</p>"
                        f"<p style='color:#B8C2DC;font-size:.88rem'>{score.get('justification', '')}</p></div>",
                        unsafe_allow_html=True)
        with v2:
            sc = score.get("scores", {})
            if sc:
                labels, vals = list(sc.keys()), [float(x or 0) for x in sc.values()]
                r = go.Figure(go.Scatterpolar(r=vals + vals[:1], theta=labels + labels[:1], fill="toself",
                    line=dict(color="#D4AF37", width=3), fillcolor="rgba(212,175,55,.25)"))
                r.update_layout(polar=dict(bgcolor="rgba(255,255,255,.03)",
                    radialaxis=dict(range=[0, 10], gridcolor="rgba(255,255,255,.12)", tickfont=dict(color="#93A0C0")),
                    angularaxis=dict(gridcolor="rgba(255,255,255,.12)", tickfont=dict(size=10))),
                    paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E8ECF6"), height=400,
                    title="Modèle FOKAM — alignement avec la thèse SAPA", showlegend=False)
                st.plotly_chart(r, use_container_width=True)

        sub = st.tabs(["📝 Note de cadrage", "🌐 Risques CEMAC & signaux faibles", "🔎 Données SYSCOHADA extraites"])

        with sub[0]:
            st.markdown("<div class='memo'>", unsafe_allow_html=True)
            st.markdown(f"**Sira M&A — Note de cadrage** · {R['date']} · *Préparée par {AUTHOR_NAME}*")
            st.markdown(R["memo"])
            st.markdown("</div>", unsafe_allow_html=True)
            d1, d2 = st.columns(2)
            full_md = f"# Note de cadrage — {R['company']}\n*Sira M&A · SAPA · {R['date']} · {AUTHOR_NAME}*\n\n{R['memo']}"
            d1.download_button("⬇️ Télécharger (Markdown)", full_md, f"note_cadrage_{R['company']}.md",
                               use_container_width=True)
            html = ("<html><meta charset='utf-8'><body style='font-family:Arial;max-width:900px;margin:40px auto'>"
                    f"<h1>Note de cadrage — {R['company']}</h1><p><i>Sira M&A · SAPA · {R['date']} · {AUTHOR_NAME}</i></p>"
                    f"<pre style='white-space:pre-wrap;font-family:Arial'>{R['memo']}</pre></body></html>")
            d2.download_button("⬇️ Télécharger (HTML)", html, f"note_cadrage_{R['company']}.html",
                               use_container_width=True)

        with sub[1]:
            st.markdown(R["intel"])

        with sub[2]:
            a, b = st.columns(2)
            a.markdown("#### ✅ Points forts")
            for x in fin.get("points_forts", []) or []:
                a.markdown(f"- {x}")
            b.markdown("#### ⚠️ Risques identifiés")
            for x in fin.get("risques_identifies", []) or []:
                b.markdown(f"- {x}")
            if fin.get("anomalies_syscohada"):
                st.markdown("#### 🧮 Anomalies SYSCOHADA détectées")
                for x in fin.get("anomalies_syscohada", []):
                    st.markdown(f"- {x}")
            with st.expander("JSON brut extrait"):
                st.json(fin)

# ══════════════════════════════════════════════════════════════════════════
#  🗂️  ONGLET 3 — DEAL FLOW CEMAC
# ══════════════════════════════════════════════════════════════════════════
with tab_pipe:
    st.markdown("### Pipeline de deal flow — session en cours")
    if st.session_state.deals:
        filt_country = st.multiselect("Filtrer par pays", list(CEMAC_COUNTRIES.keys()))
        rows = st.session_state.deals
        if filt_country:
            rows = [r for r in rows if r["Pays"] in filt_country]
        st.dataframe(rows, use_container_width=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Deals analysés", len(rows))
        go_count = sum(1 for r in rows if r["Décision"] == "GO")
        m2.metric("Recommandations GO", go_count)
        m3.metric("Pays couverts", len({r["Pays"] for r in rows}))
    else:
        st.info("Aucun deal analysé pour le moment dans cette session.")

    st.markdown("&nbsp;")
    st.markdown("### 🗺️ Repères macro par pays CEMAC")
    cols = st.columns(3)
    for i, (name, info) in enumerate(CEMAC_COUNTRIES.items()):
        with cols[i % 3]:
            st.markdown(f"""<div class="pillbox">
<b>{COUNTRY_FLAGS.get(name,'')} {name}</b><br>
<span style="font-size:.82rem;color:#B8C2DC">{info['note_macro']}</span><br>
<span style="font-size:.78rem;color:#93A0C0">Plan national : {info['plan_national']}</span></div>""",
                       unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
#  ℹ️  ONGLET 4 — ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════
with tab_about:
    st.markdown("### Architecture du projet Sira M&A")
    st.markdown("""
```
[Ingestion SYSCOHADA / OHADA] → [Analyse des Risques CEMAC] → [Scoring Thèse SAPA] → [Génération Note de Cadrage]
```

**Stack technique**
- **Interface** : Streamlit (dashboard, formulaires, visualisations Plotly)
- **Intelligence artificielle** : Groq Cloud — modèles Llama 3.3 70B Versatile / Llama 3.1 8B Instant (Meta),
  plus Groq Compound pour la recherche web en temps réel intégrée au modèle
- **Portabilité** : conteneurisation Docker + orchestration Docker Compose
- **Documents** : extraction PDF via `pypdf`, lecture d'états financiers SYSCOHADA et de documents juridiques OHADA

**Sources et référentiels intégrés au moteur de prompts**
- Marché : BVMAC (bourse unique CEMAC, Douala) et son régulateur COSUMAF (Libreville)
- Réglementation : BEAC (réglementation des changes), COBAC (secteur bancaire/microfinance), droit OHADA & CCJA,
  référentiel comptable SYSCOHADA révisé
- Presse spécialisée : Investir au Cameroun, EcoMatin, Le Nouveau Gabon, Agence Ecofin, Financial Afrik, etc.

**Souveraineté des données** — voir le détail dans la barre latérale (« Souveraineté & sécurité des données »).
En production, ce copilote est conçu pour être hébergé sur un environnement cloud privé ou hybride dédié à la
SAPA, avec option Zero Data Retention côté fournisseur de modèle.
""")

st.markdown(f"<div class='foot'>© {dt.date.today().year} Société Africaine de Participation · Sira M&A — Afrique "
            f"Centrale · Développé par <b>{AUTHOR_NAME}</b> · Propulsé par Groq &amp; Llama (Meta) · Dockerisé<br>"
            "Outil d'aide à la décision : les analyses sont préliminaires et doivent être vérifiées en Due Diligence.</div>",
            unsafe_allow_html=True)
