# 🦅 Sira M&A — Afrique Centrale est consultable via ce lien : https://sapa-deal-flow-agent-ug9zswyacrbcznu4fqijch.streamlit.app/

**Copilote IA d'analyse M&A et de Deal Flow pour la Société Africaine de Participation (SAPA)**

> *« Sira »* — la voie, le chemin, dans plusieurs langues d'Afrique de l'Ouest et du Centre.
> Ce projet trace le chemin d'une opportunité d'investissement, du premier signal capté sur le
> terrain jusqu'à la note de cadrage prête pour le Comité d'Investissement.

---

## 1. Description du projet

Sira M&A est un agent d'intelligence artificielle qui automatise le tri initial et l'analyse de
conformité des opportunités d'investissement en zone **CEMAC** (Cameroun, Gabon, République du
Congo, Tchad, République Centrafricaine, Guinée Équatoriale).

Le cœur de métier d'une holding de participation est de repérer et d'évaluer de nouvelles
entreprises dans lesquelles investir. C'est un exercice à fort volume et à forte exigence de
rigueur : chaque dossier reçu (pitch deck, bilan, statuts) doit être lu, comparé au marché, confronté
à la réglementation locale, puis noté selon la thèse d'investissement de la maison. Sira M&A prend en
charge ce premier tri, du scan de la donnée brute jusqu'à la note de synthèse, en suivant un
enchaînement en quatre temps :

```
[Ingestion SYSCOHADA / OHADA] → [Analyse des Risques CEMAC] → [Scoring Thèse SAPA] → [Génération Note de Cadrage]
```

1. **Ingestion SYSCOHADA / OHADA** — l'agent lit les documents transmis (pitch decks, états
   financiers, statuts, procès-verbaux d'assemblée) et en extrait les données financières et
   juridiques clés, en reconnaissant le vocabulaire comptable propre au référentiel SYSCOHADA révisé
   et au droit des sociétés OHADA.
