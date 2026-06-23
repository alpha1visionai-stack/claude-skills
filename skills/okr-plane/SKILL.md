---
name: okr-plane
description: This skill should be used when the user asks to "plane issue analysieren", "klartext-check machen", "gap-analyse plane", "auftragskarte für plane schreiben", "issue in plane anlegen", "okr sync ausführen", "plane tasks prüfen", "klartext compliance prüfen", "NPE plane prüfen", "neues objective anlegen", "objective hinzufügen", "okr anlegen", "kr hinzufügen", or invokes "/okr-plane" or "/okr-add". Covers the full NPE OKR+Plane workflow: Klartext-Auftrag compliance checks, issue creation via plane_cli.py, bulk OKR sync via plane_okr_sync.py, gap analysis reports, and guided creation of new Objectives/KRs with Klartext cards per issue.
version: 1.3.0
---

# /okr-plane — NPE OKR & Plane PM Skill

Vier Haupt-Workflows: **Compliance-Check** (Klartext-Framework auf Plane-Issues anwenden), **Issue anlegen** (Klartext-Karte → Plane via CLI), **OKR-Sync** (Bulk-Zuweisung Issues → KR-Module), **Neues Objective** (geführte Abfrage → Klartext-Karte pro Issue → Anlegen in Plane).

## ⚡ Personas — Immer laden vor jeder Ressourcen-Zuweisung

Vor jedem Feld WER (Driver / Approver) die Datei `references/personas.md` heranziehen.
Vollständige Definitionen + DACI-Regeln stehen dort. Kurzreferenz:

**Menschen (Approver — immer genau 1, nie delegierbar):**

| Person | Rolle | Approver für |
|---|---|---|
| 👤 Mo | Business Lead | BUCH Exposé/Verlag/Launch, WS Sales/Pricing, NPEA Business (KR 2.4) |
| 👤 Oliver | Domain Lead | BUCH Kapitel (alle 11), WS Workshop-Design/Didaktik |
| 👤 Walter | CTO | Alle NPEA Features (Phase 7 Abnahme) |

**KI-Agenten (Driver — 1 pro Task):**

| Agent | Projekte | Phasen |
|---|---|---|
| 🤖 Ki-Agent-Briefing-Writer | NPEA | 1–3 |
| 🤖 Ki-Agent-Content-Writer | BUCH, WS | 1–3, 5–6 |
| 🤖 Ki-Agent-Content-Research | BUCH (Faktencheck), NPEA (R1/R2) | Recherche |
| 🤖 Ki-Agent-Architect | NPEA | 5 (Tech Spec) |
| 🤖 Ki-Agent-Developer | NPEA | 6 (Implementation) |
| 🤖 Ki-Agent-Marketing | WS, BUCH (KR 1.5) | 5–6 |
| 🤖 Ki-Agent-Project-Manager | Alle | PM-Tasks |

**Phase-Gates (nie überspringen):**
- Phase 4 `Review-Briefing` → Gate: Mo + Oliver setzen auf Done → erst dann startet Phase 5
- Phase 7 `Testing & final Review` → Gate: Walter nimmt ab → erst dann geht Feature live

## Kritische Konfiguration

```
Plane URL:       https://plane.alpha-vision-ai.de
Workspace-Slug:  wholevital2
Auth-Header:     X-API-Key: <token>        ← KEIN Bearer!
.env:            stacks/.env
```

Projekte: `BUCH` (O1) · `NPEA` (O2) · `WS` (O3) · `WHOLE` (O4)

---

## Workflow 1 — Klartext Compliance-Check

Analysiert Plane-Issues gegen das 6-Feld-Klartext-Framework. Ausgabe: Gap-Liste mit Severity.

**6 Felder prüfen:**

