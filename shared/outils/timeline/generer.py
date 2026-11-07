#!/usr/bin/env python3
"""Génère la timeline de suivi d'une vidéo (une page HTML autonome) à partir du repo.

Sources lues :
  - videos/<slug>/storyboard.md      tableau des scènes (partie, fonction, procédé principal, fabrication) ;
  - videos/<slug>/scenes/*/scene.md  titre, durée, statut, production, plans (durée, matière, contenu, son) ;
  - videos/<slug>/script.md          voix off, textes à l'écran et indications, par scène ;
  - videos/<slug>/suivi.json         étapes globales, scène en cours, points à appliquer et à décider.

Sortie : videos/<slug>/suivi/timeline.html (le gabarit est shared/outils/timeline/gabarit.html).

Usage :
  python shared/outils/timeline/generer.py 2026-11-quelle-aurait-du-etre-ta-vie
"""
import datetime
import io
import json
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parents[3]
GABARIT = pathlib.Path(__file__).with_name("gabarit.html")
MATIERES = ("3D", "UI", "MD", "IMG", "NOIR")


def lire(p):
    return io.open(p, encoding="utf-8").read()


def cellules(ligne):
    return [c.strip() for c in ligne.strip().strip("|").split("|")]


def nettoyer(t):
    """Retire le gras et le code Markdown pour l'affichage."""
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"~~(.+?)~~", r"\1", t)
    return t.strip()


def secondes(texte):
    m = re.search(r"(\d+)\s*s\b", texte)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+):(\d{2})", texte)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    return 0


def scenes_du_storyboard(sb):
    out = {}
    for l in sb.split("\n"):
        m = re.match(r"\| (S\d\d) \|", l)
        if not m:
            continue
        c = cellules(l)
        if len(c) < 9:
            continue
        out[m.group(1)] = {
            "partie": nettoyer(c[1]),
            "resume": nettoyer(c[2]),
            "fonction": nettoyer(c[3]),
            "procede": nettoyer(c[4]),
            "secondaires": nettoyer(c[5]),
            "duree_sb": nettoyer(c[7]),
            "fabrication": nettoyer(c[8]),
        }
    return out


def fiche(p):
    s = lire(p)
    titre = s.split("\n", 1)[0].lstrip("# ").strip()
    def champ(nom):
        m = re.search(r"\| \*\*" + re.escape(nom) + r"\*\* \| (.+?) \|\n", s)
        return nettoyer(m.group(1)) if m else ""
    intention = ""
    m = re.search(r"## Intention\n(.+?)\n## ", s, re.S)
    if m:
        intention = nettoyer(m.group(1))
    plans = []
    for l in s.split("\n"):
        if re.match(r"\| S\d\d-P\d\d \|", l):
            c = cellules(l)
            mat = c[2].upper() if len(c) > 2 else ""
            plans.append({
                "id": c[0],
                "duree": secondes(c[1]),
                "matiere": mat if mat in MATIERES else "MD",
                "contenu": nettoyer(c[3]) if len(c) > 3 else "",
                "animation": nettoyer(c[4]) if len(c) > 4 else "",
                "procede": nettoyer(c[5]) if len(c) > 5 else "",
                "son": nettoyer(c[6]) if len(c) > 6 else "",
            })
    return {
        "titre": titre,
        "duree_fiche": champ("Durée"),
        "statut": champ("Statut"),
        "production": champ("Production") or "à faire",
        "intention": intention,
        "plans": plans,
    }


def script_par_scene(sc):
    out = {}
    blocs = re.split(r"\n## (S\d\d) · ", "\n" + sc)
    for i in range(1, len(blocs) - 1, 2):
        sid, corps = blocs[i], blocs[i + 1]
        corps = corps.split("\n## ", 1)[0]
        lignes = []
        for l in corps.split("\n")[1:]:
            l = l.rstrip()
            if l.startswith("> "):
                lignes.append({"type": "voix", "texte": nettoyer(l[2:])})
            elif l.startswith("ÉCRAN"):
                lignes.append({"type": "ecran", "texte": nettoyer(l.split(":", 1)[1]) if ":" in l else nettoyer(l)})
            elif l.startswith("["):
                lignes.append({"type": "jeu", "texte": nettoyer(l.strip("[]"))})
        mots = sum(len(re.findall(r"[\wÀ-ÿ'’-]+", x["texte"])) for x in lignes if x["type"] == "voix")
        out[sid] = {"lignes": lignes, "mots": mots}
    return out


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "2026-11-quelle-aurait-du-etre-ta-vie"
    base = RACINE / "videos" / slug
    suivi = json.loads(lire(base / "suivi.json"))
    sb = scenes_du_storyboard(lire(base / "storyboard.md"))
    sc = script_par_scene(lire(base / "script.md"))

    scenes = []
    for p in sorted((base / "scenes").glob("S*/scene.md")):
        sid = p.parent.name
        f = fiche(p)
        d = dict(id=sid, **f, **sb.get(sid, {}))
        d["voix"] = sc.get(sid, {"lignes": [], "mots": 0})
        d["duree"] = sum(x["duree"] for x in f["plans"]) or secondes(f["duree_fiche"]) or secondes(sb.get(sid, {}).get("duree_sb", ""))
        scenes.append(d)

    # Ordre de montage : l'interlude S06 revient après les scènes listées dans suivi.json
    par_id = {s["id"]: s for s in scenes}
    apres = suivi.get("interludes_S06_apres") or []
    ordre = []
    n = 0
    for s in scenes:
        if s["id"] == "S06":
            continue
        ordre.append({"id": s["id"], "occurrence": None})
        if s["id"] in apres and "S06" in par_id:
            n += 1
            ordre.append({"id": "S06", "occurrence": n})

    data = {
        "slug": slug,
        "genere": datetime.datetime.now().strftime("%d/%m/%Y à %H:%M"),
        "suivi": suivi,
        "scenes": par_id,
        "ordre": ordre,
        "interludes": len(apres),
    }
    html = lire(GABARIT).replace("/*__DONNEES__*/null", json.dumps(data, ensure_ascii=False))
    sortie = base / "suivi" / "timeline.html"
    sortie.parent.mkdir(exist_ok=True)
    io.open(sortie, "w", encoding="utf-8", newline="\n").write(html)
    total = sum(par_id[o["id"]]["duree"] for o in ordre)
    print(f"écrit : {sortie.relative_to(RACINE)} · {len(scenes)} scènes · {len(ordre)} blocs · {total // 60} min {total % 60:02d} s d'image")


if __name__ == "__main__":
    main()