2. **Analyse des risques CEMAC** — l'agent confronte la cible au cadre réglementaire régional : la
   réglementation des changes de la BEAC pour les flux financiers transfrontaliers, la supervision
   prudentielle de la COBAC pour le secteur financier, et mène une veille dans la presse économique
   spécialisée de la sous-région à la recherche de signaux faibles (marché public gagné, extension
   d'usine, levée de fonds) et de risques réputationnels.
3. **Scoring Thèse SAPA** — l'agent note la cible sur sept axes qui traduisent la vision
   d'investissement de la SAPA en critères mesurables : alignement stratégique, impact sur l'emploi
   local, valeur ajoutée industrielle, solidité de la gouvernance, santé financière, conformité
   réglementaire et potentiel de sortie.
4. **Génération de la note de cadrage** — l'agent rédige une synthèse structurée en neuf sections,
   prête à être discutée en Comité d'Investissement, avec une matrice des risques et une liste des
   points à vérifier en Due Diligence approfondie.

---

## 2. Pertinence stratégique pour la SAPA

Un outil panafricain générique perdrait l'essentiel de ce qui fait la spécificité — et la difficulté —
du marché d'Afrique Centrale. Sira M&A a été conçu pour coller précisément au terrain d'action et à la
philosophie d'investissement de la SAPA.

**Maîtrise du risque de change et de conformité CEMAC.** La zone CEMAC partage une monnaie commune, le
FCFA, et une réglementation des changes édictée par la BEAC qui encadre strictement les flux de
capitaux entrants et sortants. Un investissement mal préparé sur ce plan peut bloquer un apport en
capital ou un rapatriement de dividendes pendant des mois. L'agent alerte systématiquement l'équipe
M&A sur la faisabilité de ces flux dès le stade du pré-tri, avant que la question ne se pose en pleine
négociation.

**Détection fine des PME d'élite, dans l'esprit du modèle porté par le Dr FOKAM.** Le développement
par la PME locale suppose de savoir repérer les entreprises familiales ou les PME industrielles en
forte croissance avant qu'elles n'aient une visibilité internationale. L'agent est programmé pour
chercher ces signaux faibles — gain de marché public, extension d'usine, augmentation de capital —
dans la presse économique locale, là où elles apparaissent en premier, bien avant tout classement ou
toute base de données financière internationale.

**Analyse sectorielle contextualisée.** Chaque pays de la sous-région suit une trajectoire propre — la
transition post-pétrole au Gabon et au Congo, l'agro-industrie et les services au Cameroun, l'économie
pétrolière et agro-pastorale au Tchad. L'agent intègre le plan national de développement de chaque
État dans son évaluation, pour juger l'alignement d'une cible non pas dans l'absolu, mais au regard
des priorités réelles de son pays.

**Due Diligence accélérée en contexte francophone et OHADA.** Statuts, procès-verbaux de conseil
d'administration, bilans au format SYSCOHADA : l'agent est instruit pour passer ce corpus au crible en
quelques secondes et en faire ressortir les anomalies classiques (provisions sous-évaluées, comptes
courants d'associés non formalisés, engagements hors bilan non mentionnés), là où un premier tri
manuel prendrait plusieurs heures par dossier.

---

## 3. Mode d'emploi

### 3.1 Prérequis

- Une clé API Groq, gratuite, obtenue sur https://console.groq.com/keys
- Soit Docker (recommandé), soit Python 3.11/3.12 en local

### 3.2 Installation avec Docker (recommandé)

```bash
git clone https://github.com/VOTRE-PSEUDO/sira-ma-agent.git
cd sira-ma-agent
cp .env.example .env          # puis renseigner GROQ_API_KEY dans .env
docker compose up --build
```

L'application est disponible sur **http://localhost:8501**. Pour l'arrêter : `docker compose down`.

### 3.3 Installation sans Docker

```bash
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### 3.4 Personnalisation avant toute présentation

Ouvrir `app.py` et remplacer la constante `AUTHOR_NAME` par le nom de l'auteur du projet. La clé API
peut être fournie via `.env`, ou saisie directement dans le champ prévu à cet effet dans la barre
latérale de l'application — utile pour une démonstration sans exposer sa clé dans le code.

---

## 4. Guide d'utilisation

**Onglet « Nouvelle analyse »**
1. Renseigner le nom de la cible, son pays (menu déroulant limité aux six pays CEMAC) et son secteur.
2. Joindre, si disponibles, les documents reçus : pitch deck, états financiers, statuts, RCCM, PV
   d'assemblée générale (PDF ou texte). En leur absence, l'agent s'appuie sur sa veille web et la
   presse spécialisée.
3. Cliquer sur **Lancer l'agent Sira M&A**. Les quatre étapes du workflow s'exécutent l'une après
   l'autre et sont affichées en direct.

**Onglet « Résultats du deal »**
- Indicateurs clés (chiffre d'affaires, EBITDA, marge, ratio d'endettement, part d'emplois locaux).
- Jauge de score global et recommandation (GO / GO SOUS CONDITIONS / NO GO), avec le niveau de
  conformité CEMAC/OHADA affiché à côté.
- Graphique radar détaillant la notation sur les sept axes du modèle FOKAM.
- Note de cadrage complète, téléchargeable en Markdown ou en HTML pour partage au Comité
  d'Investissement.
- Détail de la veille sur les risques CEMAC et les signaux faibles détectés.
- Données financières et juridiques extraites, au format JSON pour vérification ou réutilisation.

**Onglet « Deal Flow CEMAC »**
- Vue tabulaire de tous les deals analysés dans la session, filtrable par pays.
- Compteurs synthétiques : nombre de deals, nombre de recommandations GO, nombre de pays couverts.
- Rappel des repères macroéconomiques et du plan national de développement de chacun des six pays.

**Onglet « Architecture »**
- Rappel du schéma de fonctionnement, de la stack technique et des référentiels réglementaires et de
  marché intégrés au moteur de prompts, ainsi que des recommandations de sécurisation des données.

**Barre latérale**
- Sélection du modèle Llama (Groq) utilisé pour l'analyse.
- Paramétrage de la thèse d'investissement : pays couverts, secteurs prioritaires, taille de ticket,
  type de participation, critères additionnels dans l'esprit du modèle FOKAM.
- Encart dépliant sur la souveraineté et la sécurité des données.

---

## 5. Structure du projet

```
sira-ma-agent/
├── app.py                     # Application Streamlit (interface + workflow)
├── core/
│   ├── llm.py                 # Client Groq, gestion des erreurs et des limites de débit, veille web
│   └── reference_cemac.py     # Référentiel CEMAC / OHADA / BVMAC injecté dans les prompts
├── .streamlit/config.toml     # Thème visuel de l'application
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 6. Modèles utilisés (Groq Cloud)

| Modèle | Usage dans l'agent |
|---|---|
| `llama-3.3-70b-versatile` | Analyse financière, scoring, rédaction de la note de cadrage (modèle par défaut) |
| `llama-3.1-8b-instant` | Tri rapide et extraction, pour les tâches à faible latence |
| `groq/compound` | Veille web CEMAC, avec recherche intégrée au modèle |

> Meta et Groq ont retiré les modèles Llama 3.2 du catalogue Groq (remplacés notamment par Llama 4
> Scout pour les usages multimodaux). L'agent utilise donc les modèles Llama réellement servis en
> production par Groq au moment de sa conception, ce qui est indiqué explicitement dans l'interface
> pour éviter toute ambiguïté lors d'une présentation.

---

## 7. Limites actuelles

- **Prototype de démonstration, non un outil de production.** L'application n'a pas fait l'objet
  d'un audit de sécurité ni d'une revue juridique ; elle illustre une approche et une architecture,
  pas un produit prêt à traiter des données réellement confidentielles.
- **Aucune connexion directe à un registre officiel.** L'agent ne consulte pas d'API RCCM, BEAC ou
  COBAC : ses éléments de conformité proviennent de sa connaissance générale du cadre réglementaire et
  d'une veille web, à recouper systématiquement avec les registres officiels avant toute décision.
- **Données de marché non garanties en temps réel.** La BVMAC est un marché encore peu liquide, sans
  API publique de cotation ; les informations de marché doivent être vérifiées directement auprès de
  la bourse ou d'une société de bourse agréée.
- **Le modèle peut se tromper ou halluciner**, en particulier sur des chiffres précis absents des
  documents fournis. Chaque note de cadrage indique les données non vérifiées, mais la vigilance de
  l'analyste humain reste indispensable.
- **Aucune mémoire persistante entre les sessions** dans cette version : le pipeline de deal flow
  affiché dans l'onglet dédié est réinitialisé à chaque redémarrage de l'application.
- **Dépendance à un fournisseur de cloud d'inférence externe (Groq)**, ce qui pose la question de la
  souveraineté des données tant qu'aucun accord de Zero Data Retention n'est formellement signé.

## 8. Perspectives d'évolution

- **Connexion à des sources de données structurées** : API ou flux de scraping autorisé pour la
  BVMAC, les journaux officiels nationaux et les registres RCCM, afin de fiabiliser la couche de
  conformité au-delà de la veille web générale.
- **Base de deal flow persistante** : remplacement du stockage en mémoire de session par une base de
  données (PostgreSQL ou équivalent), avec historique, droits d'accès par utilisateur et export
  consolidé pour le Comité d'Investissement.
- **Module de comparables sectoriels** : constitution progressive d'une bibliothèque interne de
  transactions et de multiples de valorisation observés en zone CEMAC, pour enrichir le scoring au fil
  des dossiers traités.
- **Déploiement souverain** : hébergement sur un cloud privé ou hybride dédié à la SAPA, avec option
  de modèle de langage auto-hébergé pour les dossiers les plus sensibles, en complément du mode Groq
  Cloud utilisé pour la démonstration.
- **Boucle de retour du Comité d'Investissement** : ajout d'un mécanisme de validation ou de
  correction humaine sur chaque note générée, dont les enseignements viendraient affiner
  progressivement les critères de scoring du modèle FOKAM.
- **Extension progressive du périmètre géographique**, vers l'espace UEMOA puis panafricain, une fois
  le modèle validé et éprouvé sur son terrain d'origine, la zone CEMAC.

---

## Avertissement

Les analyses produites par Sira M&A sont des synthèses **pré-Due Diligence**, destinées à accélérer le
premier tri du deal flow. Elles ne remplacent en aucun cas une Due Diligence juridique, financière et
fiscale complète, menée par des professionnels qualifiés.
