# Knowledge Builder v5.1 Logik

Diese Logik dient der maximalen Informationserhaltung bei der Verarbeitung von Diktaten und Chat-Prompts.

## 1. Extraktions-Prinzipien
- **Identifikation von Entitäten**: Alle Eigennamen (Personen, Firmen, Städte) müssen extrahiert werden.
- **Erhalt von Beispielen**: Anekdotische Evidenz (z.B. der Vorfall mit dem Messer in Marseille) darf nicht zu "Sicherheitsrisiken" abstrahiert werden, sondern muss als konkretes Beispiel erhalten bleiben.
- **Kausalitäten**: "Warum" wird etwas getan? (z.B. McDonald's Recruiting wegen der Nachtarbeits-Resilienz). Die Begründung ist so wichtig wie der Fakt selbst.
- **Numerische Präzision**: Alle Zahlen (Marktgrößen, Vakanzquoten, Daten) müssen exakt übernommen werden.

## 2. Der "France Factor"
Informationen mit Frankreich-Bezug sind besonders zu gewichten:
- **Rechtliche Schranken**: NAO (Négociations Annuelles Obligatoires).
- **Soziale Dynamik**: Gewerkschaftsdruck, Kriminalität in spezifischen Städten.
- **Operative Realität**: Investitionsstau, technische Instabilität.

## 3. Merging & De-Duplikation
- Bei widersprüchlichen Informationen hat der chronologisch letzte Prompt Vorrang (Korrektur-Logik).
- Redundante Informationen werden nicht gelöscht, sondern als Bestätigung des Fakts gewertet.
- Das Master-Dokument sollte thematisch sortiert sein (Vision, Board, MDs, Recruiting, Risiko, Kennzahlen).
