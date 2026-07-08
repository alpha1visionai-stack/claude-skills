#!/bin/bash
#==============================================================================
# llm-council-skill Installer fuer Ubuntu / Linux
#
# Installiert:
#   - Python 3.11+ (falls nicht vorhanden)
#   - llm CLI (Simon Willison)
#   - llm-council-skill v0.2.0 (Ori Neidich)
#   - llm-gemini plugin
#   - llm-anthropic plugin
#   - Council-Konfiguration
#   - AGENTS.md (Web-Grounding-Pflicht)
#   - Skills: der-rat + expert-council
#
# Verwendung:
#   chmod +x install_ubuntu.sh
#   ./install_ubuntu.sh
#
# Optional: API-Key als Argument uebergeben
#   ./install_ubuntu.sh sk-or-v1-xxxxxxxx
#==============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
print_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
print_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo ""
echo "=============================================="
echo "  llm-council-skill Installer fuer Ubuntu"
echo "=============================================="
echo ""

OPENROUTER_KEY="${1:-${OPENROUTER_API_KEY:-}}"

# 1. System aktualisieren
print_info "Systempakete aktualisieren..."
sudo apt-get update -qq

# 2. Python installieren
if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_ok "Python 3 bereits installiert: $PY_VERSION"
else
    print_info "Python 3 installieren..."
    sudo apt-get install -y python3 python3-pip python3-venv
    print_ok "Python 3 installiert"
fi

# 3. pip aktualisieren
print_info "pip aktualisieren..."
python3 -m pip install --upgrade pip --quiet 2>/dev/null || sudo apt-get install -y python3-pip
print_ok "pip bereit"

# 4. llm CLI installieren
print_info "llm CLI installieren..."
python3 -m pip install --user llm 2>/dev/null || pip3 install --user llm
print_ok "llm CLI installiert"

export PATH="$HOME/.local/bin:$PATH"
if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    print_info "PATH in .bashrc ergaenzt"
fi

# 5. llm-council-skill installieren
print_info "llm-council-skill v0.2.0 installieren..."
pip3 install --user llm-council-skill 2>/dev/null || python3 -m pip install --user llm-council-skill
print_ok "llm-council-skill installiert"

# 6. Plugins installieren
print_info "llm-gemini und llm-anthropic Plugins installieren..."
python3 -m llm install llm-gemini 2>/dev/null || llm install llm-gemini
python3 -m llm install llm-anthropic 2>/dev/null || llm install llm-anthropic
print_ok "Plugins installiert"

# 7. Verzeichnisse erstellen
print_info "Verzeichnisse erstellen..."
mkdir -p "$HOME/.llm"
mkdir -p "$HOME/.llm/logs"
mkdir -p "$HOME/.codex"
mkdir -p "$HOME/.agents/skills/der-rat"
mkdir -p "$HOME/.agents/skills/expert-council"
print_ok "Verzeichnisse erstellt"

# 8. Konfiguration installieren
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/../config/council-config.json" ]; then
    print_info "council-config.json installieren..."
    cp "$SCRIPT_DIR/../config/council-config.json" "$HOME/.llm/council-config.json"
    print_ok "Council-Konfiguration installiert"
else
    print_warn "council-config.json nicht gefunden"
fi

# 9. AGENTS.md installieren
if [ -f "$SCRIPT_DIR/../config/AGENTS.md" ]; then
    print_info "AGENTS.md installieren (Web-Grounding-Pflicht)..."
    cp "$SCRIPT_DIR/../config/AGENTS.md" "$HOME/.codex/AGENTS.md"
    print_ok "AGENTS.md installiert"
fi

# 10. Skills installieren
if [ -f "$SCRIPT_DIR/../skills/der-rat/SKILL.md" ]; then
    print_info "Skill 'der-rat' installieren..."
    cp "$SCRIPT_DIR/../skills/der-rat/SKILL.md" "$HOME/.agents/skills/der-rat/SKILL.md"
    print_ok "der-rat installiert"
