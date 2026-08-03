# Marker deutscher KI-Texte — was zählt und was nicht

Diese Datei erklärt, *warum* die Signale funktionieren und wo sie versagen.
Ohne dieses Verständnis werden aus Messwerten falsche Urteile.

## Inhalt

1. Die Grundidee
2. Was das Skript messen kann
3. Was nur beim Lesen auffällt
4. Häufige Fehlalarme
5. Häufige Fehlschlüsse in die andere Richtung
6. Evidenz außerhalb des Textes

---

## 1. Die Grundidee

Ein Sprachmodell wählt bei jedem Wort das statistisch naheliegendste aus einer
gedämpften Verteilung. Das erzeugt Text, der *zu wahrscheinlich* ist: gleichmäßig
im Rhythmus, mittig im Wortschatz, symmetrisch im Argument, sauber in der
Typografie. Menschen schreiben unwahrscheinlicher. Sie verlieren den Faden,
werden ungerecht, wiederholen sich, tippen daneben, brechen einen Gedanken ab.

Alle Signale unten sind Varianten dieses einen Gedankens. Man sucht nicht nach
„KI-Wörtern", sondern nach **fehlender Unregelmäßigkeit**.

Wichtig: Diese Signale messen *Textoberfläche*, nicht Autorschaft. Ein Mensch,
der gleichmäßig und sauber schreibt, erzeugt dieselbe Oberfläche. Deshalb ist
das Ergebnis immer ein Indizienbild und niemals ein Nachweis.

---

## 2. Was das Skript messen kann

### Rhythmus (stärkstes quantitatives Signal)

| Messwert | KI-typisch | Mensch-typisch |
|---|---|---|
| Variationskoeffizient der Satzlängen | unter 0,40 | 0,45–0,85 |
| Anteil Sätze im ±25 %-Korridor | über 0,60 | 0,35–0,50 |
| Sätze unter 5 Wörtern | keine | kommen vor |
| Absatzlängen | fast identisch | ungleich |

Der Variationskoeffizient (Standardabweichung geteilt durch Mittelwert) ist
robust gegen Textlänge und Textsorte. Menschen wechseln unbewusst zwischen
Anlauf, Ausführung und Punchline. Modelle produzieren Sätze, die alle etwa
gleich viel Arbeit erledigen.

### Typografie (stärkstes Einzelsignal, wenn es zutrifft)

- **Geviertstrich —** (U+2014): Auf deutscher Tastatur nicht ohne Umweg
  tippbar. Wer ihn im Fließtext benutzt, hat kopiert, ein Autokorrektur-Tool
  benutzt, oder es ist ein professioneller Satz. Drei oder mehr im Text sind
  ein starkes Signal.
- **Geschütztes Leerzeichen, Zero-Width-Zeichen**: Reste aus dem HTML einer
  Chat-Oberfläche. Fast beweisend für Copy-Paste — sagt aber nur, dass der
  Text durch eine Web-UI ging, nicht wer ihn schrieb.
- **`- **Begriff**: Erklärung`**: Die charakteristische LLM-Listenform.
- **Typografisches Auslassungszeichen …** statt drei getippter Punkte.
- **Null Tippunsauberkeiten über 300+ Wörter**: kein doppeltes Leerzeichen,
  kein Wortdoppler, kein fehlendes Leerzeichen nach Komma. Menschen, die
  nicht lektorieren, schaffen das selten.

### Wortwahl

- **Konnektoren-Überschuss**: „darüber hinaus", „zudem", „ferner",
  „des Weiteren", „folglich", „somit", „insbesondere". Über 2 pro 100 Wörter
  ist auffällig. Modelle klammern Sätze aneinander, weil das lokal
  wahrscheinlich ist, auch wenn die logische Beziehung dünn ist.
- **Nominalstil**: Häufung auf -ung, -heit, -keit, -ierung, -barkeit.
  Über 7 pro 100 Wörter ist ein Signal — aber auch das Kennzeichen von
  Behörden- und Fachdeutsch (siehe Fehlalarme).
