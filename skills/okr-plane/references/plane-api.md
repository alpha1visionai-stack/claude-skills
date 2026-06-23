# Plane API Referenz — NPE Projekt

## Basis-Konfiguration

```python
BASE    = 'https://plane.alpha-vision-ai.de/api/v1'
WS      = 'wholevital2'
HEADERS = {'X-API-Key': TOKEN, 'Content-Type': 'application/json'}
```

Token steht in `stacks/.env` → `PLANE_API_TOKEN`

## Endpoints (alle getestet, Stand 2026-06-17)

```
# Projekte
GET  /workspaces/{ws}/projects/?per_page=100

# Issues
GET  /workspaces/{ws}/projects/{pid}/issues/?per_page=500
POST /workspaces/{ws}/projects/{pid}/issues/
PATCH /workspaces/{ws}/projects/{pid}/issues/{iid}/

# Module
GET  /workspaces/{ws}/projects/{pid}/modules/?per_page=100

# Module-Issues  ← /module-issues/ NICHT /issues/
GET  /workspaces/{ws}/projects/{pid}/modules/{mid}/module-issues/
POST /workspaces/{ws}/projects/{pid}/modules/{mid}/module-issues/
DELETE /workspaces/{ws}/projects/{pid}/modules/{mid}/module-issues/{mi_id}/

# Labels
GET  /workspaces/{ws}/projects/{pid}/labels/

# Members  ← gibt LISTE zurück, kein {"results": [...]} Wrapper!
GET  /workspaces/{ws}/members/

# States
GET  /workspaces/{ws}/projects/{pid}/states/
```

## Projekt-IDs (aus NPE-OKR-Task-Mapping.json)

Beim Start per API abrufen:
```python
projs = get(f'{BASE}/workspaces/{WS}/projects/?per_page=100')['results']
proj_map = {p['identifier']: p for p in projs}
pid_buch = proj_map['BUCH']['id']
pid_npea = proj_map['NPEA']['id']
pid_ws   = proj_map['WS']['id']
```

## Issue-Felder

```python
# Relevante Felder beim GET:
issue = {
    'id': 'uuid',
    'name': 'Issue-Titel',
    'state': 'uuid',           # state ID (nicht state_id!)
    'parent': 'uuid | null',   # null = Parent-Task
    'assignees': ['uuid'],
    'label_details': [{'id': 'uuid', 'name': 'Future'}],
    'target_date': 'YYYY-MM-DD | null',
    'description_html': '...',
}

# PATCH zum Label setzen:
existing = [l['id'] for l in issue.get('label_details', [])]
patch(f'{BASE}/workspaces/{WS}/projects/{pid}/issues/{iid}/',
      {'label_ids': existing + [future_label_id]})
```

## Module-Issues POST

```python
# Mehrere Issues einem Modul zuweisen:
post(module_issues_url(pid, mid), {'issues': [id1, id2, id3]})

# Einzelnes Issue aus Modul entfernen:
# 1. GET module-issues → finde mi_id (nicht issue_id!)
# 2. DELETE .../module-issues/{mi_id}/
```

## Fehlerbehandlung

| Code | Bedeutung | Aktion |
|---|---|---|
| 401 | Falscher Auth-Header | Prüfe: X-API-Key statt Bearer |
| 403 | Falscher Workspace-Slug | Prüfe: wholevital2 (nicht wv) |
| 404 | Falscher Endpoint | Prüfe: module-issues/ nicht issues/ |
| 429 | Rate-Limit | sleep(15) dann retry; sleep(0.3) zwischen Calls |

## Members-Response Handling

```python
# BUG-FIX: members gibt Liste zurück, kein Dict mit "results"
raw = response.json()
members = raw if isinstance(raw, list) else raw.get("results", [])
member_map = {m['id']: m.get('display_name', '?') for m in members}
```

## Schreibrechte

- `stacks/` — owned by walter, direkt schreibbar
- `projekt-management/` — owned by mo, Muster:
  ```bash
  sudo cp /tmp/datei /home/mo/Dokumente/npe-project/projekt-management/datei
  sudo chown mo:mo /home/mo/Dokumente/npe-project/projekt-management/datei
  ```
