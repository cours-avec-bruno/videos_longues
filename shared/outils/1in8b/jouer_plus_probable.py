#!/usr/bin/env python3
"""Joue une vie pas à pas (/live) en prenant, à chaque décision, l'option la plus fréquente.

La politique `auto` du moteur tire au sort selon les parts réelles : elle ne prend donc pas toujours
l'option majoritaire. Ici, on décide nous-mêmes. À chaque décision, on estime la part de chaque option
proposée à partir des vies simulées dans les mêmes conditions de naissance (fichier de parts_decisions.py),
et on prend la plus haute.

Estimation, par ordre de préférence :
  1. « même menu » : les rencontres de la même décision où exactement les mêmes options étaient proposées
     (au moins 5 rencontres) ;
  2. « taux quand proposée » : pour chaque option, la part des fois où elle a été prise quand elle était
     proposée, normalisée sur le menu actuel ;
  3. sinon : décision jamais vue dans l'échantillon, première option, signalée « À VÉRIFIER ».

Usage :
  python shared/outils/1in8b/jouer_plus_probable.py --seed 20261106 \
      --conditions videos/<slug>/prompts/partie/0-mesures-naissance.json \
      --parts videos/<slug>/prompts/partie/6-parts-decisions.json \
      --sortie videos/<slug>/prompts/partie/7-vie-la-plus-probable.json
"""
import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from partie import Api, lire_cle  # noqa: E402


def estimer(parts, did, menu):
    e = parts.get(did)
    if not e:
        return None, "jamais vue", 0
    detail = e.get("detail") or []
    meme = [r["choisie"] for r in detail if r["proposees"] == sorted(menu)]
    if len(meme) >= 5:
        c = collections.Counter(meme)
        return {k: c.get(k, 0) / len(meme) for k in menu}, "même menu", len(meme)
    taux = {}
    for k in menu:
        proposee = [r for r in detail if k in r["proposees"]]
        taux[k] = (sum(1 for r in proposee if r["choisie"] == k) / len(proposee)) if proposee else 0.0
    tot = sum(taux.values())
    if tot == 0:
        return None, "options jamais vues", len(detail)
    return {k: v / tot for k, v in taux.items()}, "taux quand proposée", len(detail)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--conditions", required=True)
    ap.add_argument("--parts", required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--lang", default="fr")
    a = ap.parse_args()

    cond = json.loads(pathlib.Path(a.conditions).read_text(encoding="utf-8"))["conditions_finales"]
    parts = json.loads(pathlib.Path(a.parts).read_text(encoding="utf-8"))["decisions"]
    api = Api(lire_cle())

    pas = []
    r = api.post("/live", dict(cond, seed=a.seed, lang=a.lang))
    meta = r.get("meta")
    for _ in range(800):
        etat = r.get("state") or {}
        entree = {"age": etat.get("age"), "year": etat.get("year"), "events": r.get("events")}
        if r.get("ended") or not r.get("token"):
            entree["fin"] = r.get("death")
            entree["etat"] = etat
            pas.append(entree)
            break
        d = r.get("decision")
        if not d:
            pas.append(entree)
            r = api.post("/live", {"token": r["token"], "until": "decision"})
            continue
        menu = [c["key"] for c in d.get("choices", [])]
        est, methode, base = estimer(parts, d.get("id"), menu)
        if est:
            choisi = max(menu, key=lambda k: est[k])
        else:
            choisi = menu[0]
            methode += " → première option, À VÉRIFIER"
        entree.update({
            "decision": d,
            "parts_estimees": {k: round(v, 3) for k, v in (est or {}).items()},
            "methode": methode,
            "base": base,
            "choisi": choisi,
        })
        pas.append(entree)
        print(f"  {entree['age']:>3} ans · {d.get('id'):<12} → {choisi:<14} ({methode}, base {base})")
        r = api.post("/live", {"token": r["token"], "choose": choisi})

    out = {"meta": meta, "seed": a.seed, "conditions": cond, "regle": "à chaque décision, l'option la plus fréquente (estimée)",
           "parts_depuis": a.parts, "pas": pas, "appels": api.appels}
    pathlib.Path(a.sortie).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"écrit : {a.sortie} ({api.appels} appels)")


if __name__ == "__main__":
    main()
