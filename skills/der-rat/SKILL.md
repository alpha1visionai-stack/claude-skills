---
name: der-rat
description: "Schickt jede Frage, Idee oder Entscheidung durch einen Rat aus 5 KI-Beratern, die unabhängig analysieren, sich gegenseitig kontrollieren und am Ende ein klares Urteil fällen. PFLICHT-TRIGGER: 'rat', 'rat das', 'rat das durch', 'frag den rat', 'ab in den rat', 'der rat soll ran', 'gremium', 'gremium das', 'ab ins gremium', 'frag das gremium'. STARKE TRIGGER (nur bei echter Entscheidung mit Tradeoff): 'soll ich X oder Y', 'welche option', 'was würdest du an meiner stelle tun', 'ist das der richtige move', 'ich kann mich nicht entscheiden', 'ich bin hin- und hergerissen', 'gib mir mehrere perspektiven', 'pressure-test das'. NICHT triggern bei einfachen Ja/Nein-Fragen, Faktenfragen ('wann war X'), reinen Schreibaufgaben oder belanglosem 'soll ich' ohne echten Tradeoff (z.B. 'soll ich Markdown nehmen' ist keine Rats-Frage). Triggern wenn eine echte Entscheidung mit Einsatz, mehreren Optionen und Kontext vorliegt, die aus mehreren Blickwinkeln druckgetestet werden soll."
---

# Der Rat

Du fragst eine KI, du kriegst eine Antwort. Die kann stark sein, kann auch mittelmäßig sein – du merkst den Unterschied nicht, weil du nur eine Perspektive gesehen hast.

Der Rat löst das. Deine Frage läuft durch 5 unabhängige Berater, jeder denkt aus einem komplett anderen Winkel. Danach treten sie einen Schritt zurück und prüfen sich gegenseitig. Am Ende fasst ein Vorsitzender alles zu einem klaren Urteil zusammen: wo sich der Rat einig ist, wo er streitet, was er fast übersehen hätte – und was du konkret tun solltest.

Adaptiert von Andrej Karpathys „LLM Council". Im Original feuern mehrere Modelle parallel, prüfen sich anonym und ein Vorsitzender synthetisiert. Hier passiert das in einem Durchgang im Claude Chat: fünf **Denkweisen** statt fünf Modellen.

---

## Wann der Rat tagt

Der Rat ist für Fragen, bei denen Falschliegen teuer ist.

Gute Rats-Fragen:
- „Soll ich einen 97-€-Workshop oder einen 497-€-Kurs launchen?"
- „Welcher von diesen drei Positionierungs-Winkeln ist am stärksten?"
- „Ich überlege von X auf Y zu pivotieren. Bin ich bescheuert?"
- „Hier ist meine Landingpage-Copy. Wo ist sie schwach?"
- „VA einstellen oder erst die Automatisierung bauen?"

Schlechte Rats-Fragen:
- „Was ist die Hauptstadt von Frankreich?" (eine richtige Antwort, keine Perspektiven nötig)
- „Schreib mir einen Tweet" (Kreativ-Aufgabe, keine Entscheidung)
- „Fass diesen Artikel zusammen" (Verarbeitung, kein Urteil)

Der Rat glänzt, wenn echte Unsicherheit da ist und eine falsche Entscheidung wehtut. Wenn du die Antwort längst kennst und nur Bestätigung willst, wird der Rat dir vermutlich Dinge sagen, die du nicht hören willst. Genau dafür ist er da.

---

## Die fünf Berater

Jeder Berater denkt aus einem anderen Winkel. Das sind keine Job-Titel oder Personas, sondern Denkweisen, die von Natur aus gegeneinander arbeiten.

### 1. Der Skeptiker
Sucht aktiv nach dem, was nicht funktioniert, was fehlt, was scheitern wird. Geht davon aus, dass die Idee einen fatalen Fehler hat, und versucht ihn zu finden. Sieht alles solide aus, gräbt er tiefer. Kein Pessimist – eher der Freund, der dich vor einem schlechten Deal bewahrt, indem er die Fragen stellt, die du vermeidest.

### 2. Der Grundsatz-Denker
Ignoriert die Oberflächen-Frage und fragt: „Was wollen wir hier eigentlich lösen?" Streicht Annahmen weg, baut das Problem von Grund auf neu zusammen. Manchmal ist sein wertvollster Beitrag der Satz: „Du stellst die komplett falsche Frage."

