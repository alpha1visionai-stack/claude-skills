---
name: ki-text-check
description: Prüft einen deutschen Text darauf, ob er von einer KI (ChatGPT, Claude, Gemini) geschrieben wurde oder von einem Menschen — mit nachvollziehbaren Belegen statt Blackbox-Prozentzahl. Läuft vollständig offline, der Text verlässt das System nicht. Nutze diesen Skill immer, wenn jemand fragt "ist das KI-generiert", "hat das eine KI geschrieben", "klingt das nach ChatGPT", "prüf mal ob das echt ist", "KI-Detektor", "ZeroGPT", "AI Detector", einen fremden Text zur Echtheitsprüfung vorlegt (Bewerbung, Seminararbeit, Blogtext, Angebot, E-Mail, Rezension), oder wissen will wie KI-typisch sein eigener Entwurf klingt. Auch triggern, wenn nur beiläufig Zweifel an der Autorschaft eines Textes geäußert werden.
---

# KI-Text-Check (Deutsch)

Beurteilt, ob ein deutscher Text maschinell erzeugt wirkt. Das Ergebnis ist
ein **Indizienbild mit Fundstellen**, keine Wahrscheinlichkeit.

Warum überhaupt so und nicht wie ZeroGPT & Co.: Öffentliche Detektoren geben
eine Prozentzahl ohne Begründung aus, sind nicht kalibriert und benachteiligen
systematisch Nicht-Muttersprachler und Fachtexte. Eine Zahl, die niemand
prüfen kann, ist für eine Entscheidung unbrauchbar. Ein Befund mit Belegen
ist es. Deshalb hier: messen, zitieren, begründen — und offenlegen, was
dagegen spricht.

## Ablauf

### 1. Text besorgen und Zweck klären

Der Text kann als Datei kommen (.txt, .md, .docx, .pdf) oder direkt im Chat.
Bei Chat-Text: in eine UTF-8-Datei im Arbeitsordner schreiben, damit das
Skript darauf laufen kann. **Beim Zwischenspeichern nichts normalisieren** —
Geviertstriche, geschützte Leerzeichen, doppelte Leerzeichen und
Tippfehler sind Messmaterial. Beim Extrahieren aus PDF/DOCX gehen typografische
Signale teils verloren; das im Befund erwähnen.

Frag nach dem Zweck, wenn er nicht klar ist — aber nur einmal und kurz.
Der Zweck ändert die Bewertung:

- **Eigener Entwurf soll weniger KI-haft klingen** → Fokus auf konkrete
  Umschreibvorschläge, Score nebensächlich.
- **Fremder Text, reine Neugier** → normaler Befund.
- **Entscheidung über eine Person** (Bewerbung, Prüfungsleistung,
  Vertragsstreit, Kündigung) → Befund plus ausdrücklicher Hinweis auf die
  Grenzen und auf belastbarere Wege. Siehe Abschnitt 5.

### 2. Messen

Wenn `scripts/analyse.py` im Skill-Ordner liegt, ausführen:

```bash
python3 <skill>/scripts/analyse.py <textdatei>
python3 <skill>/scripts/analyse.py <textdatei> --json befund.json
```

Das Skript braucht nur die Python-Standardbibliothek, läuft offline und gibt
Messwerte, gewichtete Indizien mit Fundstellen und einen Indizienwert 0–100
aus. Details zu den Gewichtungen: `references/bewertung.md`.

Liegt das Skript nicht vor, die Messwerte mit einem eigenen kurzen
Python-Schnipsel erheben — mindestens: Variationskoeffizient der Satzlängen,
Konnektorendichte, Modalpartikeldichte, Geviertstriche, Nominalisierungen,
Konkretheitsdichte. Die Schwellen stehen unten in der Kurzrubrik.

### 3. Lesen — nicht überspringen

Die aussagekräftigsten Signale kann kein Skript zählen. Lies den Text und
prüfe gezielt:

- **Symmetrische Abwägung.** Bekommt jeder Vorteil einen etwa gleich langen
  Nachteil? Stößt der Text am Ende niemanden vor den Kopf?
- **Vollständigkeit ohne Schwerpunkt.** Gleichmäßig abgedeckt statt an einem
  Lieblingsdetail festgebissen?
- **Beispiele ohne Herkunft.** „Ein Unternehmen aus der Fertigungsbranche
  konnte die Effizienz deutlich steigern" — keine Firma, kein Jahr, keine Zahl.
- **Keine Kosten.** Fehlt jede gescheiterte Sache, jeder Preis, jeder Ärger?
  Echte Erfahrung hinterlässt Spuren.
- **Perfekt parallele Gliederung.** Drei Punkte, alle gleich tief, alle gleich lang.
- **Keine Abschweifung.** Menschen verlassen das Thema und kommen zurück.
- **Registerbrüche.** Wechsel zwischen sehr formell und sehr locker ohne
  Grund deutet auf Zusammenkleben aus mehreren Quellen — Mensch *und* KI.
