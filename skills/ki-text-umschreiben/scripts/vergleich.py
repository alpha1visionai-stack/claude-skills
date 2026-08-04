#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vergleich.py — Zwei Textfassungen messen und gegenüberstellen.

Ruft `analyse.py` aus dem Skill ki-text-check für beide Fassungen auf und
zeigt, was sich verändert hat: welche KI-Indizien verschwunden sind, welche
noch stehen, welche Mensch-Signale dazugekommen sind.

Zusätzlich eine Inhaltsprüfung: Wenn beim Umschreiben zu viel Substanz
verloren geht, ist ein niedrigerer Indizienwert wertlos. Das Skript warnt,
wenn sich Länge oder Inhaltswortschatz zu stark verschoben haben.

Nutzung:
    python3 vergleich.py original.txt neu.txt
    python3 vergleich.py original.txt neu.txt --analyse /pfad/zu/analyse.py

Findet analyse.py automatisch, wenn ki-text-check als Skill installiert ist.
Nur Standardbibliothek. Läuft offline.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter

SUCHPFADE = [
    "~/.claude/skills/ki-text-check/scripts/analyse.py",
    "~/.config/claude/skills/ki-text-check/scripts/analyse.py",
    "../../ki-text-check/scripts/analyse.py",
    "../ki-text-check/scripts/analyse.py",
    "./ki-text-check/scripts/analyse.py",
]

STOPWOERTER = set("""der die das den dem des ein eine einer eines einem einen und oder aber
doch sondern denn wenn dass weil als wie so an auf aus bei bis durch für gegen in mit nach
ohne seit über um unter vor zu zum zur ist sind war waren sein seine seiner ihr ihre ihren
sich es er sie wir du ich man nicht auch nur noch schon mehr sehr kann können soll sollen
muss müssen wird werden würde haben hat hatte hatten dieser diese dieses am im vom beim
dann dort hier dabei damit dafür""".split())


def finde_analyse(explizit=None):
    if explizit:
        p = os.path.expanduser(explizit)
        if os.path.isfile(p):
            return p
        sys.exit(f"analyse.py nicht gefunden unter: {explizit}")
    if os.environ.get("KI_TEXT_CHECK_ANALYSE"):
        p = os.path.expanduser(os.environ["KI_TEXT_CHECK_ANALYSE"])
        if os.path.isfile(p):
            return p
    hier = os.path.dirname(os.path.abspath(__file__))
    for kand in SUCHPFADE:
        p = os.path.abspath(os.path.join(hier, os.path.expanduser(kand))) \
            if kand.startswith((".", "..")) else os.path.expanduser(kand)
        if os.path.isfile(p):
            return p
    sys.exit(
        "analyse.py nicht gefunden. Der Skill ki-text-check muss installiert "
        "sein, oder gib den Pfad mit --analyse an."
    )