| Feld | Fehler-Muster | Severity |
|---|---|---|
| WAS | Tätigkeit statt Outcome ("erstellen", "entwickeln") | 🔴 |
| WOFÜR | Fehlt oder nur 1st-Order | 🟡 |
| WER: Approver | Nicht gesetzt (genau 1, nie delegierbar) | 🔴 |
| WER: Driver | Nicht gesetzt bei technischen Features | 🟠 |
| WIE | Leitplanken fehlen | 🟡 |
| BIS WANN | Kein `target_date` (BUCH+WS) | 🟠 |
| FERTIG WENN | Keine DoD-Kriterien | 🔴 |

**Vorgehen:**
1. Issues per API laden: `GET /api/v1/workspaces/wholevital2/projects/{pid}/issues/?per_page=500`
2. Nur Parent-Tasks analysieren (`parent == null`)
3. Für Approver-Zuweisung: Standard-Mapping aus Personas-Tabelle oben verwenden
4. Pro Gap: Severity + Beispiele + Maßnahmen-Owner
5. Output: `sudo cp /tmp/klartext-gap-analyse-YYYY-MM-DD.md /home/mo/Dokumente/npe-project/projekt-management/` + `sudo chown mo:mo`

---

## Workflow 2 — Issue anlegen (Klartext-Karte → Plane)

```bash
cd /home/mo/Dokumente/npe-project
python3 stacks/plane_cli.py <PROJ_KEY> <pfad/karte.md> [--module "KR Name"]
```

**PROJ_KEY**: `BUCH` / `NPEA` / `WS` / `WHOLE`

Driver und Approver aus Personas-Tabelle bestimmen, bevor die Karte geschrieben wird.

**Klartext-Karten-Template:**

```markdown
# [Outcome-Formulierung — was verändert sich?]

## WAS
[Outcome: nicht Tätigkeit]

## WOFÜR
[Impact 2nd/3rd Order — was bricht wenn dieser Task fehlt?]

## WER
- Driver: 🤖 Ki-Agent-[Name]
- Approver: 👤 [Mo | Oliver | Walter]
- Contributor: [optional]
- Informed: [optional]

## WIE
- Non-negotiable: [Leitplanken]
- Nicht: [Ausschlüsse]
- Frei: [Agency-Raum des Drivers]

## BIS WANN
2026-MM-DD

## FERTIG WENN
- [ ] Kriterium 1 (binär prüfbar)
- [ ] Kriterium 2

## ⚡ PROAKTIV-REGEL
Driver meldet bei Approver wenn Deadline in Gefahr, Scope-Änderung nötig oder Blocker erkannt.
```

---

## Workflow 3 — OKR Bulk-Sync

```bash
cd /home/mo/Dokumente/npe-project
python3 stacks/plane_okr_sync.py                 # alle Objectives
python3 stacks/plane_okr_sync.py --only O5       # nur O5
python3 stacks/plane_okr_sync.py --dry-run       # Vorschau
```

Weist alle Issues den KR-Modulen zu + setzt `🅿️ Future`-Labels.
Bei Rate-Limiting (429): 15s warten + retry mit `time.sleep(1–3)` zwischen Calls.

---

## Workflow 4 — Neues Objective anlegen (geführte Abfrage + Klartext)

**Trigger:** "neues Objective anlegen", "O5 anlegen", "neues OKR", "/okr-add"

Kein manuelles JSON-Editieren oder Skript-Starten nötig. Der Workflow läuft in zwei Phasen:
**Phase 1** sammelt die OKR-Struktur. **Phase 2** erstellt für jeden Issue eine Klartext-Karte,
prüft sie selbst, fragt nach was fehlt, und legt das Issue erst nach Bestätigung in Plane an.

---

### Phase 1 — Struktur abfragen

