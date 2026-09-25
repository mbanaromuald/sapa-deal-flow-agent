"""
Sira M&A - Afrique Centrale
Couche d'accès au LLM : Groq Cloud, modèles Llama de Meta.
Isolée dans ce module pour rester facilement testable/remplaçable
(ex : bascule vers un endpoint privé si la SAPA opte pour un déploiement souverain).
"""
import json
import re
import time

from openai import OpenAI

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Modèles Llama actuellement servis par Groq (vérifiés — Llama 3.2 a été retiré du
# catalogue Groq et n'est donc volontairement pas proposé ici).
MODELS = {
    "Llama 3.3 70B Versatile (recommandé — analyse & rédaction)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B Instant (rapide — tri & extraction)": "llama-3.1-8b-instant",
    "Groq Compound (Llama + recherche web intégrée)": "groq/compound",
}
DEFAULT_MODEL = "llama-3.3-70b-versatile"
WEB_MODEL = "groq/compound"


def get_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL, timeout=180)


def _chat(client: OpenAI, model: str, system: str, user: str, temperature: float) -> str:
    """Appel chat.completions avec retry exponentiel simple sur limite de débit (429)."""
    last_err = None
    for attempt in range(3):
        try:
            r = client.chat.completions.create(
                model=model, temperature=temperature,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            )
            return r.choices[0].message.content or ""
        except Exception as e:  # noqa: BLE001
            last_err = e
            msg = str(e).lower()
            if "decommission" in msg or "model_not_found" in msg or "does not exist" in msg:
                raise RuntimeError(
                    f"Le modèle « {model} » n'est plus servi par Groq. "
                    "Sélectionnez un autre modèle Llama dans la barre latérale."
                ) from e
            if ("rate" in msg or "429" in msg) and attempt < 2:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    raise last_err  # pragma: no cover


def web_search_snippets(query: str, site_hints: list[str] | None = None, n: int = 6) -> str:
    """Veille web de secours (DuckDuckGo, gratuit, sans clé) utilisée quand le modèle
    choisi n'a pas de recherche intégrée. Biaisée vers la presse spécialisée CEMAC."""
    try:
        from ddgs import DDGS
        results = []
        with DDGS() as d:
            for r in d.text(query, region="fr-fr", max_results=n):
                results.append(f"- {r.get('title', '')} — {r.get('body', '')[:280]} ({r.get('href', '')})")
            for r in d.news(query, region="fr-fr", max_results=n):
                results.append(f"- [Actu] {r.get('title', '')} — {r.get('body', '')[:280]} ({r.get('url', '')})")
        return "\n".join(results)
    except Exception:
        return ""


def llm(client: OpenAI, model: str, system: str, user: str, web: bool = False, temperature: float = 0.2) -> str:
    """Appel unifié. Si web=True : tente Groq Compound (Llama + recherche web native),
    sinon complète le prompt avec une veille DuckDuckGo avant d'interroger le modèle choisi."""
    if web:
        try:
            return _chat(client, WEB_MODEL, system, user, temperature)
        except Exception:
            snippets = web_search_snippets(user.strip().split("\n")[0][:180])
            if snippets:
                user = f"{user}\n\nRÉSULTATS DE VEILLE WEB (à exploiter, citer la source) :\n{snippets}"
    return _chat(client, model, system, user, temperature)


def parse_json(text: str) -> dict:
    """Extrait le premier bloc JSON valide d'une réponse LLM (tolère un préambule)."""
    try:
        match = re.search(r"\{.*\}", text, re.S)
        return json.loads(match.group(0)) if match else {}
    except Exception:
        return {}