### 3. Der Visionär
Sucht das Upside, das alle anderen übersehen. Was könnte größer sein? Welche angrenzende Chance liegt versteckt? Was wird unterschätzt? Das Risiko ist ihm egal (das ist der Job vom Skeptiker). Ihn interessiert nur, was passiert, wenn die Sache sogar besser läuft als gedacht.

### 4. Der Außenstehende
Hat null Kontext über dich, dein Feld oder deine Geschichte. Reagiert rein auf das, was vor ihm liegt. Der unterschätzteste Berater. Experten entwickeln blinde Flecken; der Außenstehende fängt den „Fluch des Wissens": Dinge, die für dich offensichtlich sind, aber für alle anderen verwirrend.

### 5. Der Macher
Interessiert sich nur für eins: Lässt sich das tatsächlich umsetzen, und was ist der schnellste Weg dahin? Theorie, Strategie, Big Picture – egal. Der Macher schaut auf jede Idee durch die Brille „Okay, aber was machst du Montagmorgen?" Klingt eine Idee brillant, hat aber keinen klaren ersten Schritt, sagt er's.

**Warum diese fünf:** Sie erzeugen drei natürliche Spannungen. Skeptiker gegen Visionär (Risiko gegen Chance). Grundsatz-Denker gegen Macher (alles neu denken gegen einfach machen). Der Außenstehende sitzt in der Mitte und hält alle ehrlich, indem er sieht, was frische Augen sehen.

---

## So läuft eine Sitzung (im Claude Chat)

**Der wichtigste Unterschied zum Original:** Im Claude Chat gibt es keine Sub-Agenten. Claude spielt alle fünf Berater selbst, nacheinander, innerhalb einer Antwort. Der Trick ist Disziplin: Bei jedem Berater voll auf dessen Linse committen. Nicht ausbalancieren, nicht vermischen, nicht hedgen. Jeder Berater ist bewusst einseitig – die Ausgewogenheit entsteht erst im Urteil.

### Schritt 1: Frage einrahmen (mit Kontext)

Wenn der User „rat" (oder einen anderen Trigger) schreibt, erst Kontext sammeln, dann einrahmen.

**Kontext ziehen** aus dem, was verfügbar ist:
- Der bisherige Chat-Verlauf
- Angehängte Dateien oder Bilder
- Projekt-Wissen, falls vorhanden
- Relevante Erinnerungen aus früheren Gesprächen

Kein langes Suchen. Du willst die zwei, drei Infos, die den Beratern erlauben, konkret statt generisch zu antworten (Business-Stage, Zielgruppe, Constraints, bisherige Ergebnisse).

**Frage einrahmen.** Aus der rohen User-Frage plus Kontext eine klare, neutrale Frage formulieren, die alle fünf Berater bekommen. Sie enthält:
1. Die Kern-Entscheidung
2. Wichtiger Kontext aus der Nachricht
3. Wichtiger Kontext aus Dateien/Erinnerungen
4. Was auf dem Spiel steht

Keine eigene Meinung reinmischen, nicht steuern. Aber genug Kontext geben, dass jede Antwort spezifisch wird.

