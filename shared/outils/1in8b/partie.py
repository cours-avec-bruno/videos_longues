#!/usr/bin/env python3
"""Rejoue et archive une partie de 1 sur 8 milliards (1in8b Engine API), avec chaque décision documentée.

Ce que fait le script (tout est enregistré en JSON dans le dossier de sortie) :
  1. la vie « au plus fréquent » : /life avec la politique auto (« ce que la plupart des gens choisissent »,
     le défaut du moteur), avec le récit, les décisions (options + option retenue) et les chiffres année par année ;
  2. la même vie (même seed) avec la politique « ambitious » : la vie « pour réussir », à comparer ;
  3. la même vie rejouée pas à pas avec /live, pour enregistrer chaque décision telle que le moteur la présente
     (question, options, probabilités quand le moteur les donne) et l'option prise ;
  4. les 4 autres bébés (seeds suivantes) et les comparaisons de contexte.

La clé n'est jamais affichée. Elle est lue, dans l'ordre, dans :
  - la variable d'environnement K8B_KEY ;
  - le fichier ~/.1in8b-cle (une seule ligne : k8b_...).

Usage (la vie la plus probable : Inde, campagne, garçon, cinquième du milieu ; caste et religion mesurées) :
  python shared/outils/1in8b/partie.py --seed 20261106 --country IND --sex male --place village --fifth 3       --mesurer faith,caste --sortie videos/<slug>/prompts/partie
"""
import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://1in8b.life/api/v1"
UA = "studio-videos-longues/1.0"
CHAMPS_PROBA = ("odds", "share", "p", "prob", "probability", "pct", "percent", "weight", "chance")


def lire_cle():
    cle = os.environ.get("K8B_KEY", "").strip()
    if not cle:
        f = pathlib.Path.home() / ".1in8b-cle"
        if f.exists():
            cle = f.read_text(encoding="utf-8-sig").strip()
    if not cle.startswith("k8b_"):
        sys.exit("Clé introuvable : mettez-la dans la variable K8B_KEY ou dans le fichier ~/.1in8b-cle (une ligne k8b_...).")
    return cle


