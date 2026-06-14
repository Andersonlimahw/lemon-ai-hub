#!/usr/bin/env bash

# setup-token-saving.sh - Configures RTK, Caveman, Graphify, and Context-Mode.
# Supports both interactive prompts and command-line arguments.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_PROJECT_DIR="$(pwd)"

# Default selections
INSTALL_RTK=""
SCOPE_RTK="global"

INSTALL_CAVEMAN=""
SCOPE_CAVEMAN="global"

INSTALL_GRAPHIFY=""
SCOPE_GRAPHIFY="project"

INSTALL_CONTEXT_MODE=""
SCOPE_CONTEXT_MODE="global"

INTERACTIVE=true

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --non-interactive)
      INTERACTIVE=false
      shift
      ;;
    --rtk)
      INSTALL_RTK="y"
      SCOPE_RTK="${2:-global}"
      shift 2
      ;;
    --caveman)
      INSTALL_CAVEMAN="y"
      SCOPE_CAVEMAN="${2:-global}"
      shift 2
      ;;
    --graphify)
      INSTALL_GRAPHIFY="y"
      SCOPE_GRAPHIFY="${2:-project}"
      shift 2
      ;;
    --context-mode)
      INSTALL_CONTEXT_MODE="y"
      SCOPE_CONTEXT_MODE="${2:-global}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

prompt_user() {
  local prompt_text="$1"
  local default_val="$2"
  local user_input
  
  if [ "$INTERACTIVE" = true ]; then
    read -rp "$prompt_text [$default_val]: " user_input
    echo "${user_input:-$default_val}"
  else
    echo "$default_val"
  fi
}

echo "=== Token Saving Setup Wizard ==="

# 1. RTK Prompt
if [ -z "$INSTALL_RTK" ]; then
  INSTALL_RTK=$(prompt_user "Deseja instalar/configurar o RTK (Rust Token Killer)? (y/n)" "y")
  if [ "$INSTALL_RTK" = "y" ]; then
    SCOPE_RTK=$(prompt_user "Escopo do RTK ([g]lobal / [p]rojeto)?" "g")
    if [ "$SCOPE_RTK" = "g" ] || [ "$SCOPE_RTK" = "global" ]; then
      SCOPE_RTK="global"
    else
      SCOPE_RTK="project"
    fi
  fi
fi

# 2. Caveman Prompt
if [ -z "$INSTALL_CAVEMAN" ]; then
  INSTALL_CAVEMAN=$(prompt_user "Deseja ativar o Caveman Mode (comunicação comprimida ~75%)? (y/n)" "y")
  if [ "$INSTALL_CAVEMAN" = "y" ]; then
    SCOPE_CAVEMAN=$(prompt_user "Escopo do Caveman ([g]lobal / [p]rojeto)?" "g")
    if [ "$SCOPE_CAVEMAN" = "g" ] || [ "$SCOPE_CAVEMAN" = "global" ]; then
      SCOPE_CAVEMAN="global"
    else
      SCOPE_CAVEMAN="project"
    fi
  fi
fi

# 3. Graphify Prompt
if [ -z "$INSTALL_GRAPHIFY" ]; then
  INSTALL_GRAPHIFY=$(prompt_user "Deseja configurar o Graphify (Knowledge Graph de codebase)? (y/n)" "y")
  if [ "$INSTALL_GRAPHIFY" = "y" ]; then
    SCOPE_GRAPHIFY=$(prompt_user "Escopo do Graphify ([g]lobal / [p]rojeto)?" "p")
    if [ "$SCOPE_GRAPHIFY" = "g" ] || [ "$SCOPE_GRAPHIFY" = "global" ]; then
      SCOPE_GRAPHIFY="global"
    else
      SCOPE_GRAPHIFY="project"
    fi
  fi
fi

# 4. Context-Mode Prompt
if [ -z "$INSTALL_CONTEXT_MODE" ]; then
  INSTALL_CONTEXT_MODE=$(prompt_user "Deseja instalar o Context-Mode (compactação de contexto)? (y/n)" "y")
  if [ "$INSTALL_CONTEXT_MODE" = "y" ]; then
    SCOPE_CONTEXT_MODE=$(prompt_user "Escopo do Context-Mode ([g]lobal / [p]rojeto)?" "g")
    if [ "$SCOPE_CONTEXT_MODE" = "g" ] || [ "$SCOPE_CONTEXT_MODE" = "global" ]; then
      SCOPE_CONTEXT_MODE="global"
    else
      SCOPE_CONTEXT_MODE="project"
    fi
  fi
fi

