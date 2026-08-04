---
name: ki-text-umschreiben
description: Überarbeitet einen deutschen Text, der maschinell klingt, in eine Fassung mit menschlichem Rhythmus, echter Konkretheit und ohne LLM-Floskeln — gezielt gegen die Befunde aus ki-text-check, ohne Fakten zu erfinden. Nutze diesen Skill immer, wenn jemand sagt "schreib das menschlicher", "das klingt nach ChatGPT, überarbeite es", "mach den Text natürlicher", "entschärfe den Text", "weniger KI-Sprech", "kann man das umformulieren dass es nicht nach KI klingt", oder wenn ki-text-check einen Indizienwert ab 62 gemeldet hat und der Verfasser den Text selbst überarbeiten will. Auch triggern, wenn jemand einen eigenen Entwurf zeigt und nur beiläufig sagt, er klinge glattgebügelt oder gestelzt.
---

# KI-Text umschreiben (Deutsch)

Gegenstück zu `ki-text-check`. Der Prüf-Skill sagt, *was* maschinell wirkt und
*wo*. Dieser Skill macht daraus eine überarbeitete Fassung.

Wichtig für das Selbstverständnis: Die Eingriffe, die einen Text weniger
maschinell wirken lassen, sind fast deckungsgleich mit denen, die ihn besser
machen — konkreter, kürzer, mit einer erkennbaren Haltung. Das ist Lektorat,
kein Trick. Behandle die Aufgabe entsprechend: Ziel ist ein besserer Text,
der niedrigere Indizienwert ist die Folge, nicht der Zweck.

## Wann dieser Skill dran ist