class Api:
    def __init__(self, cle):
        self.cle = cle
        self.appels = 0

    def _req(self, req):
        req.add_header("Authorization", "Bearer " + self.cle)
        req.add_header("User-Agent", UA)
        for essai in range(8):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    self.appels += 1
                    time.sleep(2.1)  # 30 appels par minute au plus sur l'offre gratuite
                    return json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                corps = e.read().decode("utf-8", "replace")
                if e.code in (429, 502, 503, 504) and essai < 7:
                    attente = 30 if e.code == 429 else 10 * (essai + 1)
                    print(f"   (serveur : {e.code}, nouvel essai dans {attente} s)")
                    time.sleep(attente)
                    continue
                sys.exit(f"Erreur {e.code} sur {req.full_url.split('?')[0]} : {corps[:500]}")
        sys.exit("Trop d'erreurs du serveur.")

    def get(self, chemin, **params):
        q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        return self._req(urllib.request.Request(f"{BASE}{chemin}?{q}"))

    def post(self, chemin, corps):
        req = urllib.request.Request(f"{BASE}{chemin}", data=json.dumps(corps).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        return self._req(req)


def ecrire(dossier, nom, data):
    p = dossier / nom
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  écrit : {p}")


def proba(choix):
    """La probabilité d'une option, si le moteur la donne (le nom du champ n'est pas documenté)."""
    for k in CHAMPS_PROBA:
        v = choix.get(k)
        if isinstance(v, (int, float)):
            return float(v)
    return None


def rejouer_live(api, seed, lang, decisions_auto, conditions=None, max_pas=600):
    """Rejoue la vie pas à pas. À chaque décision : l'option la plus probable si le moteur donne les
    probabilités ; sinon l'option que la politique auto a prise au même âge pour la même question."""
    auto_par_age = {}
    for d in decisions_auto or []:
        cle = (d.get("age"), d.get("id") or d.get("card"))
        auto_par_age.setdefault(cle, d)
    pas = []
    r = api.post("/live", dict(conditions or {}, seed=seed, lang=lang))
    for _ in range(max_pas):
        d = r.get("decision")
        entree = {"age": (r.get("state") or {}).get("age"), "events": r.get("events"), "decision": d}
        if r.get("ended") or not r.get("token"):
            entree["fin"] = r.get("death")
            pas.append(entree)
            break
        if not d:
            pas.append(entree)
            r = api.post("/live", {"token": r["token"], "until": "decision"})
            continue
        choix = d.get("choices") or []
        avec_p = [(proba(c), c) for c in choix]
        if choix and all(p is not None for p, _ in avec_p):
            retenu = max(avec_p, key=lambda t: t[0])[1]
            entree["regle"] = "la plus probable (probabilités données par le moteur)"
        else:
            ref = auto_par_age.get((entree["age"], d.get("id")))
            cle_auto = None
            if ref:
                cle_auto = ref.get("chose") or ref.get("choice") or ref.get("made")
            retenu = next((c for c in choix if c.get("key") == cle_auto), None)
            if retenu:
                entree["regle"] = "celle de la politique auto (même âge, même question)"
            else:
                retenu = choix[0] if choix else None
                entree["regle"] = "⚠️ ni probabilités ni correspondance auto : première option, À VÉRIFIER"
        entree["choisi"] = retenu.get("key") if retenu else None
        pas.append(entree)
        r = api.post("/live", {"token": r["token"], "choose": entree["choisi"]})
    return pas


def le_plus_frequent(api, conditions, par, seed, n=60):
    """Mesure, avec /simulate, la valeur la plus fréquente d'un trait de naissance (caste, religion…)
    parmi les naissances qui ont déjà les conditions données. Renvoie (valeur, tableau des parts)."""
    sexe = conditions.get("sex")
    r = api.get("/simulate", n=n, by=par, seed=seed, **conditions)
    bloc = r.get("male" if sexe == "male" else "female") or {}
    groupes = bloc.get("groups") or {}
    parts = {k: (v.get("lives") if isinstance(v, dict) else v) for k, v in groupes.items()}
    if not parts:
        return None, r
    return max(parts, key=lambda k: parts[k] or 0), {"parts": parts, "reponse": r}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--lang", default="fr")
    ap.add_argument("--country", help="ISO alpha-3 (ex. IND) ; absent = tiré au sort")
    ap.add_argument("--sex", choices=["male", "female"])
    ap.add_argument("--place", choices=["town", "village"])
    ap.add_argument("--fifth", type=int, choices=[1, 2, 3, 4, 5])
    ap.add_argument("--faith")
    ap.add_argument("--caste")
    ap.add_argument("--mesurer", default="", help="traits à fixer à leur valeur la plus fréquente, mesurée par /simulate (ex. faith,caste)")
    ap.add_argument("--sans-live", action="store_true", help="ne pas rejouer pas à pas avec /live")
    ap.add_argument("--etapes", default="mesures,auto,ambitieuse,live,autres,tiree",
                    help="étapes à faire ; les autres sont relues dans le dossier de sortie (ex. live,autres,tiree)")
    a = ap.parse_args()
    etapes = {e.strip() for e in a.etapes.split(",")}

    dossier = pathlib.Path(a.sortie)
    dossier.mkdir(parents=True, exist_ok=True)
    api = Api(lire_cle())
    cond = {k: v for k, v in dict(country=a.country, sex=a.sex, place=a.place, fifth=a.fifth,
                                  faith=a.faith, caste=a.caste).items() if v is not None}
    print(f"Partie seed {a.seed}, conditions {cond} → {dossier}")

    mesures = {}
    if "mesures" not in etapes and (dossier / "0-mesures-naissance.json").exists():
        cond = json.loads((dossier / "0-mesures-naissance.json").read_text(encoding="utf-8"))["conditions_finales"]
        print(f"   conditions relues : {cond}")
    for trait in [t.strip() for t in a.mesurer.split(",") if t.strip() and "mesures" in etapes]:
        print(f"0. Mesure du trait le plus fréquent : {trait}")
        valeur, detail = le_plus_frequent(api, cond, trait, a.seed)
        mesures[trait] = {"retenu": valeur, **(detail if isinstance(detail, dict) and "parts" in detail else {"reponse": detail})}
        print(f"   {trait} le plus fréquent : {valeur}  {mesures[trait].get('parts')}")
        if valeur and valeur not in ("none", "majority", "null"):
            cond[trait] = valeur
    if mesures:
        ecrire(dossier, "0-mesures-naissance.json", {"conditions_finales": cond, "mesures": mesures})

    if "auto" in etapes:
        print("1. La vie au plus fréquent (politique auto)")
        auto = api.get("/life", seed=a.seed, lang=a.lang, record=1, decisions=1, trace=1, **cond)
        ecrire(dossier, "1-vie-auto.json", auto)
    else:
        auto = json.loads((dossier / "1-vie-auto.json").read_text(encoding="utf-8"))

    if "ambitieuse" in etapes:
        print("2. La même vie, politique ambitieuse")
        ambi = api.get("/life", seed=a.seed, lang=a.lang, record=1, decisions=1, trace=1, policy="ambitious", **cond)
        ecrire(dossier, "2-vie-ambitieuse.json", ambi)

    if not a.sans_live and "live" in etapes:
        print("3. La vie rejouée pas à pas (/live)")
        vie = (auto.get("lives") or [{}])[0]
        pas = rejouer_live(api, a.seed, a.lang, vie.get("decisions"), cond)
        ecrire(dossier, "3-live-pas-a-pas.json", {"meta": auto.get("meta"), "seed": a.seed, "conditions": cond, "pas": pas})

    if "autres" in etapes:
        print("4. Les 4 autres bébés (tirés au sort, sans condition)")
        autres = [api.get("/life", seed=a.seed + i, lang=a.lang, record=0, decisions=1) for i in range(1, 5)]
        ecrire(dossier, "4-autres-bebes.json", autres)

    if "tiree" in etapes:
        print("5. La vie tirée au sort avec la même seed (Khadija, pour comparaison)")
        tiree = api.get("/life", seed=a.seed, lang=a.lang, record=1, decisions=1)
        ecrire(dossier, "5-vie-tiree-au-sort.json", tiree)

    ecrire(dossier, "0-meta.json", {
        "seed": a.seed,
        "conditions": cond,
        "engine": (auto.get("meta") or {}).get("engine"),
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "appels": api.appels,
        "usage": auto.get("usage"),
        "credit": "1in8b Engine (1in8b.life)",
    })
    print(f"Terminé : {api.appels} appels.")


if __name__ == "__main__":
    main()
