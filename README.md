# 🦅 SAPA M&A — Afrique Centrale

Copilote IA d'analyse M&A et de Deal Flow pour la **Société Africaine de Participation (SAPA)**,
spécialisé sur la zone **CEMAC** (Cameroun, Gabon, Congo, Tchad, RCA, Guinée Équatoriale).

**Stack** : Streamlit · Groq Cloud (Llama 3.3 / 3.1, Meta) · Docker

```
[Ingestion SYSCOHADA/OHADA] → [Analyse des Risques CEMAC] → [Scoring Thèse SAPA] → [Génération Note de Cadrage]
```

## 1. Prise en main

1. Ouvrir `app.py` et remplacer `AUTHOR_NAME` par votre nom.
2. Copier `.env.example` en `.env` et renseigner `GROQ_API_KEY`
   (obtenue sur https://console.groq.com/keys — offre gratuite disponible).
   La clé peut aussi être saisie directement dans la barre latérale de l'application.

## 2. Lancement avec Docker (recommandé)

```bash
docker compose up --build
```

Application disponible sur **http://localhost:8501**.

Pour arrêter : `docker compose down`.

## 3. Lancement sans Docker

```bash
python -m venv .venv && source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 4. Structure du projet

```
sira-ma-agent/
├── app.py                     # Application Streamlit (interface + workflow)
├── core/
│   ├── llm.py                 # Client Groq, retry, veille web
│   └── reference_cemac.py     # Référentiel CEMAC/OHADA/BVMAC injecté dans les prompts
├── .streamlit/config.toml     # Thème visuel
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 5. Modèles utilisés (Groq)

| Modèle | Usage |
|---|---|
| `llama-3.3-70b-versatile` | Analyse financière, scoring, rédaction de la note de cadrage (par défaut) |
| `llama-3.1-8b-instant` | Tri rapide / extraction, faible latence |
| `groq/compound` | Veille web CEMAC avec recherche intégrée |

> **Note** : Meta/Groq a retiré les modèles **Llama 3.2** du catalogue Groq (remplacés notamment par
> Llama 4 Scout pour la vision). L'application utilise donc les modèles Llama actuellement servis en
> production par Groq (3.3 70B et 3.1 8B), ce qui est indiqué en toutes lettres dans l'interface.

## 6. Souveraineté des données

Ce projet est un **prototype fonctionnel** destiné à la démonstration. Pour un déploiement réel au sein
de la SAPA, il est recommandé de :

- héberger l'application sur un **cloud privé / VPC dédié** (ou hybride), non partagé ;
- activer, côté fournisseur du modèle, une option de type **Zero Data Retention** ;
- chiffrer au repos les documents confidentiels (pitch decks, PV d'AG, états financiers) ;
- restreindre l'accès au Comité d'Investissement et journaliser chaque analyse.

## 7. Déploiement sur Streamlit Community Cloud

Le mode Groq fonctionne directement sur Streamlit Cloud (contrairement à un LLM local type Ollama).
Renseignez `GROQ_API_KEY` dans **Settings → Secrets** de l'application déployée.

## Avertissement

Les analyses produites sont des synthèses **pré-Due Diligence**, destinées à accélérer le premier tri
du deal flow. Elles ne remplacent pas une Due Diligence juridique, financière et fiscale complète.
