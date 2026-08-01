---
name: prompts-feedback-loops
description: Ready-to-paste prompts to run continuous validation and feedback loops — API test loops, exploratory browser QA, error-fix loops, metric optimization, and completion verification gates.
---

# Prompts — Loops de feedback e qualidade

Receitas para transformar "acho que funciona" em evidência. Regra de ouro da trilha: **um loop driver por vez** — encadeie loops em sequência, nunca dois donos do mesmo ciclo.

## R1 — Loop de validação de API

**Skills:** `api-test-loop` + `verification-before-completion`
**Quando:** endpoints novos ou alterados; você quer prova via CURL, não opinião.

```text
Rode a skill api-test-loop nos endpoints <lista ou prefixo de rota>.
Valide práticas REST, inputs de borda (nulos, negativos, overflow,
injeção), segurança e formato de saída via CURL. Registre cada
finding em findings.md com severidade e curl de reprodução. Aplique
fixes cirúrgicos e re-valide até zerar os CRITICAL. Feche com
verification-before-completion.
Sucesso: findings.md com todos os CRITICAL fechados, cada um com
o curl de prova antes/depois.
```

## R2 — QA exploratório no browser

**Skills:** `chrome-qa-loop`
**Quando:** app web vivo precisa de olhos exploratórios, não de suíte E2E.

```text
Rode chrome-qa-loop no app <url>, usando o manifesto de telas
<path/config>. Explore cada tela com o contexto do doc, gere um
report markdown por finding (severidade, passos de reprodução,
evidência). Não corrija nada ainda — só triagem.
Sucesso: um report por finding, triável sem abrir o app; zero
findings duplicados.
```

## R3 — Loop de correção de erro

**Skills:** `error-fixer-loop`
**Quando:** build/teste/typecheck quebrou e você quer fix + regra anti-regressão, não só band-aid.

```text
Capturei esta falha: <cole stack/erro exato>.
Rode o error-fixer-loop: investigar causa raiz → fix mínimo →
verificar com o mesmo comando que falhou → persistir a regra
anti-regressão do padrão de erro.
Sucesso: comando de verificação verde + regra persistida; o diff
toca só o necessário.
```

## R4 — Loop de otimização de métrica

**Skills:** `karpathy-loop`
**Quando:** existe uma métrica objetiva (latência, bundle, tokens, cobertura) e você quer ciclos autônomos de melhoria.

```text
Rode karpathy-loop com alvo: melhorar <métrica> de <baseline> para
<meta> em <arquivo/área>. Cada ciclo: hipótese → mudança mínima →
medir com <comando de medição> → manter ou reverter. Pare em <N>
ciclos ou na meta.
Sucesso: métrica na meta (ou melhor resultado após N ciclos) com
log de cada ciclo e medição reprodutível.
```

## Encadeamento recomendado

`chrome-qa-loop` (achar) → `bug-diagnostics` (diagnosticar o finding cabeludo) → `error-fixer-loop` (fixar com regra). Sequência, nunca simultâneo — cada etapa entrega artefato para a próxima.
