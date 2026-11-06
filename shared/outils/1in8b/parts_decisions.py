#!/usr/bin/env python3
"""Mesure, sur de nombreuses vies nées dans les mêmes conditions, quelle option la politique auto prend
à chaque décision. Donne des parts réelles (« X % des vies ont choisi ceci ») pour les encarts « À VOUS ».

Le moteur ne publie pas de probabilité par option : ces parts sont **observées** sur des vies simulées
(un échantillon, avec son incertitude), pas des probabilités officielles.

Usage :
  python shared/outils/1in8b/parts_decisions.py --conditions videos/<slug>/prompts/partie/0-mesures-naissance.json \
      --vies 40 --seed-depart 30000000 --sortie videos/<slug>/prompts/partie/6-parts-decisions.json
"""
import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from partie import Api, lire_cle  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conditions", required=True, help="0-mesures-naissance.json (conditions_finales)")
    ap.add_argument("--vies", type=int, default=40)
    ap.add_argument("--seed-depart", type=int, default=30000000)
    ap.add_argument("--policy", default=None, help="auto (défaut du moteur) ou ambitious")
    ap.add_argument("--sortie", required=True)
    a = ap.parse_args()

    cond = json.loads(pathlib.Path(a.conditions).read_text(encoding="utf-8"))["conditions_finales"]
    api = Api(lire_cle())
    par_decision = collections.defaultdict(lambda: {"question": None, "labels": {}, "choix": collections.Counter(), "ages": [], "rencontres": []})
    vies = []
    seed = a.seed_depart
    while len(vies) < a.vies:
        n = min(5, a.vies - len(vies))
        r = api.get("/life", seed=seed, n=n, lang="fr", record=0, decisions=1, policy=a.policy, **cond)
        for v in r.get("lives", []):
            vies.append({"seed": v.get("seed"), "name": v.get("name"), "education": v.get("education"),
                         "age_at_death": v.get("age_at_death"), "children": v.get("children")})
            for d in v.get("decisions") or []:
                e = par_decision[d["id"]]
                e["question"] = e["question"] or d.get("question")
                for c in d.get("choices", []):
                    e["labels"][c["key"]] = c["label"]
                e["choix"][d.get("chose")] += 1
                e["ages"].append(d.get("age"))
                e["rencontres"].append({"age": d.get("age"), "proposees": sorted(c["key"] for c in d.get("choices", [])), "choisie": d.get("chose")})
        seed += 1000
        print(f"  {len(vies)} vies")

    resume = {}
    for k, e in sorted(par_decision.items(), key=lambda kv: -sum(kv[1]["choix"].values())):
        total = sum(e["choix"].values())
        resume[k] = {
            "question": e["question"],
            "rencontres": total,
            "ages": sorted(set(e["ages"])),
            "parts": {e["labels"].get(c, c): round(n / total, 3) for c, n in e["choix"].most_common()},
            "parts_par_cle": {c: round(n / total, 4) for c, n in e["choix"].most_common()},
            "labels": e["labels"],
            "detail": e["rencontres"],
            "options_jamais_prises": [lab for key, lab in e["labels"].items() if key not in e["choix"]],
        }
    out = {"conditions": cond, "policy": a.policy or "auto", "vies": len(vies), "seeds_depuis": a.seed_depart,
           "attention": "parts observées sur des vies simulées (échantillon), pas des probabilités publiées par le moteur",
           "decisions": resume, "liste_vies": vies}
    pathlib.Path(a.sortie).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"écrit : {a.sortie} ({api.appels} appels)")


if __name__ == "__main__":
    main()