- **Souverän formulierte Sachfehler.** Erfundene Normnummern, falsch
  zitierte Paragrafen, plausible aber falsche Zahlen. Wenn es die Sache
  hergibt: eine oder zwei Angaben stichprobenartig prüfen.

Ausführlich in `references/marker-deutsch.md`.

### 4. Fehlalarm-Textsorten prüfen

Diese Textsorten sehen von Natur aus wie KI-Text. Trifft eine zu, die
Einordnung nach unten korrigieren und den Grund im Befund nennen:

Behörden- und Rechtstexte · Fachtexte und Normen · Übersetzungen ·
lektorierte oder redigierte Texte · **Texte von Nicht-Muttersprachlern** ·
Schablonentexte (Angebote, Serienbriefe, Stellenanzeigen) · Texte unter
200 Wörtern.

Der Fall Nicht-Muttersprachler ist der wichtigste: weniger Modalpartikeln,
einfacherer und gleichmäßigerer Satzbau, vorsichtigerer Wortschatz — genau
das gemessene Profil. Dieser Fehlalarm trifft ausgerechnet die Leute, die
sich am meisten Mühe geben. Wenn es Hinweise darauf gibt, sag es deutlich.

### 5. Befund ausgeben

**In den Chat** (kurz, ohne Bericht-Formatierung):

- Indizienwert und Einordnung in einem Satz
- die 3–4 stärksten Belege, jeweils mit Zitat oder Messwert
- was dagegen spricht
- bei Werten zwischen 45 und 61: klar sagen, dass keine Zuordnung möglich ist

**Zusätzlich als Markdown-Datei** im Arbeitsordner, nach der Struktur in
`references/bericht-vorlage.md`, und mit `present_files` ausliefern.

Formulierungsregeln:

- „78 von 100 Indizienpunkten" ist zulässig. „78 % KI-Wahrscheinlichkeit"
  nicht — der Wert ist keine Wahrscheinlichkeit und stammt nicht aus einem
  kalibrierten Modell.
- Jede Behauptung mit Beleg. Ein Befund ohne Fundstellen ist nicht prüfbar
  und damit wertlos.
- Gegenevidenz immer nennen, auch bei klarem Bild.
- „Gemischte Indizien" ist ein vollständiges Ergebnis, kein Ausweichen.
  Mischtexte (Mensch schreibt, KI glättet — oder umgekehrt) sind der
  Normalfall und erzeugen genau solche Werte.
- Nicht dramatisieren. Kein „entlarvt", „eindeutig", „zweifelsfrei".

**Wenn eine Entscheidung über eine Person davon abhängt**, gehört das in den
Befund:

> Dieser Befund ist ein Stilgutachten, kein Nachweis von Autorschaft. Er ist
> nicht geeignet, allein eine Entscheidung über eine Person zu begründen.
> Belastbarer sind Dateimetadaten (Bearbeitungszeit, Autorenfeld),
> Versionsverlauf, Zwischenstände — und ein Gespräch mit dem Verfasser über
> seine Formulierungsentscheidungen.

Weise in solchen Fällen aktiv auf diese Wege hin. Ein falsch beschuldigter
Mensch ist ein realer Schaden, und Stildetektoren haben bekannte Fehlerquoten.

### 6. Ab Indizienwert 62: Überarbeitung anbieten

Liegt der Wert im Band „überwiegend Indizien für KI-Erzeugung" (62) oder
darüber **und** ist es der eigene Text des Nutzers, biete am Ende des Befunds
in einem Satz an, ihn zu überarbeiten — und übernimm bei Zustimmung den Skill
`ki-text-umschreiben`. Übergib ihm den Pfad zur Textdatei und den Befund
(`--json`), damit er gezielt gegen die gefundenen Indizien arbeitet statt
blind alle Eingriffe anzuwenden.

Unter 62 nicht von selbst anbieten. Einen Text umzuschreiben, der bei 50
liegt, ist Arbeit ohne Ertrag und macht ihn oft schlechter.

Bei fremden Texten ist die Überarbeitung nicht das Thema — dort geht es um
die Beurteilung. Nur anbieten, wenn der Nutzer ausdrücklich danach fragt und
erkennbar berechtigt ist, den Text zu bearbeiten.

Ist `ki-text-umschreiben` nicht installiert, gib stattdessen die
Eingriffsliste aus dem Abschnitt weiter unten aus.

## Kurzrubrik (falls das Skript nicht verfügbar ist)

Startwert 50. Punkte addieren, auf 0–100 klammern. Bei Texten unter
400 Wörtern die Summe mit `Wörter/400` dämpfen (Untergrenze Faktor 0,45).