**Ab Indizienwert 62** (Band „überwiegend Indizien für KI-Erzeugung") bietet
`ki-text-check` die Überarbeitung von sich aus an. Darunter nur, wenn der
Nutzer ausdrücklich danach fragt — einen Text umzuschreiben, der bei 50 liegt,
ist Arbeit ohne Ertrag und macht ihn oft schlechter.

**Voraussetzung: Es ist der eigene Text des Nutzers**, oder er hat das Recht,
ihn zu bearbeiten. Wenn erkennbar ein fremder Text umgeschrieben werden soll,
um eine Vorgabe zu unterlaufen, die eigene Autorschaft verlangt — eine
Prüfungsleistung, eine Bewerbung, eine Offenlegungspflicht — dann sag das
einmal klar und knapp: Umschreiben löst dieses Problem nicht, es verschiebt
es nur. Danach nicht weiter moralisieren. Bei allen anderen Fällen — eigene
Marketingtexte, Seminarunterlagen, Angebote, Blogbeiträge, Berichte — ist das
schlicht Textarbeit.

## Ablauf

### 1. Befund holen

Wenn `ki-text-check` gerade gelaufen ist, den Befund übernehmen (Indizienwert,
Liste der Indizien, Fundstellen). Wenn nicht, erst messen:

```bash
python3 <ki-text-check>/scripts/analyse.py text.txt --json befund.json
```

Ohne Befund nicht anfangen. Blind alle Eingriffe anzuwenden macht den Text
schlechter — die Hälfte davon trifft auf einen konkreten Text gar nicht zu.

### 2. Kontext klären, wenn er fehlt

Zwei Dinge musst du wissen, sonst wird die Fassung unbrauchbar:

- **Textsorte und Empfänger.** Ein Angebot an einen Geschäftsführer verträgt
  keine Modalpartikeln, ein Blogbeitrag schon. Der Eingriffskatalog gilt
  nicht überall gleich.
- **Was darf sich ändern?** Nur Sprache, oder auch Reihenfolge, Länge und
  Schwerpunkte? Frag das, wenn es nicht offensichtlich ist — aber in einem
  Satz, nicht als Fragebogen.

### 3. Gezielt eingreifen

Arbeite die Indizien aus dem Befund ab, nicht den Katalog. Details und
Vorher/Nachher-Beispiele in `references/eingriffe.md`. Nach Wirkung sortiert:

| Rang | Eingriff | Greift bei |
|---|---|---|
| 1 | **Rhythmus brechen** — zwei bis drei Sätze auf unter fünf Wörter, einen auf über dreißig | Variationskoeffizient, ±25%-Korridor, „kein kurzer Satz" |
| 2 | **Konkret werden** — Zahl, Datum, Name, Betrag statt allgemeiner Aussage | „Kaum überprüfbare Details" |
| 3 | **Floskeln streichen statt ersetzen** — „Es ist wichtig zu betonen, dass X" wird zu „X" | KI-Phrasen-Treffer |
| 4 | **Eine Haltung einbauen** — etwas, das nicht jeder unterschreiben würde | symmetrische Abwägung (aus dem Lesen) |
| 5 | **Konnektoren halbieren** — jedes zweite „darüber hinaus", „zudem", „folglich" ersatzlos weg | Konnektoren-Überschuss |
| 6 | **Nominalstil auflösen** — „die Durchführung der Schulung erfolgt" wird zu „wir schulen" | Nominalisierungsdichte, Langkomposita |
| 7 | **Etwas weglassen** — nicht alle Teilaspekte abdecken | „Vollständigkeit ohne Schwerpunkt" |
| 8 | **Typografie angleichen** — — zu – oder Komma, … zu drei Punkten, geschützte Leerzeichen raus | Geviertstrich, unsichtbare Sonderzeichen |
| 9 | **Listen auflösen** — `- **Begriff**: Erklärung` zu Fließtext, wo es passt | Listen-Muster, Markdown-Dichte |

### 4. Fehlende Konkretheit sichtbar machen — nichts erfinden

Der zweitstärkste Eingriff braucht Wissen, das du nicht hast. **Erfinde keine
Zahlen, Namen, Daten, Beträge oder Beispiele.** Bei einem Angebot oder einer
Seminarunterlage stehen sonst falsche Angaben im Umlauf, die der Verfasser
selbst nicht mehr als erfunden erkennt — das ist ein größerer Schaden als ein
hoher Indizienwert.

Stattdessen: Platzhalter setzen, dort wo ein echtes Detail den größten Effekt
hätte, und am Ende als Rückfrageliste bündeln.

```
Format:  [ZAHL: wie viele Teilnehmer?]  [DATUM: wann war das?]
         [NAME: welcher Kunde?]  [BETRAG: was hat es gekostet?]
         [BEISPIEL: welcher konkrete Fall?]
```

Setz höchstens fünf bis sieben davon — sonst kippt die Fassung von „fast
fertig" zu „Hausaufgabe". Wähle die Stellen, an denen ein Detail wirklich
trägt, nicht jede Stelle, an der eines denkbar wäre.

### 5. Nicht überkorrigieren

**Zielband ist 30–50, nicht 0.** Ein Text bei 5 liest sich, als hätte sich
jemand Mühe gegeben, ungeschliffen zu wirken — Modalpartikeln in jedem Satz,
gewollte Fragmente, aufgesetzte Lockerheit. Das ist auf andere Weise genauso
auffällig und obendrein unangenehm zu lesen.

Konkrete Grenzen:

- Modalpartikeln höchstens etwa eine pro 100 Wörter, in förmlichen Texten
  gar keine.
- Keine absichtlichen Tippfehler. Nie. Das ist der einzige Eingriff, der
  reine Täuschung ist und keinen Textnutzen hat.
- Register halten. Ein Angebot bleibt ein Angebot. Wenn die neue Fassung
  plötzlich lockerer klingt als alles andere, was der Verfasser schreibt,
  ist sie unbrauchbar.
- Fachbegriffe bleiben. „Nominalstil auflösen" heißt nicht, Fachsprache
  durch Umgangssprache zu ersetzen.

### 6. Neu messen

```bash
python3 <dieser-skill>/scripts/vergleich.py original.txt neu.txt
```

Das Skript findet `analyse.py` selbst, wenn `ki-text-check` installiert ist,
sonst `--analyse <pfad>` mitgeben. Es zeigt Indizienwert vorher/nachher, die
Kennzahlen im Vergleich, welche Indizien behoben und welche noch offen sind —
und prüft, ob beim Umschreiben Substanz verlorengegangen ist.

**Die Inhaltsprüfung ernst nehmen.** Wenn sie meldet, dass unter 60 % der
Inhaltswörter überlebt haben oder der Text 30 % kürzer wurde, ist das kein
Erfolg, sondern ein Hinweis auf verlorene Aussagen. Dann nachbessern, nicht
abliefern.

Wenn der Wert nach der Überarbeitung noch über 62 liegt: die Liste „noch
offen" durchgehen und einen zweiten Durchgang machen. Höchstens zwei — danach
ist der begrenzende Faktor fehlende Konkretheit, und die kann nur der
Verfasser liefern.

### 7. Ausgeben

**Als Datei** im Arbeitsordner: die überarbeitete Fassung, Dateiname mit
Zusatz `-ueberarbeitet`. Mit `present_files` ausliefern.

**Im Chat**, knapp:

1. Indizienwert vorher → nachher in einem Satz.
2. Die vier bis sechs wichtigsten Eingriffe als Vorher/Nachher-Paare. Nicht
   alle aufzählen — die, an denen der Verfasser das Muster erkennt und beim
   nächsten Text selbst anwenden kann.
3. Die Rückfrageliste zu den Platzhaltern, als Fragen formuliert.
4. Was noch offen ist und warum.

Kein Fließtext-Bericht, keine Wiederholung des kompletten Textes im Chat —
der steht in der Datei.

## Referenzdateien

- `references/eingriffe.md` — Eingriffskatalog mit deutschen
  Vorher/Nachher-Beispielen, Textsorten-Ausnahmen, typische Fehlgriffe
- `scripts/vergleich.py` — misst beide Fassungen, stellt sie gegenüber,
  prüft auf Substanzverlust

Setzt `ki-text-check` voraus (für `analyse.py`).