- **Floskelkatalog**: „Es ist wichtig zu betonen", „In der heutigen
  schnelllebigen Welt", „spielt eine entscheidende Rolle", „Zusammenfassend
  lässt sich sagen", „nicht nur X, sondern auch Y". Einzeln bedeutungslos,
  in Häufung deutlich.
- **Wertungsvokabular ohne Substanz**: ganzheitlich, nachhaltig, innovativ,
  maßgeschneidert, nahtlos, robust, wegweisend, Mehrwert, Potenzial.

### Mensch-Signale (Gegenevidenz, gleich wichtig)

- **Modalpartikeln**: halt, eigentlich, irgendwie, naja, tja, wobei, quasi,
  ziemlich, echt, eh, sowieso. Ein Modell schreibt sie in Sachtexten fast
  nie unaufgefordert.
- **Konkretheit**: Zahlen mit Nachkommastellen, echte Datumsangaben,
  Eigennamen, Beträge, Aktenzeichen, Durchwahlen. Modelle erfinden solche
  Details nur, wenn man sie darum bittet — und dann meist rund und glatt
  („etwa 5.000 Euro" statt „4.812,40 Euro").
- **Tippunsauberkeit**: Wortdoppler, fehlende Leerzeichen, gemischte
  Anführungszeichen, „!!", abgebrochene Sätze.
- **Ich-Perspektive mit Einsatz**: nicht „Ich denke, dass Weiterbildung
  wichtig ist", sondern „Ich hatte vorher Bauchschmerzen, weil der
  Geschäftsführer meinte …".

---

## 3. Was nur beim Lesen auffällt

Diese Punkte kann kein Skript zählen. Sie sind oft aussagekräftiger als alle
Messwerte zusammen — deshalb ist das Lesen kein optionaler Schritt.

**Symmetrische Abwägung.** KI-Texte wiegen ab, wo ein Mensch längst eine
Meinung hätte. Wenn jeder Vorteil einen etwa gleich langen Nachteil bekommt
und der Text am Ende niemanden vor den Kopf stößt, ist das ein Signal.

**Vollständigkeit ohne Schwerpunkt.** Modelle deckeln das Thema gleichmäßig
ab, statt sich an dem festzubeißen, was den Autor wirklich interessiert.
Menschen sind unfair verteilt — sie schreiben drei Absätze über ihr
Lieblingsdetail und einen Halbsatz über den Rest.

**Beispiele ohne Herkunft.** „Ein Unternehmen aus der Fertigungsbranche
konnte seine Effizienz deutlich steigern" — keine Firma, keine Zahl, kein
Jahr. Menschen erzählen Beispiele, die sie kennen, mit Namen und Ärger.

**Keine Kosten.** Echte Erfahrung hinterlässt Spuren: eine gescheiterte
Sache, ein Vorwurf, ein Preis, den jemand bezahlt hat. KI-Texte sind meist
folgenlos.

**Zu gut zum Thema passende Überschriften.** Perfekt parallele Gliederung
(drei Punkte, jeder mit Unterpunkten, jeder etwa gleich lang).

**Keine Abschweifung.** Menschen verlassen das Thema und kommen zurück.

**Beharrlicher Registerwechsel.** Wenn ein Text zwischen sehr formellen und
sehr lockeren Passagen wechselt, ohne dass es Sinn ergibt, deutet das auf
ein Zusammenkleben aus mehreren Quellen — Mensch *und* KI.

**Sachliche Glätte mit Fehlern.** Modelle formulieren falsche Angaben
genauso souverän wie richtige. Eine erfundene Normnummer oder ein falsch
zitiertes Gesetz in einem sonst tadellosen Text ist ein starkes Signal.
Angaben stichprobenartig prüfen, wenn es die Sache hergibt.

---

## 4. Häufige Fehlalarme

