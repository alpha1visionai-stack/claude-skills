#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyse.py — Messbare Stilsignale eines deutschen Textes erheben.

Das Skript trifft KEINE Entscheidung "KI oder Mensch". Es misst Merkmale,
die in KI-Texten statistisch anders verteilt sind als in menschlichen, und
liefert sie als Belege mit Fundstellen. Die Bewertung macht das Modell,
das dieses Skript aufruft — mit Blick auf Kontext, Textsorte und Zweck.

Nutzung:
    python3 analyse.py text.txt
    python3 analyse.py text.txt --json befund.json
    cat text.txt | python3 analyse.py -

Nur Standardbibliothek. Läuft offline. Der Text verlässt das System nicht.
"""

import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter

# --------------------------------------------------------------------------
# Wortlisten
# --------------------------------------------------------------------------

# Formulierungen, die in deutschen LLM-Ausgaben auffällig häufig auftreten.
# Regex, case-insensitive. Ein Treffer ist kein Beweis — Häufung ist das Signal.
KI_PHRASEN = [
    r"es ist wichtig(?:,| zu)\s*(?:zu\s+)?(?:betonen|erwähnen|beachten|verstehen|festzuhalten)",
    r"es sei (?:darauf hingewiesen|angemerkt|erwähnt)",
    r"es gilt zu (?:beachten|bedenken)",
    r"in der heutigen (?:zeit|welt|schnelllebigen|digitalen)",
    r"in einer welt, in der",
    r"zusammenfassend lässt sich (?:sagen|festhalten)",
    r"insgesamt lässt sich (?:sagen|festhalten)",
    r"abschließend lässt sich",
    r"(?:eine|die) (?:entscheidende|zentrale|wichtige|wesentliche) rolle spielen",
    r"von (?:entscheidender|zentraler|großer) bedeutung",
    r"spielt eine (?:entscheidende|wichtige|zentrale) rolle",
    r"nicht nur\b[^.!?]{3,80}\bsondern auch",
    r"sowohl\b[^.!?]{3,60}\bals auch",
    r"lassen sie uns",
    r"tauchen wir ein",
    r"(?:tiefer|näher) ein(?:zu)?tauchen",
    r"in diesem (?:artikel|beitrag|abschnitt|leitfaden) (?:werden wir|erfahren sie|zeigen wir)",
    r"die welt der\b",
    r"ein (?:echter|wahrer) gamechanger",
    r"der schlüssel zum erfolg",
    r"das a und o",
    r"türen öffnen",
    r"potenzial (?:voll )?(?:aus)?schöpfen",
    r"auf die nächste stufe",
    r"maßgeschneiderte lösung",
    r"ganzheitlicher ansatz",
    r"es lohnt sich,\s+\w+",
    r"bitte beachten sie, dass",
    r"ich hoffe, (?:dieser|diese|das) \w+ hilft",
    r"wenn (?:du|sie) (?:weitere|noch) fragen ha(?:st|ben)",
    r"als (?:ki|künstliche intelligenz|sprachmodell)",
    r"(?:vor|nach)teile? (?:und|sowie) (?:nach|vor)teile",
    r"herausforderungen und (?:chancen|möglichkeiten)",
    r"chancen und (?:herausforderungen|risiken)",
    r"es gibt (?:jedoch )?(?:auch )?(?:einige )?herausforderungen",
    r"nicht zuletzt",
    r"letztlich geht es darum",
    r"im laufe der (?:zeit|jahre)",
    r"vor diesem hintergrund",
    r"gewinnt (?:zunehmend|immer mehr) an bedeutung",
    r"rückt (?:zunehmend|immer mehr) in den (?:fokus|mittelpunkt)",
    r"stellt (?:sicher|einen wichtigen)",
    r"trägt (?:maßgeblich|entscheidend) dazu bei",
    r"ermöglicht es (?:ihnen|dir|unternehmen)",
    r"eröffnet neue (?:möglichkeiten|perspektiven|wege)",
]

# Einzelvokabeln mit auffälligem LLM-Bias im Deutschen.
KI_VOKABULAR = [
    "ganzheitlich", "nachhaltig", "innovativ", "maßgeschneidert", "vielfältig",
    "facettenreich", "unerlässlich", "essenziell", "essentiell", "beleuchten",
    "navigieren", "nahtlos", "robust", "dynamisch", "revolutionieren",
    "transformieren", "optimieren", "effizient", "wegweisend", "zukunftsweisend",
    "bahnbrechend", "vielschichtig", "umfassend", "gezielt", "fundiert",
    "zielgerichtet", "strukturiert", "systematisch", "wertvoll", "spannend",
    "beeindruckend", "bemerkenswert", "entscheidend", "elementar", "signifikant",
    "immens", "enorm", "landschaft", "reise", "ökosystem", "synergie",
    "mehrwert", "potenzial", "schlüsselrolle", "meilenstein", "leuchtturm",
]

# Konnektoren, die KI-Texte überproportional als Satzklammer nutzen.
KONNEKTOREN = [
    "darüber hinaus", "zudem", "ferner", "des weiteren", "weiterhin",
    "folglich", "somit", "dementsprechend", "demzufolge", "infolgedessen",
    "insbesondere", "hierbei", "dabei ist", "gleichzeitig", "andererseits",
    "einerseits", "zusätzlich", "überdies", "letztendlich", "letztlich",
    "grundsätzlich", "prinzipiell", "in diesem zusammenhang", "vor allem",
]

# Modalpartikeln, Füllwörter und Umgangssprache — starke Mensch-Signale.
# LLMs schreiben sie in nüchternen Sachtexten fast nie von selbst.
MENSCH_PARTIKELN = [
    "halt", "irgendwie", "irgendwo", "eigentlich", "sowieso", "eh",
    "naja", "na ja", "tja", "also", "ja gut", "wobei", "quasi",
    "ziemlich", "echt", "krass", "bisschen", "bissl", "mal eben",
    "schlicht", "einfach mal", "ehrlich gesagt", "um ehrlich zu sein",
    "meines wissens", "ich glaube", "ich denke", "ich finde", "ich meine",
    "keine ahnung", "gefühlt", "vermutlich", "wahrscheinlich eher",
    "jedenfalls", "übrigens", "apropos", "nebenbei", "kurzum",
    "schon klar", "im prinzip", "so oder so", "auf jeden fall",
]

# Umgangssprachliche Verkürzungen / gesprochene Formen.
UMGANGSFORMEN = [
    r"\bhab\b", r"\bhabs\b", r"\bnix\b", r"\bwas\b\s+für\s+ein",
    r"\bkriegen\b", r"\bkriegt\b", r"\bgucken\b", r"\bguckt\b",
    r"\bne\b(?!\w)", r"\bnee\b", r"\bmal\s+kurz\b", r"\bnochmal\b",
    r"\w+'s\b", r"\bgeht's\b", r"\bhab's\b", r"\bwill's\b",
    r"\bsone\b", r"\bsowas\b", r"\birgendwann\b", r"\bzig\b",
    r"\bdrauf\b", r"\bdran\b", r"\brum\b", r"\braus\b", r"\brein\b",
]

# Deutsche Abkürzungen, die keinen Satzende-Punkt setzen.
ABKUERZUNGEN = [
    "z.B.", "z. B.", "u.a.", "u. a.", "d.h.", "d. h.", "bzw.", "usw.",
    "etc.", "ca.", "evtl.", "ggf.", "inkl.", "exkl.", "Nr.", "Abs.",
    "Art.", "Dr.", "Prof.", "Hr.", "Fr.", "Mio.", "Mrd.", "Tsd.",
    "S.", "vgl.", "sog.", "u.U.", "i.d.R.", "o.ä.", "u.ä.", "Str.",
]

STOPWOERTER = set("""der die das den dem des ein eine einer eines einem einen und oder aber
doch sondern denn wenn dass weil als wie so an auf aus bei bis durch für gegen in mit nach
ohne seit über um unter vor zu zum zur ist sind war waren sein seine seiner ihr ihre ihren
sich es er sie wir ihr du ich man nicht auch nur noch schon mehr sehr kann können soll
sollen muss müssen wird werden würde haben hat hatte hatten dieser diese dieses am im
vom beim zur dann dort hier dabei damit dafür""".split())


# --------------------------------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------------------------------

def satz_split(text):
    """Text in Sätze zerlegen, deutsche Abkürzungen schützen."""
    geschuetzt = text
    for i, abk in enumerate(ABKUERZUNGEN):
        geschuetzt = geschuetzt.replace(abk, abk.replace(".", "\x00"))
    teile = re.split(r"(?<=[.!?…])[\s\n]+|\n{2,}", geschuetzt)
    saetze = []
    for t in teile:
        t = t.replace("\x00", ".").strip()
        if len(re.findall(r"\w", t)) >= 2:
            saetze.append(t)
    return saetze


def woerter(text):
    return re.findall(r"[A-Za-zÄÖÜäöüßẞ][A-Za-zÄÖÜäöüß\-']*", text)


def stdev(werte):
    if len(werte) < 2:
        return 0.0
    m = sum(werte) / len(werte)
    return math.sqrt(sum((w - m) ** 2 for w in werte) / (len(werte) - 1))


def pro100(n, gesamt):
    return round(100.0 * n / gesamt, 2) if gesamt else 0.0


def schnipsel(text, treffer, laenge=70):
    """Kurzen Kontext um einen Regex-Treffer ausgeben."""
    a = max(0, treffer.start() - laenge // 2)
    b = min(len(text), treffer.end() + laenge // 2)
    s = text[a:b].replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return ("…" if a > 0 else "") + s + ("…" if b < len(text) else "")


# --------------------------------------------------------------------------
# Messungen
# --------------------------------------------------------------------------

def mess_rhythmus(saetze):
    laengen = [len(woerter(s)) for s in saetze]
    laengen = [l for l in laengen if l > 0]
    if not laengen:
        return {}
    m = sum(laengen) / len(laengen)
    sd = stdev(laengen)
    cv = sd / m if m else 0.0
    band = [l for l in laengen if abs(l - m) <= 0.25 * m]
    erste = [woerter(s)[0].lower() for s in saetze if woerter(s)]
    kommas = [s.count(",") for s in saetze]
    return {
        "saetze": len(saetze),
        "wortlaenge_mittel": round(m, 1),
        "wortlaenge_sd": round(sd, 1),
        "variationskoeffizient": round(cv, 3),
        "kuerzester_satz": min(laengen),
        "laengster_satz": max(laengen),
        "anteil_im_25prozent_band": round(len(band) / len(laengen), 3),
        "satzanfang_diversitaet": round(len(set(erste)) / len(erste), 3) if erste else 0.0,
        "haeufigster_satzanfang": Counter(erste).most_common(3),
        "kommas_pro_satz": round(sum(kommas) / len(saetze), 2),
        "saetze_ohne_komma_anteil": round(sum(1 for k in kommas if k == 0) / len(saetze), 3),
        "kurzsaetze_unter_5_woerter": sum(1 for l in laengen if l < 5),
    }


def mess_absaetze(text):
    abs_ = [a.strip() for a in re.split(r"\n\s*\n", text) if a.strip()]
    if len(abs_) < 2:
        return {"absaetze": len(abs_)}
    laengen = [len(woerter(a)) for a in abs_]
    m = sum(laengen) / len(laengen)
    return {
        "absaetze": len(abs_),
        "absatzlaenge_mittel": round(m, 1),
        "absatzlaenge_sd": round(stdev(laengen), 1),
        "absatz_variationskoeffizient": round(stdev(laengen) / m, 3) if m else 0.0,
        "absatzlaengen": laengen[:25],
    }


def mess_lexik(text):
    ws = [w.lower() for w in woerter(text)]
    if not ws:
        return {}
    n = len(ws)
    counts = Counter(ws)
    hapax = sum(1 for c in counts.values() if c == 1)
    # MATTR: Type-Token-Ratio im gleitenden Fenster (robust gegen Textlänge)
    fenster = 100
    if n >= fenster:
        ttrs = [len(set(ws[i:i + fenster])) / fenster
                for i in range(0, n - fenster + 1, 10)]
        mattr = sum(ttrs) / len(ttrs)
        mattr_sd = stdev(ttrs)
    else:
        mattr, mattr_sd = len(set(ws)) / n, 0.0
    inhalt = Counter(w for w in ws if w not in STOPWOERTER and len(w) > 3)
    nominal = len(re.findall(
        r"\w{4,}(?:ung|heit|keit|tät|ität|ismus|ierung|barkeit|schaft|nis)\b",
        text, re.IGNORECASE))
    lang = sum(1 for w in ws if len(w) > 12)
    return {
        "woerter": n,
        "unterschiedliche_woerter": len(counts),
        "hapax_anteil": round(hapax / len(counts), 3),
        "mattr_100": round(mattr, 3),
        "mattr_streuung": round(mattr_sd, 3),
        "wortlaenge_mittel_zeichen": round(sum(len(w) for w in ws) / n, 2),
        "anteil_woerter_ueber_12_zeichen": round(lang / n, 3),
        "nominalisierungen_pro_100": pro100(nominal, n),
        "top_inhaltswoerter": inhalt.most_common(8),
    }


def mess_typografie(text):
    zw = sum(1 for ch in text if unicodedata.category(ch) == "Cf")
    return {
        "gedankenstrich_lang_em": text.count("—"),
        "gedankenstrich_halb_en": len(re.findall(r"\s–\s", text)),
        "bindestrich_als_gedankenstrich": len(re.findall(r"\s-\s", text)),
        "anfuehrung_typografisch_de": text.count("„") + text.count("“"),
        "anfuehrung_typografisch_en": text.count("“") + text.count("”"),
        "anfuehrung_gerade": text.count('"'),
        "apostroph_typografisch": text.count("’"),
        "doppelpunkte": text.count(":"),
        "semikola": text.count(";"),
        "ausrufezeichen": text.count("!"),
        "fragezeichen": text.count("?"),
        "auslassung_zeichen": text.count("…"),
        "auslassung_dreipunkt": len(re.findall(r"\.\.\.", text)),
        "klammerpaare": min(text.count("("), text.count(")")),
        "nbsp": text.count(" "),
        "schmale_leerzeichen": text.count(" ") + text.count(" "),
        "zero_width_und_steuerzeichen": zw,
        "doppelte_leerzeichen": len(re.findall(r"(?<=\S)  +(?=\S)", text)),
        "markdown_fett": len(re.findall(r"\*\*[^*\n]{2,60}\*\*", text)),
        "markdown_bullets": len(re.findall(r"^\s*[-*•]\s+", text, re.MULTILINE)),
        "markdown_bullet_fett_leadin": len(re.findall(
            r"^\s*[-*•]\s+\*\*[^*\n]{2,50}\*\*\s*[:–—-]", text, re.MULTILINE)),
        "markdown_ueberschriften": len(re.findall(r"^#{1,6}\s+\S", text, re.MULTILINE)),
        "emoji_oder_symbole": len([ch for ch in text
                                   if unicodedata.category(ch) == "So"]),
    }


def mess_phrasen(text):
    treffer, belege = [], []
    for p in KI_PHRASEN:
        for m in re.finditer(p, text, re.IGNORECASE):
            treffer.append(p)
            belege.append({"muster": p, "stelle": schnipsel(text, m)})
            break  # ein Beleg pro Muster genügt
    ws = [w.lower() for w in woerter(text)]
    n = len(ws) or 1
    vok = Counter(w for w in ws if w in KI_VOKABULAR)
    konn = []
    tl = text.lower()
    for k in KONNEKTOREN:
        c = len(re.findall(r"\b" + re.escape(k) + r"\b", tl))
        if c:
            konn.append((k, c))
    konn_gesamt = sum(c for _, c in konn)
    # Dreierketten "A, B und C" — LLM-Lieblingsrhythmus
    dreier = len(re.findall(
        r"\b\w{4,}(?:e|en|er|es)?,\s+\w{4,}(?:e|en|er|es)?\s+und\s+\w{4,}", text))
    return {
        "ki_phrasen_treffer": len(treffer),
        "ki_phrasen_belege": belege[:15],
        "ki_vokabular_distinkt": len(vok),
        "ki_vokabular_gesamt": sum(vok.values()),
        "ki_vokabular_top": vok.most_common(10),
        "ki_vokabular_pro_100": pro100(sum(vok.values()), n),
        "konnektoren_distinkt": len(konn),
        "konnektoren_gesamt": konn_gesamt,
        "konnektoren_pro_100": pro100(konn_gesamt, n),
        "konnektoren_top": sorted(konn, key=lambda x: -x[1])[:10],
        "dreierketten": dreier,
    }


def mess_menschsignale(text):
    ws = [w.lower() for w in woerter(text)]
    n = len(ws) or 1
    tl = text.lower()
    partikel = []
    for p in MENSCH_PARTIKELN:
        c = len(re.findall(r"\b" + re.escape(p) + r"\b", tl))
        if c:
            partikel.append((p, c))
    partikel_gesamt = sum(c for _, c in partikel)
    umgang = []
    for p in UMGANGSFORMEN:
        c = len(re.findall(p, tl))
        if c:
            umgang.append((p, c))
    ich = len(re.findall(r"\b(?:ich|mir|mich|mein|meine|meiner|meinem|meinen)\b", tl))
    # Tippfehler- und Schlampigkeits-Proxies
    doppelwort = re.findall(r"\b(\w{3,})\s+\1\b", tl)
    komma_ohne_space = len(re.findall(r"\w,\w", text))
    punkt_ohne_space = len(re.findall(r"[a-zäöüß]\.[A-ZÄÖÜ]", text))
    gemischte_quotes = sum(1 for x in [text.count("„") > 0,
                                       text.count('"') > 0,
                                       text.count("“") > 0] if x)
    mehrfach_satzzeichen = len(re.findall(r"[!?]{2,}", text))
    # Konkretheit: Zahlen, Daten, Beträge, URLs, Uhrzeiten
    zahlen = len(re.findall(r"\b\d+(?:[.,]\d+)?\b", text))
    daten = len(re.findall(r"\b\d{1,2}\.\s*\d{1,2}\.\s*\d{2,4}\b|\b(?:19|20)\d{2}\b", text))
    betraege = len(re.findall(r"(?:€|EUR|\$|USD|CHF)\s*\d|\d+\s*(?:€|EUR|Euro)", text))
    urls = len(re.findall(r"https?://|www\.", text))
    prozent = len(re.findall(r"\d+\s*(?:%|Prozent)", text))
    return {
        "partikel_distinkt": len(partikel),
        "partikel_gesamt": partikel_gesamt,
        "partikel_pro_100": pro100(partikel_gesamt, n),
        "partikel_top": sorted(partikel, key=lambda x: -x[1])[:10],
        "umgangsformen_distinkt": len(umgang),
        "umgangsformen_gesamt": sum(c for _, c in umgang),
        "ich_perspektive_pro_100": pro100(ich, n),
        "doppelte_woerter": len(doppelwort),
        "doppelte_woerter_beispiele": doppelwort[:5],
        "komma_ohne_leerzeichen": komma_ohne_space,
        "punkt_ohne_leerzeichen": punkt_ohne_space,
        "gemischte_anfuehrungsstile": gemischte_quotes,
        "mehrfache_satzzeichen": mehrfach_satzzeichen,
        "zahlen": zahlen,
        "jahreszahlen_und_daten": daten,
        "geldbetraege": betraege,
        "urls": urls,
        "prozentangaben": prozent,
        "konkretheit_pro_100": pro100(zahlen + daten + betraege + urls + prozent, n),
    }


# --------------------------------------------------------------------------
# Indizienbewertung
# --------------------------------------------------------------------------

def bewerte(r, a, l, t, p, h):
    """Gewichtete Indizien sammeln. Positiv = KI-Richtung, negativ = Mensch."""
    ind = []

    def add(punkte, name, befund):
        ind.append({"punkte": punkte, "indiz": name, "befund": befund})

    n_saetze = r.get("saetze", 0)
    n_woerter = l.get("woerter", 0)

    # --- Rhythmus -------------------------------------------------------
    cv = r.get("variationskoeffizient", 0)
    if n_saetze >= 8:
        if cv < 0.30:
            add(13, "Satzlängen fast gleichförmig",
                f"Variationskoeffizient {cv} (menschliche Prosa liegt meist 0,45–0,80)")
        elif cv < 0.42:
            add(7, "Satzlängen auffällig gleichmäßig", f"Variationskoeffizient {cv}")
        elif cv > 0.85:
            add(-9, "Satzlängen stark schwankend",
                f"Variationskoeffizient {cv} — typisch für spontan geschriebenen Text")
        elif cv > 0.68:
            add(-5, "Satzlängen natürlich schwankend", f"Variationskoeffizient {cv}")

        band = r.get("anteil_im_25prozent_band", 0)
        if band > 0.60:
            add(8, "Satzlängen im engen Korridor",
                f"{int(band*100)} % aller Sätze liegen ±25 % um den Mittelwert")

        sd = r.get("satzanfang_diversitaet", 1)
        if sd < 0.55:
            add(6, "Wiederkehrende Satzanfänge",
                f"nur {int(sd*100)} % der Sätze beginnen mit einem neuen Wort; "
                f"häufigste: {r.get('haeufigster_satzanfang')}")
        elif sd > 0.88 and n_saetze >= 20:
            add(-3, "Vielfältige Satzanfänge", f"Diversität {sd}")

        if r.get("kurzsaetze_unter_5_woerter", 0) >= max(2, n_saetze * 0.12):
            add(-6, "Mehrere sehr kurze Sätze / Fragmente",
                f"{r['kurzsaetze_unter_5_woerter']} Sätze unter 5 Wörtern")
        if r.get("kurzsaetze_unter_5_woerter", 0) == 0 and n_saetze >= 15:
            add(4, "Kein einziger kurzer Satz",
                "gleichmäßig ausformulierte Sätze über den ganzen Text")

    if a.get("absaetze", 0) >= 5:
        acv = a.get("absatz_variationskoeffizient", 0)
        if acv < 0.15:
            add(8, "Absätze gleich lang zugeschnitten",
                f"Absatz-Variationskoeffizient {acv}, Längen {a.get('absatzlaengen')}")
        elif acv < 0.25:
            add(4, "Absätze ähnlich lang",
                f"Absatz-Variationskoeffizient {acv}, Längen {a.get('absatzlaengen')}")
        elif acv > 0.70:
            add(-4, "Absätze ungleich lang", f"Variationskoeffizient {acv}")

    # --- Lexik ----------------------------------------------------------
    if n_woerter >= 120:
        nom = l.get("nominalisierungen_pro_100", 0)
        if nom > 7:
            add(6, "Ausgeprägter Nominalstil",
                f"{nom} Nominalisierungen pro 100 Wörter (-ung/-heit/-keit/-ierung)")
        elif nom < 1.5 and n_woerter >= 150:
            add(-4, "Kaum Nominalstil",
                f"nur {nom} Nominalisierungen pro 100 Wörter — verbnaher, "
                "gesprochener Satzbau")
        lang = l.get("anteil_woerter_ueber_12_zeichen", 0)
        if lang > 0.09:
            add(4, "Viele Langkomposita", f"{int(lang*100)} % der Wörter über 12 Zeichen")
        ms = l.get("mattr_streuung", 1)
        if ms and ms < 0.035 and n_woerter >= 300:
            add(5, "Wortschatzdichte auffällig konstant",
                f"Streuung der gleitenden Type-Token-Ratio nur {ms}")

    # --- Typografie -----------------------------------------------------
    em = t.get("gedankenstrich_lang_em", 0)
    if em >= 3:
        add(11, "Häufiger Geviertstrich (—)",
            f"{em}× — im deutschen Tastaturalltag praktisch nicht getippt")
    elif em >= 1:
        add(6, "Geviertstrich (—) vorhanden", f"{em}×")

    if (t.get("nbsp", 0) or t.get("zero_width_und_steuerzeichen", 0)
            or t.get("schmale_leerzeichen", 0)):
        add(6, "Unsichtbare Sonderzeichen im Text",
            f"NBSP: {t.get('nbsp')}, Steuer-/Zero-Width-Zeichen: "
            f"{t.get('zero_width_und_steuerzeichen')} — Copy-Paste aus einer Web-Oberfläche")

    if t.get("markdown_bullet_fett_leadin", 0) >= 2:
        add(9, "Listen im Muster „**Begriff**: Erklärung“",
            f"{t['markdown_bullet_fett_leadin']}× — charakteristische LLM-Listenform")
    elif t.get("markdown_fett", 0) >= 5 and t.get("markdown_bullets", 0) >= 3:
        add(5, "Stark durchformatierte Struktur",
            f"{t['markdown_fett']} Fettungen, {t['markdown_bullets']} Listenpunkte")

    if n_saetze >= 20 and t.get("ausrufezeichen", 0) == 0 \
            and t.get("fragezeichen", 0) == 0:
        add(3, "Keine Ausrufe- oder Fragezeichen", "durchgehend neutraler Aussagemodus")
    if n_saetze >= 12:
        dp = t.get("doppelpunkte", 0)
        if dp >= n_saetze * 0.30:
            add(4, "Hohe Doppelpunktdichte", f"{dp} Doppelpunkte auf {n_saetze} Sätze")

    if t.get("auslassung_zeichen", 0) >= 1 and t.get("auslassung_dreipunkt", 0) == 0:
        add(3, "Typografisches Auslassungszeichen (…)",
            f"{t['auslassung_zeichen']}× statt drei getippter Punkte")

    if n_woerter >= 300 and t.get("doppelte_leerzeichen", 0) == 0 \
            and h.get("komma_ohne_leerzeichen", 0) == 0 \
            and h.get("punkt_ohne_leerzeichen", 0) == 0 \
            and h.get("doppelte_woerter", 0) == 0:
        add(6, "Keine einzige Tippunsauberkeit",
            "über den ganzen Text keine doppelten Leerzeichen, "
            "Komma-/Punktfehler oder Wortdoppler")

    # --- Floskeln -------------------------------------------------------
    ph = p.get("ki_phrasen_treffer", 0)
    if ph:
        add(min(24, 5 * ph), f"{ph} KI-typische Formulierungsmuster",
            "; ".join(b["stelle"] for b in p.get("ki_phrasen_belege", [])[:4]))

    vok = p.get("ki_vokabular_distinkt", 0)
    if vok >= 6:
        add(min(12, 2 * vok), f"{vok} verschiedene LLM-Lieblingsvokabeln",
            str(p.get("ki_vokabular_top")))
    elif vok >= 3:
        add(5, f"{vok} LLM-Lieblingsvokabeln", str(p.get("ki_vokabular_top")))

    kp = p.get("konnektoren_pro_100", 0)
    if kp > 2.2:
        add(9, "Konnektoren-Überschuss",
            f"{kp} Bindewörter pro 100 Wörter ({p.get('konnektoren_top')})")
    elif kp > 1.4:
        add(5, "Erhöhte Konnektoren-Dichte", f"{kp} pro 100 Wörter")

    if n_saetze >= 8 and p.get("dreierketten", 0) >= max(2, n_saetze * 0.15):
        add(5, "Häufige Dreierketten („A, B und C“)",
            f"{p['dreierketten']} Vorkommen auf {n_saetze} Sätze")

    # --- Mensch-Signale -------------------------------------------------
    pp = h.get("partikel_pro_100", 0)
    if pp > 1.2:
        add(-12, "Viele Modalpartikeln und Füllwörter",
            f"{pp} pro 100 Wörter ({h.get('partikel_top')})")
    elif pp > 0.5:
        add(-7, "Modalpartikeln vorhanden", f"{pp} pro 100 Wörter ({h.get('partikel_top')})")
    elif pp < 0.1 and n_woerter >= 150:
        add(5, "Keine Modalpartikeln",
            "kein „halt“, „eigentlich“, „irgendwie“, „naja“ im ganzen Text")

    if h.get("umgangsformen_distinkt", 0) >= 3:
        add(-8, "Umgangssprachliche Formen",
            f"{h['umgangsformen_gesamt']} Treffer in {h['umgangsformen_distinkt']} Varianten")

    unsauber = (h.get("doppelte_woerter", 0) + h.get("komma_ohne_leerzeichen", 0)
                + h.get("punkt_ohne_leerzeichen", 0) + h.get("mehrfache_satzzeichen", 0))
    if unsauber >= 3:
        add(-11, "Mehrere Tippunsauberkeiten",
            f"{unsauber} Fundstellen (Wortdoppler, fehlende Leerzeichen, „!!“)")
    elif unsauber >= 1:
        add(-6, "Tippunsauberkeit vorhanden", f"{unsauber} Fundstelle(n)")

    if h.get("gemischte_anfuehrungsstile", 0) >= 2:
        add(-5, "Gemischte Anführungszeichen-Stile",
            "typisch für zusammenkopierte oder von Hand getippte Texte")

    ich = h.get("ich_perspektive_pro_100", 0)
    if ich > 1.5:
        add(-6, "Deutliche Ich-Perspektive", f"{ich} Ich-Bezüge pro 100 Wörter")

    kk = h.get("konkretheit_pro_100", 0)
    if kk > 1.5:
        add(-6, "Hohe Konkretheit",
            f"{kk} Zahlen/Daten/Beträge/URLs pro 100 Wörter — "
            "überprüfbare Details, die Modelle selten frei erfinden")
    elif kk < 0.3 and n_woerter >= 150:
        add(4, "Kaum überprüfbare Details",
            "fast keine Zahlen, Daten, Namen oder Beträge")

    return ind


def score_und_band(indizien, n_woerter):
    rohsumme = sum(i["punkte"] for i in indizien)
    # Kurze Texte liefern zu wenig Evidenz für klare Aussagen. Die Dämpfung
    # zieht das Ergebnis bewusst zur Mitte, damit der Befund nicht mehr
    # Sicherheit behauptet als das Material trägt.
    daempfung = min(1.0, max(0.45, n_woerter / 400.0))
    summe = int(round(rohsumme * daempfung))
    score = max(0, min(100, 50 + summe))
    if n_woerter < 80:
        verlaesslichkeit = "sehr gering"
    elif n_woerter < 200:
        verlaesslichkeit = "gering"
    elif n_woerter < 500:
        verlaesslichkeit = "mittel"
    else:
        verlaesslichkeit = "brauchbar"
    if score >= 80:
        band = "starke Indizien für KI-Erzeugung"
    elif score >= 62:
        band = "überwiegend Indizien für KI-Erzeugung oder starke KI-Überarbeitung"
    elif score >= 45:
        band = "gemischte Indizien — keine belastbare Zuordnung"
    elif score >= 25:
        band = "überwiegend Indizien für menschliches Schreiben"
    else:
        band = "starke Indizien für menschliches Schreiben"
    return {
        "indizienwert": score,
        "punktesumme": summe,
        "punktesumme_ungedaempft": rohsumme,
        "laengendaempfung": round(daempfung, 2),
        "einordnung": band,
        "verlaesslichkeit_nach_textlaenge": verlaesslichkeit,
        "hinweis": ("Der Indizienwert ist keine Wahrscheinlichkeit. Er fasst nur "
                    "zusammen, wie viele der gemessenen Stilmerkmale in welche "
                    "Richtung zeigen. Fachtexte, Behördendeutsch, Übersetzungen "
                    "und lektorierte Texte erzeugen dieselben Muster wie KI-Texte."),
    }


# --------------------------------------------------------------------------
# Ausgabe
# --------------------------------------------------------------------------

def klartext(erg):
    z = erg["zusammenfassung"]
    aus = []
    aus.append("=" * 68)
    aus.append("STILANALYSE — MESSWERTE UND INDIZIEN")
    aus.append("=" * 68)
    aus.append(f"Textumfang: {erg['lexik'].get('woerter', 0)} Wörter, "
               f"{erg['rhythmus'].get('saetze', 0)} Sätze, "
               f"{erg['absaetze'].get('absaetze', 0)} Absätze")
    aus.append(f"Indizienwert: {z['indizienwert']}/100  ({z['punktesumme']:+d} Punkte)")
    aus.append(f"Einordnung:   {z['einordnung']}")
    aus.append(f"Verlässlichkeit nach Textlänge: {z['verlaesslichkeit_nach_textlaenge']}")
    aus.append("")
    ki = [i for i in erg["indizien"] if i["punkte"] > 0]
    me = [i for i in erg["indizien"] if i["punkte"] < 0]
    aus.append(f"--- Indizien Richtung KI ({len(ki)}) " + "-" * 30)
    for i in sorted(ki, key=lambda x: -x["punkte"]):
        aus.append(f"  [+{i['punkte']:>2}] {i['indiz']}")
        aus.append(f"         {i['befund']}")
    if not ki:
        aus.append("  keine")
    aus.append("")
    aus.append(f"--- Indizien Richtung Mensch ({len(me)}) " + "-" * 26)
    for i in sorted(me, key=lambda x: x["punkte"]):
        aus.append(f"  [{i['punkte']:>3}] {i['indiz']}")
        aus.append(f"         {i['befund']}")
    if not me:
        aus.append("  keine")
    aus.append("")
    aus.append("--- Rohwerte " + "-" * 54)
    for block in ("rhythmus", "absaetze", "lexik", "typografie",
                  "phrasen", "menschsignale"):
        aus.append(f"[{block}]")
        for k, v in erg[block].items():
            aus.append(f"  {k}: {v}")
    aus.append("")
    aus.append(z["hinweis"])
    return "\n".join(aus)


def main():
    ap = argparse.ArgumentParser(description="Stilsignale eines deutschen Textes messen.")
    ap.add_argument("datei", help="Textdatei (UTF-8) oder '-' für stdin")
    ap.add_argument("--json", metavar="PFAD", help="Rohbefund als JSON speichern")
    ap.add_argument("--nur-json", action="store_true", help="nur JSON auf stdout")
    args = ap.parse_args()

    if args.datei == "-":
        text = sys.stdin.read()
    else:
        with open(args.datei, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

    if len(woerter(text)) < 20:
        print("Text zu kurz für eine sinnvolle Messung (unter 20 Wörter).",
              file=sys.stderr)
        sys.exit(2)

    saetze = satz_split(text)
    r = mess_rhythmus(saetze)
    a = mess_absaetze(text)
    l = mess_lexik(text)
    t = mess_typografie(text)
    p = mess_phrasen(text)
    h = mess_menschsignale(text)
    ind = bewerte(r, a, l, t, p, h)

    erg = {
        "rhythmus": r, "absaetze": a, "lexik": l, "typografie": t,
        "phrasen": p, "menschsignale": h, "indizien": ind,
        "zusammenfassung": score_und_band(ind, l.get("woerter", 0)),
    }

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(erg, f, ensure_ascii=False, indent=2)
    if args.nur_json:
        print(json.dumps(erg, ensure_ascii=False, indent=2))
    else:
        print(klartext(erg))


if __name__ == "__main__":
    main()
