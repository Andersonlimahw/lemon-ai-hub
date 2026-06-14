# AI Marketplace

Repositório centralizado e otimizado para gerenciar **AI Skills e Plugins** entre diferentes agentes locais (Claude Code, Codex, OpenCode, Agy).

Este projeto é baseado e inspirado no padrão do Peter Steinberger (`steipete/agent-scripts`), mas estruturado com foco em `.claude` e compartilhado com os demais provedores via links simbólicos transparentes.

---

## 📂 Estrutura do Repositório

- **`skills/`**: Skills reutilizáveis e roteadores de prompts.
  - [`senior-prompt-engineer`](file:///Users/andersonlimadev/Projects/IA/ai-marketplace/skills/senior-prompt-engineer/SKILL.md): Stage-0 prompt refiner e definidor de Execution Map (`EXEC-MAP v1`).
  - [`skills-selector`](file:///Users/andersonlimadev/Projects/IA/ai-marketplace/skills/skills-selector/SKILL.md): Gatekeeper meta-skill que decide dinamicamente quais skills carregar sob demanda.
  - [`smart-dispatch`](file:///Users/andersonlimadev/Projects/IA/ai-marketplace/skills/smart-dispatch/SKILL.md): Roteamento inteligente de implementações com fallback e YOLO-mode.
  - [`karpathy-recipe`](file:///Users/andersonlimadev/Projects/IA/ai-marketplace/skills/karpathy-recipe/SKILL.md): Metodologia incremental de desenvolvimento (baseada na receita do Karpathy).
  - [`llm-wiki-curator`](file:///Users/andersonlimadev/Projects/IA/ai-marketplace/skills/llm-wiki-curator/SKILL.md): Manutenção automatizada de documentação estruturada `llms.txt`.
  - [`token-saver`](file:///Users/andersonlimadev/Projects/IA/ai-marketplace/skills/token-saver/SKILL.md): Skill genérica para instalação e configuração de ferramentas de economia de tokens.
- **`plugins/`**: Referências aos plugins instalados.
  - `marketplaces/karpathy-skills`: Link simbólico para os plugins locais instalados.
- **`scripts/`**: Helpers utilitários.
  - `setup-symlinks.sh`: Script para automatizar a criação dos links simbólicos globais.
  - `marketplace`: Interface CLI para listagem e gerenciamento de ferramentas de IA do repositório.

---

## 🚀 Instalação & Setup de Links Simbólicos

Para sincronizar suas configurações globais de agentes e compartilhar a mesma pasta de skills entre todos eles, execute o script de setup a partir da raiz do repositório:

```bash
chmod +x scripts/setup-symlinks.sh
./scripts/setup-symlinks.sh
```

Esse script realiza os seguintes passos:
1. Faz backup de pastas existentes (como `~/.claude/skills` se já existirem).
2. Cria o link simbólico `~/.claude/skills` apontando para a pasta `skills/` deste repositório.
3. Cria links simbólicos de `~/.codex/skills`, `~/.opencode/skills` e `~/.agy/skills` apontando diretamente para `~/.claude/skills`.

Com isso, qualquer skill adicionada ou atualizada neste repositório estará disponível imediatamente em todos os seus CLI de IA!

---

## 🛒 O CLI `marketplace`

Você pode listar as skills e os plugins ativos a qualquer momento através do utilitário `marketplace`:

```bash
./scripts/marketplace list-skills
./scripts/marketplace list-plugins
```

---

## 🪙 Otimização de Contexto e Token Saving (`token-saver`)

Para instalar e configurar de forma assistida as principais ferramentas de economia de tokens do ecossistema, utilize a skill `token-saver` (ou execute o script diretamente):

```bash
chmod +x skills/token-saver/scripts/setup-token-saving.sh
./skills/token-saver/scripts/setup-token-saving.sh
```

### O que o Setup Otimiza:
- **RTK (Rust Token Killer)**: Intercepta comandos de shell (git, tests, build) e remove outputs verbosos. (Use `rtk gain` para ver a auditoria).
- **Caveman Mode**: Reduz o tamanho das respostas (output tokens) em ~75% através de escrita telegráfica compacta.
- **Graphify**: Estrutura seu codebase em grafos de relacionamento `graphify-out/` para que a LLM encontre arquivos sem ler a pasta inteira.
- **Context-Mode**: Compacta logs longos, APIs e dumps grandes enviando apenas resumos estruturados para o contexto ativo do chat.
