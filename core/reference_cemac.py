"""
Sira M&A - Afrique Centrale
Base de connaissance statique injectée dans les prompts : géographie CEMAC,
régulateurs, presse spécialisée et thèse d'investissement « modèle FOKAM ».
Ces éléments sont du contexte pour guider le LLM, pas des données de marché
temps réel : les chiffres de marché doivent toujours être vérifiés par la
veille web intégrée à l'agent.
"""

CEMAC_COUNTRIES = {
    "Cameroun": {
        "capitale": "Yaoundé", "pole_eco": "Douala", "devise": "FCFA (XAF)",
        "secteurs_cles": ["Agro-industrie", "Industrie manufacturière", "Services financiers", "BTP", "Logistique portuaire"],
        "plan_national": "Stratégie Nationale de Développement 2020-2030 (SND30)",
        "note_macro": "Économie la plus diversifiée de la CEMAC ; hub logistique régional via le port de Douala.",
    },
    "Gabon": {
        "capitale": "Libreville", "pole_eco": "Port-Gentil", "devise": "FCFA (XAF)",
        "secteurs_cles": ["Bois & agro-transformation", "Mines (manganèse)", "Services", "Transition post-pétrole"],
        "plan_national": "Plan d'Accélération de la Transformation (PAT)",
        "note_macro": "Diversification post-pétrole activement recherchée ; siège de la COSUMAF (régulateur BVMAC).",
    },
    "République du Congo": {
        "capitale": "Brazzaville", "pole_eco": "Pointe-Noire", "devise": "FCFA (XAF)",
        "secteurs_cles": ["Hydrocarbures", "Agro-industrie", "BTP", "Bois"],
        "plan_national": "Plan National de Développement (PND)",
        "note_macro": "Dépendance pétrolière forte ; enjeu de diversification et de restructuration de la dette.",
    },
    "Tchad": {
        "capitale": "N'Djaména", "pole_eco": "N'Djaména", "devise": "FCFA (XAF)",
        "secteurs_cles": ["Pétrole", "Agro-pastoral", "BTP"],
        "plan_national": "Vision 2030 « le Tchad que nous voulons »",
        "note_macro": "Économie pétrolière et agro-pastorale ; risque sécuritaire régional à surveiller.",
    },
    "République Centrafricaine": {
        "capitale": "Bangui", "pole_eco": "Bangui", "devise": "FCFA (XAF)",
        "secteurs_cles": ["Mines (diamant, or)", "Agriculture", "Bois"],
        "plan_national": "Plan National de Relèvement et de Consolidation de la Paix (RCPCA)",
        "note_macro": "Risque politique et sécuritaire élevé ; secteur formel restreint.",
    },
    "Guinée Équatoriale": {
        "capitale": "Malabo", "pole_eco": "Bata", "devise": "FCFA (XAF)",
        "secteurs_cles": ["Hydrocarbures", "BTP", "Services"],
        "plan_national": "Agenda Horizonte 2035",
        "note_macro": "Seul pays hispanophone de la CEMAC ; économie très dépendante des hydrocarbures.",
    },
}

REGULATORS_CONTEXT = """
- BEAC (Banque des États de l'Afrique Centrale) : banque centrale commune des 6 pays CEMAC, émettrice du FCFA (XAF),
  dépositaire central historique du marché financier régional. Édicte la réglementation des changes CEMAC
  (Règlement n°02/18/CEMAC) : rapatriement obligatoire des recettes d'exportation, autorisation ou déclaration
  préalable pour les transferts de capitaux et dividendes vers l'étranger au-delà de certains seuils, justificatifs
  documentaires exigés pour toute sortie de devises. C'est le point de vigilance n°1 pour un investisseur qui doit
  organiser des flux entrants (apport en capital) ou sortants (dividendes, remboursement d'actionnaire, sortie du deal).
- COBAC (Commission Bancaire de l'Afrique Centrale) : régulateur et superviseur prudentiel du secteur bancaire et de la
  microfinance dans la zone CEMAC. Pertinente pour toute cible du secteur financier (banque, microfinance, leasing) :
  ratios prudentiels, agrément, gouvernance, actionnariat de référence.
- COSUMAF (Commission de Surveillance du Marché Financier de l'Afrique Centrale) : régulateur du marché financier
  régional, basé à Libreville, en charge de l'agrément des sociétés de bourse et du contrôle du marché BVMAC.
- BVMAC (Bourse des Valeurs Mobilières de l'Afrique Centrale) : bourse régionale unique de la CEMAC, née en juillet 2019
  de la fusion de l'ancienne BVMAC (Libreville) et de la Douala Stock Exchange (DSX). Siège social à Douala. Marché
  encore peu liquide, avec un compartiment actions restreint et un compartiment obligataire (emprunts d'État et
  d'entreprises) plus actif. Une introduction en bourse (IPO) ou une émission obligataire à la BVMAC est une voie de
  sortie possible pour la SAPA, à évaluer au cas par cas selon la liquidité réelle du marché au moment de l'analyse.
- OHADA / CCJA : l'Organisation pour l'Harmonisation en Afrique du Droit des Affaires fournit le droit des sociétés
  commun (Acte uniforme relatif au droit des sociétés commerciales et du GIE, Acte uniforme sur les sûretés, Acte
  uniforme portant organisation des procédures collectives d'apurement du passif). La CCJA (Cour Commune de Justice et
  d'Arbitrage, siège à Abidjan) est la juridiction suprême et la chambre d'arbitrage de référence pour sécuriser un
  pacte d'actionnaires régional.
- SYSCOHADA révisé : référentiel comptable obligatoire dans les 17 pays OHADA. Les états financiers normalisés à
  contrôler sont : Bilan, Compte de résultat, Tableau des Flux de Trésorerie (ou TAFIRE selon le système), État annexé.
  Points d'attention classiques en Due Diligence SYSCOHADA : provisions pour risques et charges sous-évaluées, comptes
  courants d'associés non formalisés, immobilisations non réévaluées, engagements hors bilan non mentionnés en annexe.
"""