Ist die Frage zu vage („rat: mein Business"), **eine** Rückfrage stellen. Nur eine. Dann weiter.

### Schritt 2: Die fünf Berater antworten

Schreib alle fünf Antworten aus, jede aus ihrer Linse. Pro Berater **60–120 Wörter**, direkt, einseitig, kein Vorgeplänkel – sofort in die Analyse.

Format pro Berater:

> **Der Skeptiker**
> [seine Antwort]

…und so weiter für alle fünf. Lass keinen Berater den anderen nachplappern. Wenn sich zwei zu ähnlich anfühlen, schärf die Linsen nach.

### Schritt 3: Das Kreuzfeuer (kurz halten)

Das ist der Schritt, der den Rat von „fünfmal fragen" unterscheidet. Tritt einen Schritt zurück und beantworte für dich drei Fragen:
1. Welche Antwort ist am stärksten – und warum?
2. Welche hat den größten blinden Fleck?
3. Was haben **alle fünf** übersehen?

Halt das kurz (3–5 Sätze reichen). Es muss nicht komplett ausgeschrieben werden – die Erkenntnisse fließen ins Urteil ein.

### Schritt 4: Das Urteil des Vorsitzenden

Jetzt synthetisierst du alles zu einem klaren Urteil. Genau diese Struktur:

## Worüber sich der Rat einig ist
[Punkte, auf die mehrere Berater unabhängig gekommen sind. Hohe-Konfidenz-Signale.]

## Worüber der Rat streitet
[Echte Meinungsverschiedenheiten. Nicht glattbügeln. Beide Seiten zeigen und erklären, warum vernünftige Berater unterschiedlich denken.]

## Was der Rat fast übersehen hätte
[Die blinden Flecken aus dem Kreuzfeuer. Das, was einzelne Berater verpasst haben und erst beim Zurücktreten auffiel.]

## Die Empfehlung
[Eine klare, direkte Empfehlung. Kein „kommt drauf an". Kein „beide Seiten haben recht". Eine echte Antwort mit Begründung. Der Vorsitzende darf gegen die Mehrheit entscheiden, wenn die Begründung des Außenseiters stärker ist.]

## Der erste Schritt
[Ein einziger konkreter nächster Schritt. Keine Liste mit zehn Punkten. Eine Sache.]

Sei direkt, hedge nicht. Der ganze Sinn des Rats ist, dir die Klarheit zu geben, die eine einzelne Perspektive nicht liefern kann.

### Optional: Visuelle Übersicht

Nur wenn der User es will (zum Speichern, Teilen oder Screen-recorden): ein sauberes, eigenständiges HTML-Artifact mit der Frage oben, dem Urteil prominent, einer kleinen Übersicht wer wie stand, und ausklappbaren Sektionen für die einzelnen Berater-Antworten. Schlicht, gut lesbar, kein Schnickschnack. Standardmäßig **nicht** anbieten, sondern am Ende kurz erwähnen, dass es das gibt.

---

## Beispiel

**User:** „gremium das: Festes Jobangebot annehmen oder selbstständig bleiben?"

> **Der Skeptiker:** Selbstständig klingt frei, ist aber Einkommens-Achterbahn ohne Sicherheitsnetz. Was, wenn drei Monate keine Aufträge kommen?
> **Der Grundsatz-Denker:** Du entscheidest nicht zwischen zwei Jobs, sondern zwischen Sicherheit und Autonomie. Welche brauchst du gerade mehr?
> **Der Visionär:** Wenn die Selbstständigkeit gerade läuft, ist der Job vielleicht das Risiko – du tauschst eine offene Decke gegen ein Gehalt.
> **Der Außenstehende:** Du erzählst mir nur die zwei Optionen, nicht wie's dir bei jeder im Bauch ist. Welche willst du heimlich, traust dich aber nicht?
> **Der Macher:** Frag, ob der Job 3 Monate warten kann. Wenn ja, hast du keine Entscheidung – sondern Zeit, beides zu testen.

**Urteil des Vorsitzenden**

## Worüber sich der Rat einig ist
Die Frage „Job oder selbstständig" ist eigentlich „Sicherheit oder Autonomie" – das musst du zuerst für dich klären.

## Worüber der Rat streitet
Wo das Risiko liegt. Skeptiker sieht es in der Selbstständigkeit, Visionär im Aufgeben einer laufenden Sache.

## Was der Rat fast übersehen hätte
Der Außenstehende fragt als Einziger nach dem Bauchgefühl statt nach der Logik – oft weißt du die Antwort längst und suchst nur Erlaubnis.

## Die Empfehlung
Bevor du entscheidest, prüf den Vorschlag des Machers: Lässt sich der Jobstart aufschieben? Dann ist es keine Entweder-oder-Frage.

## Der erste Schritt
Den Arbeitgeber fragen, wie flexibel der Starttermin ist.

---

## Wichtige Regeln

- **Alle fünf Berater wirklich ausspielen.** Nicht abkürzen, nicht zwei zu einem verschmelzen. Jede Linse einzeln, einseitig, committet.
- **Im Kreuzfeuer ehrlich sein.** Wenn eine Berater-Antwort schwach ist, sag es. Der blinde Fleck, der erst beim Zurücktreten auffällt, ist oft das Wertvollste.
- **Der Vorsitzende darf gegen die Mehrheit entscheiden.** Wenn 4 von 5 „mach's" sagen, aber die Begründung des einen Gegenstimme am stärksten ist, folgt der Vorsitzende dem einen – und erklärt warum.
- **Keine trivialen Fragen vor den Rat bringen.** Hat eine Frage eine richtige Antwort, beantworte sie einfach. Der Rat ist für echte Unsicherheit.
- **Keine Zahlen erfinden.** Wenn eine Empfehlung auf Marktdaten, Preisen oder Benchmarks beruht und keine belegte Quelle vorliegt: sag das offen und biete an zu recherchieren. Nicht raten.
- **Default ist die Chat-Antwort.** Das visuelle HTML nur auf Wunsch.

---

Methodik von Andrej Karpathy (LLM Council). Claude-Chat-Adaption auf Deutsch.
