#!/usr/bin/env bash
# harness-doctor.sh — Verifica saúde do ecossistema multi-harness (Claude = fonte da verdade).
# Checa symlinks, hooks (rtk/caveman/context-mode), configs e drift entre harnesses.
#
# Uso:  bash scripts/harness-doctor.sh          # checks locais (sem rede)
#       bash scripts/harness-doctor.sh --net    # + smoke-test zai (chama API)
set -uo pipefail

HUB="$HOME/Projects/IA/lemon-ai-hub/plugins"
PASS=0; FAIL=0; WARN=0

ok()   { printf '  \033[32mOK\033[0m    %s\n' "$1"; PASS=$((PASS+1)); }
bad()  { printf '  \033[31mFAIL\033[0m  %s\n' "$1"; FAIL=$((FAIL+1)); }
warn() { printf '  \033[33mWARN\033[0m  %s\n' "$1"; WARN=$((WARN+1)); }

link_is() { # $1=link $2=expected_target
  [ -L "$1" ] && [ "$(readlink "$1")" = "$2" ]
}

echo "=== harness-doctor — $(date +%F) ==="

echo "[hub]"
[ -d "$HUB" ] && ok "hub plugins/ existe ($(ls "$HUB" | wc -l | tr -d ' ') plugins)" || bad "hub ausente: $HUB"

echo "[rtk]"
if command -v rtk >/dev/null 2>&1; then
  ok "binário: $(rtk --version 2>/dev/null | head -1)"
  R=$(echo '{"tool_name":"Bash","tool_input":{"command":"git status"}}' | rtk hook claude 2>/dev/null)
  case "$R" in *'rtk git status'*) ok "processor 'rtk hook claude' reescreve" ;; *) bad "'rtk hook claude' não reescreveu" ;; esac
  grep -q '"rtk hook claude"' "$HOME/.claude/settings.json" && ok "hook instalado em settings.json (PreToolUse Bash)" || bad "hook rtk ausente em ~/.claude/settings.json"
else
  bad "rtk não encontrado no PATH"
fi

echo "[claude ~/.claude]"
for f in CLAUDE.md RTK.md kaparthy.md settings.json; do
  [ -r "$HOME/.claude/$f" ] && ok "$f" || bad "$f ausente"
done
if [ -e "$HOME/.claude/skills" ]; then
  warn "~/.claude/skills existe — duplica skills do marketplace; remova (design: marketplace lemon-ai-hub cobre o hub)"
else
  ok "~/.claude/skills ausente (correto: marketplace cobre o hub)"
fi
grep -q '"caveman@caveman": true' "$HOME/.claude/settings.json" && ok "caveman plugin habilitado" || bad "caveman plugin desabilitado"
grep -q '"context-mode@context-mode": true' "$HOME/.claude/settings.json" && ok "context-mode plugin habilitado" || bad "context-mode desabilitado"
grep -q 'ctx-recall.sh' "$HOME/.claude/settings.json" && ok "ctx-recall (memory recall) no SessionStart" || warn "ctx-recall não wired"
grep -q 'auto-model-selector.sh' "$HOME/.claude/settings.json" && ok "auto-model-selector no UserPromptSubmit" || warn "auto-model-selector não wired"

echo "[codex ~/.codex]"
link_is "$HOME/.codex/skills" "$HUB" && ok "skills → hub" || bad "skills symlink incorreto: $(readlink "$HOME/.codex/skills" 2>/dev/null || echo ausente)"
[ -r "$HOME/.codex/AGENTS.md" ] && ok "AGENTS.md" || bad "AGENTS.md ausente"
[ -r "$HOME/.codex/RTK.md" ] && ok "RTK.md" || warn "RTK.md ausente (referenciado por AGENTS.md)"

echo "[agy ~/.agy]"
link_is "$HOME/.agy/skills" "$HUB" && ok "skills → hub" || bad "skills symlink incorreto: $(readlink "$HOME/.agy/skills" 2>/dev/null || echo ausente)"
[ -r "$HOME/.agy/AGENTS.md" ] && ok "AGENTS.md" || bad "AGENTS.md ausente"

echo "[opencode ~/.config/opencode]"
OC="$HOME/.config/opencode"
[ -r "$OC/AGENTS.md" ] && ok "AGENTS.md" || bad "AGENTS.md ausente"
ls "$OC"/opencode.json* >/dev/null 2>&1 && ok "opencode.json" || bad "opencode.json ausente"
for p in rtk.ts ctx-recall.ts; do
  [ -r "$OC/plugins/$p" ] && ok "plugin $p" || warn "plugin $p ausente"
done
DRIFT=0
if [ -d "$OC/skills" ]; then
  for entry in "$OC/skills"/*/; do
    [ -d "$entry" ] || continue
    n="$(basename "$entry")"
    if [ ! -L "${entry%/}" ] && [ -d "$HUB/$n" ]; then
      bad "skill '$n' é cópia física do hub (drift) — rode setup-symlinks.sh"
      DRIFT=1
    fi
  done
  [ "$DRIFT" = 0 ] && ok "skills sem drift (hub-backed = symlinks)"
else
  warn "skills/ ausente"
fi

echo "[gemini ~/.gemini]"
[ -r "$HOME/.gemini/GEMINI.md" ] && ok "GEMINI.md" || warn "GEMINI.md ausente"
[ -d "$HOME/.gemini/skills" ] && ok "skills/ ($(ls "$HOME/.gemini/skills" | wc -l | tr -d ' ') curadas)" || warn "skills/ ausente"

echo "[agents git-master]"
for d in "$HOME/.claude/agents" "$HOME/.codex/agents" "$HOME/.agy/agents" "$OC/agents" "$HOME/.gemini/config/agents"; do
  [ -e "$d/git-master.md" ] && ok "$(echo "$d" | sed "s|$HOME|~|")/git-master.md" || warn "git-master ausente em $(echo "$d" | sed "s|$HOME|~|")"
done

echo "[zai]"
[ -r "$HOME/.claude/env-zai.json" ] && ok "env-zai.json (perfil provider)" || warn "env-zai.json ausente"
if [ "${1:-}" = "--net" ]; then
  bash "$HOME/.claude/hooks/zai-health.sh" glm-4.5-air || warn "zai-health falhou"
fi

echo
echo "=== resumo: $PASS OK / $WARN WARN / $FAIL FAIL ==="
[ "$FAIL" -eq 0 ]