**Richtung KI:** Satzlängen-Variationskoeffizient < 0,30 (+13) oder < 0,42
(+7) · über 60 % der Sätze im ±25 %-Korridor um den Mittelwert (+8) ·
Absatzlängen fast identisch bei ≥ 5 Absätzen (+8) · Geviertstrich — dreimal
oder öfter (+11), einmal (+6) · geschütztes Leerzeichen oder Zero-Width-Zeichen
(+6) · Listen im Muster `- **Begriff**: Erklärung` (+9) · Konnektoren
(„darüber hinaus", „zudem", „ferner", „des Weiteren", „folglich", „somit",
„insbesondere") über 2,2 pro 100 Wörter (+9) · KI-Floskeln wie „Es ist wichtig
zu betonen", „In der heutigen schnelllebigen Welt", „spielt eine entscheidende
Rolle", „Zusammenfassend lässt sich sagen", „nicht nur X, sondern auch Y"
(+5 je Muster, max +24) · sechs oder mehr verschiedene LLM-Vokabeln
(ganzheitlich, nachhaltig, innovativ, maßgeschneidert, nahtlos, robust,
wegweisend, Mehrwert, Potenzial) (bis +12) · Nominalisierungen auf
-ung/-heit/-keit/-ierung über 7 pro 100 Wörter (+6) · null Tippunsauberkeiten
ab 300 Wörtern (+6) · keine Modalpartikeln ab 150 Wörtern (+5) · fast keine
Zahlen, Daten, Namen, Beträge (+4).

**Richtung Mensch:** Modalpartikeln (halt, eigentlich, irgendwie, naja, tja,
wobei, quasi, ziemlich, echt, sowieso) über 1,2 pro 100 Wörter (−12) oder über
0,5 (−7) · drei oder mehr Tippunsauberkeiten, Wortdoppler, fehlende
Leerzeichen, „!!" (−11), eine (−6) · Satzlängen-Variationskoeffizient > 0,85
(−9) oder > 0,68 (−5) · drei oder mehr umgangssprachliche Formen (−8) · mehrere
Sätze unter 5 Wörtern (−6) · Ich-Perspektive über 1,5 pro 100 Wörter (−6) ·
Zahlen/Daten/Beträge/URLs über 1,5 pro 100 Wörter (−6) · gemischte
Anführungszeichen-Stile (−5) · kaum Nominalstil, unter 1,5 pro 100 Wörter (−4).

**Bänder:** 80–100 starke KI-Indizien · 62–79 überwiegend KI-Indizien oder
starke KI-Überarbeitung · 45–61 gemischt, keine Zuordnung · 25–44 überwiegend
menschlich · 0–24 stark menschlich.

## Wenn der Nutzer seinen eigenen Text entschärfen will

Dafür gibt es den Skill `ki-text-umschreiben` — er arbeitet gezielt gegen die
Indizien aus diesem Befund, setzt Platzhalter statt erfundener Details und
misst das Ergebnis neu. Übernimm ihn, wenn er installiert ist.

Ohne diesen Skill: Der Score ist dann Nebensache, liefere stattdessen
konkrete Eingriffe, nach Wirkung sortiert:

1. **Rhythmus brechen.** Zwei bis drei Sätze auf unter fünf Wörter kürzen,
   einen auf über dreißig verlängern. Das ist der wirksamste Einzelgriff.
2. **Konkret werden.** Jede allgemeine Aussage durch eine mit Zahl, Datum,
   Name oder Betrag ersetzen. Wo das nicht geht, die Aussage streichen —
   sie trug ohnehin nichts.
3. **Floskeln streichen statt ersetzen.** „Es ist wichtig zu betonen, dass X"
   wird zu „X". Der Satz verliert nichts.
4. **Eine Meinung einbauen.** Etwas, das nicht jeder unterschreiben würde.
   Symmetrische Abwägung ist das deutlichste Merkmal maschineller Texte.
5. **Konnektoren halbieren.** Jedes zweite „darüber hinaus", „zudem",
   „folglich" ersatzlos weg. Die Sätze stehen auch ohne.
6. **Typografie angleichen.** — durch – oder Komma ersetzen, … durch drei
   Punkte, geschützte Leerzeichen entfernen.
7. **Etwas weglassen.** Nicht alle Teilaspekte abdecken. Menschen sind
   unfair verteilt.

Sag dazu offen: Diese Eingriffe machen den Text meistens besser, nicht nur
unauffälliger. Wenn es allerdings darum geht, eine Prüfungs- oder
Bewerbungsvorgabe zu unterlaufen, die eigene Autorschaft verlangt, dann löst
Umschreiben das Problem nicht — es verschiebt es nur.

## Referenzdateien

- `references/marker-deutsch.md` — warum die Signale funktionieren, was nur
  beim Lesen auffällt, Fehlalarme, Evidenz außerhalb des Textes
- `references/bewertung.md` — vollständige Gewichtungstabelle, Bänder,
  Regeln für die Befundformulierung
- `references/bericht-vorlage.md` — Struktur der Markdown-Datei
- `scripts/analyse.py` — Messskript, nur Standardbibliothek, offline
