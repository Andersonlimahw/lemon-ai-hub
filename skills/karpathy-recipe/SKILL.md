---
name: karpathy-recipe
description: Aplica "A Recipe for Training Neural Networks" de Karpathy adaptado a engenharia de software. Força baseline mínimo rodável antes de otimizar, um knob por vez, eval verificável no início. Use ao implementar feature nova, refactor não-trivial, integrar serviço externo, ou quando user disser "implementar X do zero", "como começar feature Y", "recipe", "abordagem incremental", "baseline first".
---

# karpathy-recipe

Tradução do [Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/) para features de produto. Princípio: **be paranoid, go slow, visualize everything**.

## Fluxo obrigatório

### 1. Become one with the data
Antes de codar, ler dados reais do domínio:
- Para feature financeira: 10 transações reais do `extratos_exemplo/` ou de `financial_transactions` em staging
- Para AI: 5 exemplos de input/output esperado do user
- Listar edge cases conhecidos (memory, ADRs, issues passadas) — não inventar

Output: 1 parágrafo no PR `## Dados que olhei` com links/IDs.

### 2. Set up end-to-end skeleton + dumb baseline
Implementar **caminho completo** com lógica trivial primeiro:
- Server action retorna mock fixo
- Repository retorna `[]`
- UI usa dado hardcoded

Validar que pipeline inteiro roda (request → action → repo → DB → UI) antes de qualquer lógica real. **Não otimizar nada ainda.**

### 3. Overfit the simplest case
Próximo: fazer funcionar em **1 input** real, ignorando edge cases. Mock externals (Stripe, Belvo, OpenAI). Confirmar logs/output esperados.

### 4. Add one knob at a time
Adicionar features em ordem (validation → real DB → external API → caching → optimization). Após cada knob:
- rodar `rtk npm test`
- rodar `rtk tsc --noEmit`
- commit atômico (semantic) — cada commit deve passar verde

Se algo quebra: **reverter o knob**, não empilhar fixes.

### 5. Define eval up front
Antes de mergear, escrever:
- 1 teste unit (caminho feliz)
- 1 teste integração (com fixtures reais quando possível — ver memory: "integration tests must hit a real database")
- Critério `## Eval` no doc da feature: "feito quando X mensurável"

### 6. Regularize / harden
**Só agora** adicionar: rate limit, error boundary, retry, observabilidade Sentry, i18n keys, RLS extra. Antes não.

## Anti-padrões proibidos

- Começar otimizando antes de baseline rodar
- Adicionar dois knobs no mesmo commit
- "Vou adicionar try/catch só por garantia" sem erro reproduzido
- Caching antes de ter perf measurement
- Abstrações genéricas (factory, strategy) sem 3 callsites reais

## Output esperado quando esta skill ativa

Codex responde com mini-plano:
```
Recipe plan:
1. Data: <fonte de 5-10 exemplos reais>
2. Skeleton: <arquivos a criar com mocks>
3. Overfit: <1 caso a fazer funcionar>
4. Knobs ordenados: [...]
5. Eval: <teste + critério mensurável>
```

E pede confirmação antes de codar.

## Relacionado
- [[surgical-reviewer]] — revisor que valida estes princípios em PR
- [[eval-harness-builder]] — agent que gera os testes do passo 5
- [[andrej-karpathy-skills:karpathy-guidelines]] — guidelines comportamentais base