**Schritt 1 — Vorbedingung prüfen + Projekt ggf. anlegen:**
Plane-Projekte laden + nächste freie Objective-ID aus `stacks/okr-sync-config.json` lesen.
```
GET /api/v1/workspaces/wholevital2/projects/?per_page=100
```
- Projekt-Key **gefunden** → weiter mit Schritt 2
- Projekt-Key **nicht gefunden** → Projekt + Module automatisch anlegen:
```bash
cd /home/mo/Dokumente/npe-project
python3 stacks/plane_project_setup.py \
  --key PROJ_KEY \
  --name "Objective Name" \
  --modules "KR X.1 Name" "KR X.2 Name" \
  --add-all-members \
  --dry-run          # erst Vorschau zeigen, dann ohne --dry-run ausführen
```
Ergebnis abwarten, Projekt-ID + Modul-IDs aus JSON-Output merken → weiter mit Phase 2.

**Schritt 2 — Geführte Abfrage (eine Frage pro Nachricht):**

```
Frage 1:  Wie lautet die Objective-ID? (nächste freie wäre OX)
Frage 2:  Wie heißt das Objective?
Frage 3:  Plane-Projekt-Key? → API prüfen ob vorhanden
Frage 4:  Typ: [A] konzeptionell  [B] technisch (→ 7-Phasen-Pipeline)
```

**Schritt 3 — KR-Schleife (wiederholt bis "fertig" eingegeben wird):**

```
Frage KR-1:  Name des Key Results / Plane-Moduls?
             → API prüfen: Modul vorhanden? Wenn nein → automatisch anlegen:
               python3 stacks/plane_project_setup.py --key KEY --modules "KR Name"
Frage KR-2:  [Wenn technisch] Feature-Namen für 7-Phasen-Pipeline? (eine pro Zeile)
Frage KR-3:  Einzelne Issues (direkt nach Namen, eine pro Zeile)?
Frage KR-4:  Noch ein Key Result? (ja / fertig)
```

**Schritt 4 — Parkplatz (optional):**
```
Gibt es Issues für den Parkplatz (🅿️ Future-Label)? (ja / nein)
```

---

### Phase 2 — Klartext-Karte pro Issue (Mitprüfung + Nachfrage)

Für jeden gesammelten Issue-Namen — **einzeln und nacheinander**:

**2a — Karte entwerfen:**

Claude entwirft die Klartext-Karte automatisch aus dem Kontext:
- **WAS**: Issue-Name als Outcome umformulieren (kein Tätigkeitsverb — was verändert sich?)
- **WOFÜR**: aus KR-Name + Objective ableiten (2nd-Order-Impact — was bricht wenn dieser Task fehlt?)
- **WER Driver**: aus Persona-Matrix (Projekttyp → Agent)
- **WER Approver**: aus Persona-Matrix (Inhalt → Oliver · Business → Mo · Tech → Walter)
- **WIE**: Standard-Leitplanken für den Projekttyp vorschlagen
- **FERTIG WENN**: 2–3 binär prüfbare Kriterien vorschlagen

Alle abgeleiteten Felder mit **(Annahme)** markieren.

**2b — Selbstprüfung vor Anzeige (nie überspringen):**

Intern prüfen bevor die Karte ausgegeben wird:
- [ ] WAS ist ein Outcome, keine Tätigkeit?
- [ ] Genau 1 Approver (nie zwei gleichzeitig)?
- [ ] FERTIG WENN ist binär (ja/nein, nicht "gut genug")?
- [ ] Kein Feld leer ohne (Annahme)-Markierung?

**2c — Anzeigen + Nachfragen:**

```
📋 KLARTEXT-AUFTRAG — [Titel]

WAS         …
WOFÜR       …
WER         Driver: 🤖 …  ·  Approver: 👤 …
WIE         …
BIS WANN    (Annahme) ← bitte Datum nennen
FERTIG WENN • …
            • …
🔴 PROAKTIV  Driver meldet bei Approver wenn Deadline in Gefahr.

Passt diese Karte? → "ok" bestätigt · Korrekturen direkt nennen
BIS WANN fehlt noch — bitte Datum angeben (oder "gleich wie KR" für einheitliche Deadline).
```

BIS WANN **immer explizit nachfragen** — niemals raten oder weglassen.

**2d — Anlegen in Plane nach Bestätigung:**