# Apply RTK Setup
if [ "$INSTALL_RTK" = "y" ]; then
  echo "=> Configurando RTK..."
  if ! command -v rtk &> /dev/null; then
    echo "Aviso: Executável 'rtk' não foi encontrado no PATH."
    echo "Instrução de instalação: execute 'brew install steipete/tap/rtk' ou obtenha a partir de https://github.com/steipete/rtk"
  else
    echo "RTK encontrado em $(which rtk)."
  fi
  
  if [ "$SCOPE_RTK" = "global" ]; then
    export ENABLE_RTK=1
  else
    echo "Para configurar RTK apenas no projeto, adicione 'rtk hook claude' nos scripts locais ou config."
  fi
fi

# Apply Caveman Setup
if [ "$INSTALL_CAVEMAN" = "y" ]; then
  echo "=> Configurando Caveman Mode..."
  
  CAVEMAN_INSTRUCTIONS="
# Caveman Mode (Active)
Work style: telegráfico, noun-phrases, min tokens.
Respostas curtas, sem enrolação, sem formalidades.
"
  if [ "$SCOPE_CAVEMAN" = "global" ]; then
    export ENABLE_CAVEMAN=1
    CLAUDE_MD="$HOME/.claude/CLAUDE.md"
    if [ -f "$CLAUDE_MD" ]; then
      if ! grep -q "Caveman Mode" "$CLAUDE_MD"; then
        echo "$CAVEMAN_INSTRUCTIONS" >> "$CLAUDE_MD"
        echo "Instruções Caveman adicionadas a $CLAUDE_MD"
      fi
    else
      echo "$CAVEMAN_INSTRUCTIONS" > "$CLAUDE_MD"
      echo "Criado $CLAUDE_MD com instruções Caveman"
    fi
  else
    # Project scope
    PROJECT_CLAUDE_MD="$CURRENT_PROJECT_DIR/CLAUDE.md"
    if ! grep -q "Caveman Mode" "$PROJECT_CLAUDE_MD" 2>/dev/null; then
      echo "$CAVEMAN_INSTRUCTIONS" >> "$PROJECT_CLAUDE_MD"
      echo "Instruções Caveman adicionadas ao CLAUDE.md do projeto"
    fi
  fi
fi

# Apply Graphify Setup
if [ "$INSTALL_GRAPHIFY" = "y" ]; then
  echo "=> Configurando Graphify..."
  if ! command -v graphify &> /dev/null; then
    echo "Graphify não instalado globalmente. Clonando do repositório..."
    # Local clone / build or setup instructions
    echo "Clone/Build: git clone https://github.com/safishamsi/graphify.git ~/.graphify"
    echo "Consulte a documentação em https://github.com/safishamsi/graphify para instalar o binário."
  else
    echo "Graphify encontrado em $(which graphify)."
  fi

  if [ "$SCOPE_GRAPHIFY" = "project" ]; then
    echo "Inicializando Graphify no projeto atual..."
    if [ -d "$CURRENT_PROJECT_DIR" ]; then
      # Simula ou roda a inicialização do graphify no projeto
      mkdir -p "$CURRENT_PROJECT_DIR/graphify-out"
      echo "Criado diretório graphify-out/ no projeto para os grafos de conhecimento."
      
      # Adicionar instrução ao CLAUDE.md do projeto
      GRAPHIFY_RULE="
# Graphify Codebase Q&A
Se a pasta 'graphify-out/' estiver no projeto, consulte o knowledge graph ANTES de fazer buscas lineares ou explorar múltiplos arquivos.
"
      PROJECT_CLAUDE_MD="$CURRENT_PROJECT_DIR/CLAUDE.md"
      if ! grep -q "Graphify" "$PROJECT_CLAUDE_MD" 2>/dev/null; then
        echo "$GRAPHIFY_RULE" >> "$PROJECT_CLAUDE_MD"
        echo "Regra Graphify adicionada ao CLAUDE.md do projeto"
      fi
    fi
  fi
fi

# Apply Context-Mode Setup
if [ "$INSTALL_CONTEXT_MODE" = "y" ]; then
  echo "=> Configurando Context-Mode..."
  if [ "$SCOPE_CONTEXT_MODE" = "global" ]; then
    export ENABLE_CONTEXT_MODE=1
  fi
fi

# Run settings updater if global modifications were requested
if [ "${ENABLE_RTK:-0}" = "1" ] || [ "${ENABLE_CAVEMAN:-0}" = "1" ] || [ "${ENABLE_CONTEXT_MODE:-0}" = "1" ]; then
  echo "=> Atualizando settings.json global de ~/.claude/..."
  node "$SCRIPT_DIR/update-settings.js"
fi

echo "=== Configuração Concluída com Sucesso! ==="
echo ""
echo "Instruções Rápidas de Uso:"
echo "--------------------------------------------------------"
echo "1. RTK: Use 'rtk gain' para ver a auditoria de economia."
echo "2. Caveman: O agent falará de forma extremamente compacta."
echo "3. Graphify: Se no projeto, o agent usará 'graphify-out/' para acelerar as buscas de arquitetura."
echo "4. Context-Mode: O plugin está ativo e gerencia outputs longos automaticamente."
echo "--------------------------------------------------------"