NEWS_SOURCES = [
    {"nom": "Investir au Cameroun", "pays": "Cameroun", "url": "www.investiraucameroun.com"},
    {"nom": "EcoMatin", "pays": "Cameroun", "url": "www.ecomatin.net"},
    {"nom": "Cameroon Tribune", "pays": "Cameroun", "url": "www.cameroon-tribune.cm"},
    {"nom": "Le Nouveau Gabon", "pays": "Gabon", "url": "www.lenouveaugabon.com"},
    {"nom": "Gabon Review", "pays": "Gabon", "url": "www.gabonreview.com"},
    {"nom": "Adiac-Congo (Les Dépêches de Brazzaville)", "pays": "Congo", "url": "www.adiac-congo.com"},
    {"nom": "Tchad Infos", "pays": "Tchad", "url": "www.tchadinfos.com"},
    {"nom": "Agence Ecofin", "pays": "Régional CEMAC/Afrique", "url": "www.agenceecofin.com"},
    {"nom": "Financial Afrik", "pays": "Régional Afrique francophone", "url": "www.financialafrik.com"},
    {"nom": "African Markets", "pays": "Régional Afrique", "url": "www.african-markets.com"},
    {"nom": "BEAC (communiqués officiels)", "pays": "Régional CEMAC", "url": "www.beac.int"},
]

FOKAM_THESIS_AXES = {
    "Alignement stratégique CEMAC": "Cohérence du secteur et du pays cible avec les plans nationaux de développement "
        "et les priorités affichées de la SAPA (agro-industrie, transition post-pétrole, infrastructures, services).",
    "Impact emploi local & ancrage territorial": "Nombre d'emplois créés/maintenus localement, part de main-d'œuvre "
        "et de cadres locaux, effet d'entraînement sur l'écosystème de PME et fournisseurs locaux.",
    "Valeur ajoutée industrielle": "Part de transformation locale de la matière première, degré d'intégration "
        "verticale, réduction de la dépendance aux importations — conforme à la vision de développement par la PME "
        "industrielle locale prônée par le Dr FOKAM.",
    "Solidité du management & gouvernance": "Qualité et stabilité de l'équipe dirigeante locale, existence d'organes "
        "de gouvernance (conseil d'administration, commissariat aux comptes), transparence de l'actionnariat.",
    "Santé financière & endettement": "Rentabilité (marge EBITDA), structure du bilan SYSCOHADA, ratio dette "
        "nette / EBITDA, capacité de remboursement, qualité du besoin en fonds de roulement.",
    "Conformité réglementaire CEMAC/OHADA": "Conformité au droit OHADA (statuts, formalités RCCM), à la réglementation "
        "des changes BEAC pour les flux transfrontaliers, et le cas échéant aux exigences prudentielles COBAC.",
    "Potentiel de sortie": "Options de sortie réalistes à 5-7 ans : rachat industriel, cession à un fonds panafricain, "
        "introduction en bourse ou émission obligataire à la BVMAC.",
}

WEAK_SIGNALS_HINTS = [
    "Gain récent d'un marché public national ou communautaire (CEMAC/BAD/Banque mondiale)",
    "Extension, modernisation ou ouverture d'une nouvelle usine / unité de production",
    "Augmentation de capital ou entrée d'un nouvel actionnaire industriel",
    "Certification qualité, agrément à l'export ou nouveau partenariat de distribution",
    "Recrutement massif ou création d'emplois annoncée dans la presse locale",
    "Levée de fonds ou financement bancaire structurant obtenu",
]

SECTOR_OPTIONS = ["Agro-industrie & agro-transformation", "Industrie manufacturière", "Énergie & post-pétrole",
    "BTP & matériaux de construction", "Services financiers & microfinance", "Logistique, transport & portuaire",
    "Santé & pharmacie", "Mines & ressources naturelles", "Distribution & retail", "Télécoms & digital"]
