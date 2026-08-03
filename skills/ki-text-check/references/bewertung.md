# Bewertung und Befundformulierung

## Gewichtungen im Skript

Das Skript summiert gewichtete Indizien. Positive Punkte zeigen Richtung KI,
negative Richtung Mensch. Startwert 50, geklammert auf 0–100.

### Richtung KI

| Punkte | Indiz | Schwelle |
|---|---|---|
| +24 (max) | KI-typische Formulierungsmuster | 5 pro Treffer, gedeckelt |
| +13 | Satzlängen fast gleichförmig | Variationskoeffizient < 0,30 |
| +11 | Häufiger Geviertstrich (—) | ≥ 3 Vorkommen |
| +12 (max) | LLM-Lieblingsvokabeln | ≥ 6 verschiedene |
| +9 | Konnektoren-Überschuss | > 2,2 pro 100 Wörter |
| +9 | Listen „**Begriff**: Erklärung" | ≥ 2 Vorkommen |
| +8 | Satzlängen im engen Korridor | > 60 % im ±25 %-Band |
| +8 | Absätze gleich lang | Absatz-CV < 0,15, ≥ 5 Absätze |
| +7 | Satzlängen auffällig gleichmäßig | CV < 0,42 |
| +6 | Ausgeprägter Nominalstil | > 7 pro 100 Wörter |
| +6 | Unsichtbare Sonderzeichen | NBSP / Zero-Width vorhanden |
| +6 | Keine einzige Tippunsauberkeit | ab 300 Wörter |
| +6 | Wiederkehrende Satzanfänge | Diversität < 0,55 |
| +5 | Wortschatzdichte konstant | MATTR-Streuung < 0,035 |
| +5 | Keine Modalpartikeln | ab 150 Wörter |
| +5 | Häufige Dreierketten | ≥ 15 % der Sätze |
| +4 | Viele Langkomposita | > 9 % über 12 Zeichen |
| +4 | Kaum überprüfbare Details | < 0,3 pro 100 Wörter |
| +4 | Kein einziger kurzer Satz | ab 15 Sätzen |
| +4 | Hohe Doppelpunktdichte | ≥ 0,3 pro Satz |
| +3 | Auslassungszeichen … | statt drei Punkten |
| +3 | Keine Ausrufe-/Fragezeichen | ab 20 Sätzen |

### Richtung Mensch

| Punkte | Indiz | Schwelle |
|---|---|---|
| −12 | Viele Modalpartikeln | > 1,2 pro 100 Wörter |
| −11 | Mehrere Tippunsauberkeiten | ≥ 3 Fundstellen |
| −9 | Satzlängen stark schwankend | CV > 0,85 |
| −8 | Umgangssprachliche Formen | ≥ 3 Varianten |
| −7 | Modalpartikeln vorhanden | > 0,5 pro 100 Wörter |
| −6 | Sehr kurze Sätze / Fragmente | ≥ 12 % der Sätze |
| −6 | Deutliche Ich-Perspektive | > 1,5 pro 100 Wörter |
| −6 | Hohe Konkretheit | > 1,5 pro 100 Wörter |
| −6 | Tippunsauberkeit vorhanden | ≥ 1 Fundstelle |
| −5 | Gemischte Anführungsstile | ≥ 2 Stile |
| −5 | Satzlängen natürlich schwankend | CV > 0,68 |
| −4 | Kaum Nominalstil | < 1,5 pro 100 Wörter |
| −4 | Absätze ungleich lang | Absatz-CV > 0,70 |
| −3 | Vielfältige Satzanfänge | Diversität > 0,88, ab 20 Sätzen |

### Längendämpfung

Die Punktesumme wird mit `min(1,0; max(0,45; Wörter/400))` multipliziert.
Ein 170-Wort-Text kann also nur etwa die Hälfte des Ausschlags erreichen.
Das ist beabsichtigt: kurze Texte tragen keine starken Aussagen.

### Bänder

| Wert | Einordnung |
|---|---|
| 80–100 | starke Indizien für KI-Erzeugung |
| 62–79 | überwiegend Indizien für KI-Erzeugung oder starke KI-Überarbeitung |
| 45–61 | gemischte Indizien — keine belastbare Zuordnung |
| 25–44 | überwiegend Indizien für menschliches Schreiben |
| 0–24 | starke Indizien für menschliches Schreiben |

---

## Der Score ist nicht das Urteil

Die Zahl ist ein Einstieg, kein Ergebnis. Nach dem Skriptlauf gilt:

1. **Lies den Text.** Prüfe die Punkte aus `marker-deutsch.md`, Abschnitt 3
   — Symmetrie, fehlende Konkretheit, folgenlose Beispiele, Abwesenheit von
   Einsatz. Diese Beobachtungen wiegen oft schwerer als die Messwerte.
2. **Prüfe auf Fehlalarm-Textsorten.** Behördendeutsch, Fachtext,
   Übersetzung, Nicht-Muttersprachler, lektoriert, Schablone. Wenn eine
   zutrifft, korrigiere die Einordnung nach unten und schreib den Grund hin.
3. **Korrigiere die Einordnung ausdrücklich**, wenn Lesen und Messen
   auseinandergehen. Schreib beides in den Befund, nicht nur das Ergebnis.

---

## Regeln für die Formulierung

**Keine Scheingenauigkeit.** „78 von 100 Indizienpunkten" ist zulässig,
„78 % KI-Wahrscheinlichkeit" nicht. Der Wert ist keine Wahrscheinlichkeit
und beruht nicht auf einem kalibrierten Modell.

**Immer Belege.** Jede Behauptung mit Zitat oder Messwert. Ein Befund ohne
Fundstellen ist wertlos, weil er nicht überprüfbar ist.

**Gegenevidenz nennen.** Auch bei klarem Bild: was spricht dagegen?
Ein Befund, der nur in eine Richtung argumentiert, ist unbrauchbar.

**Bei Unklarheit unklar bleiben.** „Gemischte Indizien" ist ein
vollständiges, professionelles Ergebnis. Ein Münzwurf ist es nicht.

**Konsequenzen ernst nehmen.** Wenn erkennbar eine Entscheidung über eine
Person davon abhängt — Bewerbung, Prüfungsleistung, Kündigung,
Vertragsstreit — dann gehört in den Befund:

> Dieser Befund ist ein Stilgutachten, kein Nachweis von Autorschaft. Er
> ist nicht geeignet, allein eine Entscheidung über eine Person zu
> begründen. Belastbarer sind Dateimetadaten, Versionsverlauf und ein
> Gespräch mit dem Verfasser.

Frag in solchen Fällen nach, was der Nutzer mit dem Ergebnis vorhat, und
weise auf die belastbareren Wege hin. Das ist keine Zurückhaltung aus
Prinzipienreiterei — Stildetektoren haben bekannte Fehlerquoten,
insbesondere gegenüber Nicht-Muttersprachlern, und ein falsch beschuldigter
Mensch ist ein realer Schaden.

**Nicht überreden.** Wenn der Nutzer eine andere Einschätzung hat, sag was
du siehst und warum, aber verteidige die Zahl nicht gegen sein Wissen über
den Kontext. Er kennt den Autor, du kennst nur den Text.
