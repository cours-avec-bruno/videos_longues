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

Usage :
  python shared/outils/1in8b/partie.py --seed 20261106 --sortie videos/<slug>/prompts/partie
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
            cle = f.read_text(encoding="utf-8").strip()
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
        for essai in range(4):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    self.appels += 1
                    time.sleep(2.1)  # 30 appels par minute au plus sur l'offre gratuite
                    return json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                corps = e.read().decode("utf-8", "replace")
                if e.code == 429 and essai < 3:
                    time.sleep(30)
                    continue
                sys.exit(f"Erreur {e.code} sur {req.full_url.split('?')[0]} : {corps[:500]}")
        sys.exit("Trop d'erreurs 429.")

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


def rejouer_live(api, seed, lang, decisions_auto, max_pas=600):
    """Rejoue la vie pas à pas. À chaque décision : l'option la plus probable si le moteur donne les
    probabilités ; sinon l'option que la politique auto a prise au même âge pour la même question."""
    auto_par_age = {}
    for d in decisions_auto or []:
        cle = (d.get("age"), d.get("id") or d.get("card"))
        auto_par_age.setdefault(cle, d)
    pas = []
    r = api.post("/live", {"seed": seed, "lang": lang})
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--lang", default="fr")
    ap.add_argument("--sans-live", action="store_true", help="ne pas rejouer pas à pas avec /live")
    a = ap.parse_args()

    dossier = pathlib.Path(a.sortie)
    dossier.mkdir(parents=True, exist_ok=True)
    api = Api(lire_cle())
    print(f"Partie seed {a.seed} → {dossier}")

    print("1. La vie au plus fréquent (politique auto)")
    auto = api.get("/life", seed=a.seed, lang=a.lang, record=1, decisions=1, trace=1)
    ecrire(dossier, "1-vie-auto.json", auto)

    print("2. La même vie, politique ambitieuse")
    ambi = api.get("/life", seed=a.seed, lang=a.lang, record=1, decisions=1, trace=1, policy="ambitious")
    ecrire(dossier, "2-vie-ambitieuse.json", ambi)

    if not a.sans_live:
        print("3. La vie rejouée pas à pas (/live)")
        vie = (auto.get("lives") or [{}])[0]
        pas = rejouer_live(api, a.seed, a.lang, vie.get("decisions"))
        ecrire(dossier, "3-live-pas-a-pas.json", {"meta": auto.get("meta"), "seed": a.seed, "pas": pas})

    print("4. Les 4 autres bébés")
    autres = [api.get("/life", seed=a.seed + i, lang=a.lang, record=0, decisions=1) for i in range(1, 5)]
    ecrire(dossier, "4-autres-bebes.json", autres)

    ecrire(dossier, "0-meta.json", {
        "seed": a.seed,
        "engine": (auto.get("meta") or {}).get("engine"),
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "appels": api.appels,
        "usage": auto.get("usage"),
        "credit": "1in8b Engine (1in8b.life)",
    })
    print(f"Terminé : {api.appels} appels.")


if __name__ == "__main__":
    main()