fi

if [ -f "$SCRIPT_DIR/../skills/expert-council/SKILL.md" ]; then
    print_info "Skill 'expert-council' installieren..."
    cp "$SCRIPT_DIR/../skills/expert-council/SKILL.md" "$HOME/.agents/skills/expert-council/SKILL.md"
    print_ok "expert-council installiert"
fi

# 11. API-Key setzen
if [ -n "$OPENROUTER_KEY" ]; then
    print_info "OPENROUTER_API_KEY setzen..."
    if ! grep -q 'OPENROUTER_API_KEY' "$HOME/.bashrc" 2>/dev/null; then
        echo "export OPENROUTER_API_KEY=\"$OPENROUTER_KEY\"" >> "$HOME/.bashrc"
    else
        sed -i "s|export OPENROUTER_API_KEY=.*|export OPENROUTER_API_KEY=\"$OPENROUTER_KEY\"|" "$HOME/.bashrc"
    fi
    export OPENROUTER_API_KEY="$OPENROUTER_KEY"
    print_ok "OPENROUTER_API_KEY gesetzt"
else
    print_warn "Kein OPENROUTER_API_KEY uebergeben!"
    print_warn "Setze ihn manuell: export OPENROUTER_API_KEY=\"sk-or-v1-dein-key\""
fi

# 12. Shell-Alias
if ! grep -q 'alias rat=' "$HOME/.bashrc" 2>/dev/null; then
    print_info "Shell-Alias 'rat' erstellen..."
    echo 'alias rat="llm-council --config \"$HOME/.llm/council-config.json\""' >> "$HOME/.bashrc"
    print_ok "Alias 'rat' hinzugefuegt"
fi

# 13. UTF-8 Encoding
if ! grep -q 'PYTHONIOENCODING' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PYTHONIOENCODING=utf-8' >> "$HOME/.bashrc"
    print_info "PYTHONIOENCODING=utf-8 in .bashrc ergaenzt"
fi

# 14. Verifikation
echo ""
print_info "Installation verifizieren..."
echo ""
echo -n "  llm Version:          "
llm --version 2>/dev/null || echo "FEHLER"
echo -n "  llm-council:          "
which llm-council 2>/dev/null || echo "FEHLER"
echo -n "  Council Config:       "
[ -f "$HOME/.llm/council-config.json" ] && echo "OK" || echo "FEHLT"
echo -n "  AGENTS.md:            "
[ -f "$HOME/.codex/AGENTS.md" ] && echo "OK" || echo "FEHLT"
echo -n "  Skill der-rat:        "
[ -f "$HOME/.agents/skills/der-rat/SKILL.md" ] && echo "OK" || echo "FEHLT"
echo -n "  Skill expert-council: "
[ -f "$HOME/.agents/skills/expert-council/SKILL.md" ] && echo "OK" || echo "FEHLT"
echo -n "  API-Key:              "
[ -n "$OPENROUTER_KEY" ] && echo "gesetzt" || echo "nicht gesetzt"

# 15. Dry-Run Test
if [ -n "$OPENROUTER_KEY" ]; then
    echo ""
    print_info "Dry-Run Test..."
    llm-council --config "$HOME/.llm/council-config.json" --dry-run "Test" 2>&1 || true
fi

echo ""
echo "=============================================="
echo "  Installation abgeschlossen!"
echo "=============================================="
echo ""
echo "  Naechste Schritte:"
echo "    1. Shell neu laden:  source ~/.bashrc"
echo "    2. API-Key pruefen:  echo \$OPENROUTER_API_KEY"
echo "    3. Council testen:   rat --dry-run 'Testfrage'"
echo "    4. Echte Frage:      rat 'Soll ich X oder Y?'"
echo ""
echo "  Dokumentation:"
echo "    docs/Der_Rat_und_Expert_Council_Dokumentation.md"
echo ""