def messe(analyse_pfad, textdatei):
    r = subprocess.run(
        [sys.executable, analyse_pfad, textdatei, "--nur-json"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if r.returncode != 0:
        sys.exit(f"Messung von {textdatei} fehlgeschlagen:\n{r.stderr.strip()}")
    return json.loads(r.stdout)


# Abstrakte Allerweltswörter und LLM-Vokabeln. Sie verschwinden beim
# Umschreiben planmäßig und dürfen nicht als Substanzverlust zählen.
FUELLBEGRIFFE = set("""bedeutung auswahl heutigen schnelllebigen arbeitswelt gewinnt
zunehmend herausforderung herausforderungen belegschaft ansatz elemente aspekte
faktoren möglichkeiten rahmen bereich hinblick zusammenhang grundlage basis
ganzheitlich nachhaltig innovativ maßgeschneidert vielfältig facettenreich
unerlässlich essenziell essentiell beleuchten navigieren nahtlos robust dynamisch
revolutionieren transformieren optimieren effizient wegweisend zukunftsweisend
bahnbrechend vielschichtig umfassend gezielt fundiert zielgerichtet strukturiert
systematisch wertvoll spannend beeindruckend bemerkenswert entscheidend elementar
signifikant landschaft ökosystem synergie mehrwert potenzial potenziale
schlüsselrolle meilenstein zentrale wichtige wesentliche spezifische individuellen
konkrete geeigneter passenden aktuellen kontinuierliche""".split())


def inhaltswoerter(pfad):
    with open(pfad, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    ws = re.findall(r"[A-Za-zÄÖÜäöüßẞ][A-Za-zÄÖÜäöüß\-']*", text.lower())
    inhalt = Counter(w for w in ws
                     if w not in STOPWOERTER and w not in FUELLBEGRIFFE and len(w) > 4)
    return inhalt, len(ws)


def themenwoerter(zaehler):
    """Trägerwörter des Originals: mehrfach genannt, also thematisch relevant.

    Ein reines Set aller Inhaltswörter taugt nicht als Maßstab — beim
    Umschreiben fallen planmäßig viele Einzelbegriffe weg, ohne dass eine
    Aussage verlorengeht. Mehrfach genannte Wörter tragen dagegen das Thema.
    """
    mehrfach = [w for w, c in zaehler.items() if c >= 2]
    if len(mehrfach) >= 6:
        return set(mehrfach)
    return set(w for w, _ in zaehler.most_common(15))


def inhaltspruefung(alt_pfad, neu_pfad):
    alt, n_alt = inhaltswoerter(alt_pfad)
    neu, n_neu = inhaltswoerter(neu_pfad)
    if not alt or not neu:
        return None
    thema = themenwoerter(alt)
    ueberlebt = thema & set(neu)
    behalten = len(ueberlebt) / len(thema) if thema else 1.0
    laengendelta = (n_neu - n_alt) / n_alt if n_alt else 0.0
    verloren = sorted(thema - set(neu), key=lambda w: -alt[w])[:12]
    warnungen = []
    if behalten < 0.50:
        warnungen.append(
            f"Nur {behalten:.0%} der Themenwörter des Originals kommen noch vor. "
            "Prüfen, ob eine tragende Aussage verlorengegangen ist.")
    if laengendelta < -0.30:
        warnungen.append(
            f"Die Fassung ist {abs(laengendelta):.0%} kürzer als das Original. "
            "Prüfen, ob Aussagen weggefallen sind.")
    elif laengendelta > 0.40:
        warnungen.append(
            f"Die Fassung ist {laengendelta:.0%} länger als das Original. "
            "Umschreiben soll nicht aufblähen — prüfen, ob Neues dazugekommen ist.")
    return {
        "themenwoerter_original": len(thema),
        "anteil_themenwoerter_behalten": round(behalten, 3),
        "laengenaenderung": round(laengendelta, 3),
        "woerter_alt": n_alt, "woerter_neu": n_neu,
        "nicht_mehr_vorhanden": verloren,
        "warnungen": warnungen,
    }


def indiz_index(befund):
    return {i["indiz"]: i for i in befund["indizien"]}


def main():
    ap = argparse.ArgumentParser(
        description="Zwei Textfassungen messen und gegenüberstellen.")
    ap.add_argument("original")
    ap.add_argument("neu")
    ap.add_argument("--analyse", help="Pfad zu analyse.py aus ki-text-check")
    ap.add_argument("--json", metavar="PFAD", help="Vergleich als JSON speichern")
    args = ap.parse_args()

    pfad = finde_analyse(args.analyse)
    a = messe(pfad, args.original)
    b = messe(pfad, args.neu)

    za, zb = a["zusammenfassung"], b["zusammenfassung"]
    ia, ib = indiz_index(a), indiz_index(b)

    weg = [k for k in ia if ia[k]["punkte"] > 0 and k not in ib]
    geblieben = [k for k in ia if ia[k]["punkte"] > 0 and k in ib]
    neu_ki = [k for k in ib if ib[k]["punkte"] > 0 and k not in ia]
    neu_mensch = [k for k in ib if ib[k]["punkte"] < 0 and k not in ia]
    weg_mensch = [k for k in ia if ia[k]["punkte"] < 0 and k not in ib]

    inhalt = inhaltspruefung(args.original, args.neu)

    print("=" * 68)
    print("VERGLEICH ORIGINAL → NEUE FASSUNG")
    print("=" * 68)
    print(f"Indizienwert:  {za['indizienwert']}  →  {zb['indizienwert']}"
          f"   ({zb['indizienwert'] - za['indizienwert']:+d})")
    print(f"Einordnung:    {za['einordnung']}")
    print(f"          →    {zb['einordnung']}")
    print()

    def kennzahl(name, pfad_a, pfad_b, block, schluessel, fmt="{:.3f}"):
        va, vb = pfad_a.get(block, {}).get(schluessel), pfad_b.get(block, {}).get(schluessel)
        if va is None or vb is None:
            return
        print(f"  {name:<34} {fmt.format(va):>8}  →  {fmt.format(vb):>8}")

    print("--- Kennzahlen " + "-" * 52)
    kennzahl("Satzlängen-Variationskoeffizient", a, b, "rhythmus", "variationskoeffizient")
    kennzahl("Anteil Sätze im ±25%-Korridor", a, b, "rhythmus", "anteil_im_25prozent_band")
    kennzahl("Sätze unter 5 Wörtern", a, b, "rhythmus", "kurzsaetze_unter_5_woerter", "{:.0f}")
    kennzahl("Konnektoren pro 100 Wörter", a, b, "phrasen", "konnektoren_pro_100", "{:.2f}")
    kennzahl("KI-Phrasen-Treffer", a, b, "phrasen", "ki_phrasen_treffer", "{:.0f}")
    kennzahl("KI-Vokabeln (verschieden)", a, b, "phrasen", "ki_vokabular_distinkt", "{:.0f}")
    kennzahl("Nominalisierungen pro 100", a, b, "lexik", "nominalisierungen_pro_100", "{:.2f}")
    kennzahl("Modalpartikeln pro 100", a, b, "menschsignale", "partikel_pro_100", "{:.2f}")
    kennzahl("Konkretheit pro 100", a, b, "menschsignale", "konkretheit_pro_100", "{:.2f}")
    kennzahl("Geviertstriche (—)", a, b, "typografie", "gedankenstrich_lang_em", "{:.0f}")
    print()

    print(f"--- Behoben ({len(weg)}) " + "-" * 45)
    for k in weg:
        print(f"  [+{ia[k]['punkte']:>2} entfällt] {k}")
    if not weg:
        print("  nichts")
    print()

    print(f"--- Noch offen ({len(geblieben)}) " + "-" * 42)
    for k in sorted(geblieben, key=lambda x: -ib[x]["punkte"]):
        print(f"  [+{ib[k]['punkte']:>2}] {k}")
        print(f"        {ib[k]['befund']}")
    if not geblieben:
        print("  nichts")
    print()

    if neu_mensch:
        print(f"--- Neue Mensch-Signale ({len(neu_mensch)}) " + "-" * 33)
        for k in neu_mensch:
            print(f"  [{ib[k]['punkte']:>3}] {k}")
        print()
    if neu_ki:
        print(f"--- Achtung: neue KI-Indizien ({len(neu_ki)}) " + "-" * 27)
        for k in neu_ki:
            print(f"  [+{ib[k]['punkte']:>2}] {k}  —  {ib[k]['befund']}")
        print()
    if weg_mensch:
        print(f"--- Verlorene Mensch-Signale ({len(weg_mensch)}) " + "-" * 28)
        for k in weg_mensch:
            print(f"  [{ia[k]['punkte']:>3}] {k}")
        print()

    if inhalt:
        print("--- Inhaltsprüfung " + "-" * 48)
        print(f"  Wörter: {inhalt['woerter_alt']} → {inhalt['woerter_neu']} "
              f"({inhalt['laengenaenderung']:+.0%})")
        print(f"  Themenwörter des Originals behalten: "
              f"{inhalt['anteil_themenwoerter_behalten']:.0%} "
              f"(von {inhalt['themenwoerter_original']})")
        if inhalt["nicht_mehr_vorhanden"]:
            print(f"  Themenwörter nicht mehr vorhanden: "
                  f"{', '.join(inhalt['nicht_mehr_vorhanden'])}")
        for w in inhalt["warnungen"]:
            print(f"  ACHTUNG: {w}")
        if not inhalt["warnungen"]:
            print("  Keine Auffälligkeiten — Substanz wirkt erhalten.")
        print()

    print("Ein niedrigerer Indizienwert allein ist kein Erfolg. Entscheidend "
          "ist,\ndass der Text dabei richtig, vollständig und lesbar geblieben "
          "ist.")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({
                "vorher": za, "nachher": zb,
                "behoben": weg, "noch_offen": geblieben,
                "neue_ki_indizien": neu_ki,
                "neue_mensch_signale": neu_mensch,
                "verlorene_mensch_signale": weg_mensch,
                "inhaltspruefung": inhalt,
            }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