Diese Textsorten sehen von Natur aus wie KI-Text. Hier ist besondere
Zurückhaltung angebracht — sag es im Befund ausdrücklich.

- **Behörden- und Rechtstexte.** Nominalstil, gleichmäßige Sätze, keine
  Partikeln, keine Ich-Perspektive. Genau das Profil.
- **Fachtexte und Normen.** Dito, plus Fachvokabular, das wie
  Wertungsvokabular aussieht.
- **Übersetzungen.** Übersetzte Texte verlieren die Idiosynkrasien des
  Originals und werden rhythmisch glatter.
- **Lektorierte oder redigierte Texte.** Ein Lektorat entfernt genau die
  Unregelmäßigkeiten, auf die wir schauen. Ein guter Journalist liest wie
  ein Modell — auf der Oberfläche.
- **Nicht-Muttersprachler.** Wer Deutsch als Fremdsprache schreibt, benutzt
  weniger Partikeln, einfachere und gleichmäßigere Satzbauten und einen
  vorsichtigeren Wortschatz. Das ist ein besonders unfairer Fehlalarm, weil
  er ausgerechnet die Leute trifft, die sich am meisten Mühe geben.
- **Sehr kurze Texte.** Unter 200 Wörtern tragen die Messwerte kaum. Das
  Skript dämpft dafür, aber Zurückhaltung bleibt Pflicht.
- **Schablonentexte.** Angebote, Serienbriefe, Stellenanzeigen,
  Produktbeschreibungen aus dem Baukasten.

---

## 5. Häufige Fehlschlüsse in die andere Richtung

- **„Es hat Tippfehler, also Mensch."** Fehler lassen sich in zehn Sekunden
  einbauen. Wer täuschen will, tut genau das.
- **„Es klingt persönlich, also Mensch."** Ein Modell schreibt auf
  Zuruf jede Ich-Perspektive.
- **„Detektor sagt 0 %, also Mensch."** Umschreibewerkzeuge („Humanizer")
  sind darauf gebaut, jeden statistischen Detektor zu unterlaufen. Sie
  brechen den Rhythmus, streuen Partikeln ein und ersetzen Floskeln. Was
  sie schlecht können: echte, überprüfbare Konkretheit und einen Text mit
  Einsatz.
- **Mischtexte sind der Normalfall.** Der häufigste reale Fall ist nicht
  „ganz KI" oder „ganz Mensch", sondern: Mensch schreibt Rohfassung, KI
  glättet — oder KI schreibt Rohfassung, Mensch überarbeitet. Beides
  erzeugt mittlere Werte. Bei gemischten Befunden ist „teils/teils" die
  richtige Antwort, nicht ein Münzwurf.

---

## 6. Evidenz außerhalb des Textes

Wenn wirklich etwas davon abhängt, ist Textanalyse der schwächste
verfügbare Beweis. Stärker ist:

- **Dateimetadaten**: Erstellungs- und Bearbeitungszeit, Autorenfeld,
  Bearbeitungsdauer in der Word-Datei. 4.000 Wörter mit 6 Minuten
  Bearbeitungszeit sind aussagekräftiger als jede Stilanalyse.
- **Versionsverlauf**: Google Docs, Word-Versionen, Git. Ein Text, der in
  einem Sprung erscheint, entstand nicht beim Schreiben.
- **Entstehungsspuren**: Notizen, Zwischenstände, Quellenliste, Randnotizen.
- **Gespräch mit dem Autor**: Wer den Text selbst geschrieben hat, kann
  erklären, warum eine Stelle so und nicht anders formuliert ist, welche
  Variante er verworfen hat und woher ein Beispiel kommt. Das ist
  belastbarer als jeder Score — und respektvoller.

Wenn der Zweck der Prüfung eine Konsequenz für eine Person hat (Bewerbung,
Prüfungsleistung, Vertragsstreit), gehört dieser Hinweis in den Befund.