```bash
# Karte nach /tmp/ schreiben, dann anlegen + direkt Modul zuweisen
cd /home/mo/Dokumente/npe-project
python3 stacks/plane_cli.py PROJ_KEY /tmp/issue-titel.md --module "KR X.Y Modulname"
```

Ausgabe: `✓ [Issue-Titel] angelegt + KR X.Y zugewiesen` → weiter mit nächstem Issue.

**Kein Batch — jede Karte einzeln bestätigen lassen.**

---

### Phase 3 — Config + Abschluss

**Schritt 5 — Config schreiben:**
```python
# stacks/okr-sync-config.json: neuen Objective-Block in "objectives" einfügen
# stacks/ ist walter-owned → direkt schreibbar (kein sudo nötig)
```
Dieser Eintrag sorgt dafür dass zukünftige Sync-Läufe das Objective kennen.

**Schritt 6 — Dry-Run zur Vollständigkeitsprüfung:**
```bash
python3 stacks/plane_okr_sync.py --only OX --dry-run
```
Prüft ob alle Issues korrekt den Modulen zugewiesen sind. Fehlende zeigen sich als ⚠️.

**Schritt 7 — Abschluss:**
- `references/okr-struktur.md` mit neuem Objective + KRs aktualisieren
- Zusammenfassung ausgeben: X Issues angelegt, Y Module befüllt

---

### Eiserne Regeln Workflow 4

- **Plane-Projekt und Module müssen vor Phase 2 existieren** — sonst schlägt plane_cli.py fehl
- **BIS WANN niemals weglassen** — immer nachfragen, nie erfinden
- **Jede Karte einzeln bestätigen** — kein "alle auf einmal anlegen"
- **Annahmen immer markieren** — jede Annahme muss aktiv bestätigt oder korrigiert werden
- **Genau 1 Approver** — bei Unklarheit fragen, nie zwei eintragen

---

## Kritische API-Details

```python
# Module-Issues Endpoint (NICHT /issues/ — gibt 404!)
f'{BASE}/workspaces/{WS}/projects/{pid}/modules/{mid}/module-issues/'

# Members gibt LISTE zurück (kein "results" Wrapper!)
raw = response.json()
members = raw if isinstance(raw, list) else raw.get("results", [])

# 7-Phasen-Namen (exakt so in Plane):
PHASES = ['Feature', '1. Sketch & Concept', '2. Project Plan & Timeline',
          '3. Initiative Briefing', '4. Review-Briefing',
          '5. Technical Specification', '6. Doing & Implementation',
          '7. Testing & final Review']
```

## Schreibrechte

- `stacks/` — owned by walter, direkt schreibbar
- `projekt-management/` — owned by mo:
  ```bash
  sudo cp /tmp/datei /home/mo/Dokumente/npe-project/projekt-management/datei
  sudo chown mo:mo /home/mo/Dokumente/npe-project/projekt-management/datei
  ```

## Referenzdateien

- **`references/personas.md`** — Vollständige Persona-Definitionen + DACI-Zuweisungsmatrix ← immer lesen vor WER-Feldern
- **`references/okr-struktur.md`** — OKR-Hierarchie O1–O4, alle 13 KR-Module ← nach Workflow 4 aktualisieren
- **`references/plane-api.md`** — API-Endpoints, Auth-Fixes, Fehlerbehandlung
- **`references/gap-analyse-checkliste.md`** — Prüfkriterien, DoD-Templates, Severity-Regeln

## Framework Source of Truth

```
stacks/okr_task_management_handbook.md      ← OKR + 7-Phasen System
stacks/Klartext-Auftrag_Framework.md        ← Vollständiges Klartext-Framework
stacks/Klartext-Auftrag_Agent-Prompt_v2.md ← Agent-Prompt Vorlage
stacks/okr-sync-config.json                ← Task→KR Mapping (Single Source of Truth, v2)
stacks/plane_project_setup.py              ← Projekt + Module + Mitglieder via API anlegen
stacks/personas/                            ← Einzelne Persona-Dateien (Quellen)
```
