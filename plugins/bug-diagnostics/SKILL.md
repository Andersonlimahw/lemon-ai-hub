---
name: bug-diagnostics
description: Loop de diagnóstico para bugs difíceis e regressões de performance. Feedback loop → reprodução → hipóteses → instrumentação → fix + teste → cleanup. Use quando o usuário disser "diagnosticar"/"debugar isso", ou relatar algo quebrado/lançando exceção/falhando/lento.
---

# Bug Diagnostics

Uma disciplina para bugs difíceis. Pule fases apenas quando justificado explicitamente.

> **Créditos**: Baseado em `diagnosing-bugs` por [Matt Pocock](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs). Adaptado para português BR pelo Lemon AI Hub.

Ao explorar o codebase, leia o `CONTEXT.md` (se existir) para construir um modelo mental claro dos módulos relevantes, e consulte ADRs na área que vai mexer.

## Foco

Dois princípios não-negociáveis:

1. **Feedback loop tight** — um sinal de pass/fail que fica vermelho _neste_ bug. Sem loop, debugging é adivinhação.
2. **Determinismo** — mesmo veredito a cada execução. Bugs não-determinísticos devem ter a taxa de reprodução elevada até serem debugáveis.

---

## Fase 1 — Construir o feedback loop

**Esta é a habilidade.** Todo o resto é mecânico. Se você tem um sinal de pass/fail **tight** para o bug — um que fica vermelho _neste_ bug — você vai encontrar a causa; bisection, teste de hipóteses e instrumentação apenas o consomem. Se não tem, nenhuma quantidade de olhar código vai salvar.

Invista esforço desproporcional aqui. **Seja agressivo. Seja criativo. Recuse-se a desistir.**

### Maneiras de construir um loop — tente nesta ordem aproximada

1. **Teste falhando** em qualquer seam que alcance o bug — unit, integration, e2e.
2. **Script curl/HTTP** contra um dev server rodando.
3. **Invocação CLI** com um input fixture, fazendo diff do stdout contra um snapshot conhecido-bom.
4. **Script headless browser** (Playwright/Puppeteer) — drive a UI, asserta em DOM/console/network.
5. **Replay de trace capturado.** Salve uma network request/payload/event log real em disco; faça replay pelo code path isolado.
6. **Harness descartável.** Suba um subset mínimo do sistema (um serviço, deps mockadas) que exercita o code path do bug com uma única chamada de função.
7. **Loop property/fuzz.** Se o bug é "output às vezes errado", rode 1000 inputs aleatórios e procure o failure mode.
8. **Harness de bisection.** Se o bug apareceu entre dois estados conhecidos (commit, dataset, versão), automatize "boot no estado X, verifica, repete" para poder fazer `git bisect run`.
9. **Loop diferencial.** Rode o mesmo input em versão-antiga vs versão-nova (ou duas configs) e faça diff dos outputs.
10. **Script bash HITL.** Último recurso. Se um humano precisa clicar, _orquestre_ com `scripts/hitl-loop.template.sh` para que o loop ainda seja estruturado. Output capturado alimenta de volta para você.

Construa o feedback loop certo, e o bug está 90% resolvido.

### Tighten o loop

Trate o loop como um produto. Assim que tiver _um_ loop, **tighten**:

- Posso deixar mais rápido? (Cache de setup, pular init irrelevante, estreitar escopo do teste.)
- Posso deixar o sinal mais nítido? (Assertar no sintoma específico, não em "não crashou".)
- Posso deixar mais determinístico? (Pinar tempo, seedar RNG, isolar filesystem, congelar network.)

Um loop flaky de 30 segundos é quase tão ruim quanto nenhum loop; um determinístico de 2 segundos é tight — um superpoder de debugging.

### Bugs não-determinísticos

O objetivo não é uma repro limpa, mas sim uma **taxa de reprodução mais alta**. Loope o gatilho 100×, paralelize, adicione stress, estreite janelas de timing, injete sleeps. Um bug 50% flaky é debugável; 1% não é — continue elevando a taxa até ser debugável.

### Quando você genuinamente não consegue construir um loop

Pare e diga explicitamente. Liste o que tentou. Peça ao usuário por: (a) acesso a qualquer ambiente que reproduza, (b) um artifact capturado (HAR file, log dump, core dump, screen recording com timestamps), ou (c) permissão para adicionar instrumentação temporária em produção. **Não** prossiga para hipóteses sem um loop.

### Critério de conclusão — um loop tight que fica vermelho

A Fase 1 está completa quando o loop é **tight** e **red-capable**: você consegue nomear **um comando** — um path de script, uma invocação de teste, um curl — que você **já executou pelo menos uma vez** (cole a invocação e seu output), e que é:

- [ ] **Red-capable** — drive o code path real do bug e asserta o **sintoma exato do usuário**, de forma que possa ficar vermelho neste bug e verde quando corrigido. Não "roda sem erroar" — deve conseguir _pegar este bug específico_.
- [ ] **Determinístico** — mesmo veredito a cada execução (bugs flaky: taxa de reprodução alta e pinada, conforme acima).
- [ ] **Rápido** — segundos, não minutos.
- [ ] **Agent-runnable** — roda sem supervisão; humano no loop apenas via `scripts/hitl-loop.template.sh`.

Se se pegar lendo código para construir uma teoria antes deste comando existir, **pare — pular direto para hipótese é a falha exata que esta skill previne.** Sem comando red-capable, sem Fase 2.

---

## Fase 2 — Reproduzir + minimizar

Rode o loop. Veja ficar vermelho — o bug aparece.

Confirme:

- [ ] O loop produz o failure mode que o **usuário** descreveu — não um failure diferente que acontece de estar próximo. Bug errado = fix errado.
- [ ] O failure é reproduzível em múltiplas execuções (ou, para bugs não-determinísticos, reproduzível em taxa alta o suficiente para debugar).
- [ ] Você capturou o sintoma exato (mensagem de erro, output errado, timing lento) para que fases posteriores possam verificar que o fix realmente resolve.

### Minimizar

Assim que estiver vermelho, encolha a repro para o **menor cenário que ainda fica vermelho**. Corte inputs, callers, config, dados e steps **um de cada vez**, re-rodando o loop após cada corte — mantenha apenas o que é load-bearing para o failure.

Por que importa: uma repro mínima encolhe o espaço de hipóteses na Fase 3 (menos partes móveis para suspeitar) e se torna o teste de regressão limpo na Fase 5.

Completo quando **todo elemento restante é load-bearing** — remover qualquer um deles faz o loop ficar verde.

Não prossiga até ter reproduzido **e** minimizado.

---

## Fase 3 — Hipóteses

Gere **3–5 hipóteses ranqueadas** antes de testar qualquer uma. Geração de hipótese única ancora na primeira ideia plausível.

Cada hipótese deve ser **falsificável**: declare a predição que ela faz.

> Formato: "Se <X> é a causa, então <mudar Y> vai fazer o bug desaparecer / <mudar Z> vai piorar."

Se não consegue declarar a predição, a hipótese é um chute — descarte ou afie.

**Mostre a lista ranqueada ao usuário antes de testar.** Ele costuma ter conhecimento de domínio que re-ranqueia instantaneamente ("acabamos de deployar uma mudança em #3"), ou sabe hipóteses que já descartou. Checkpoint barato, grande economia de tempo. Não bloqueie — prossiga com seu ranking se o usuário estiver AFK.

---

## Fase 4 — Instrumentar

Cada probe deve mapear para uma predição específica da Fase 3. **Mude uma variável por vez.**

Preferência de ferramenta:

1. **Inspeção via debugger/REPL** se o ambiente suporta. Um breakpoint vale por dez logs.
2. **Logs direcionados** nas fronteiras que distinguem hipóteses.
3. Nunca "logar tudo e grep".

**Tagueie cada debug log** com um prefixo único, ex.: `[DEBUG-a4f2]`. Cleanup no final vira um único grep. Logs sem tag sobrevivem; logs tagueados morrem.

**Branch de performance.** Para regressões de performance, logs estão geralmente errados. Em vez disso: estabeleça uma medição baseline (timing harness, `performance.now()`, profiler, query plan), depois faça bisection. Meça primeiro, conserte depois.

---

## Fase 5 — Fix + teste de regressão

Escreva o teste de regressão **antes do fix** — mas apenas se existir um **seam correto** para ele.

Um seam correto é um onde o teste exercita o **padrão real do bug** como ocorre no call site. Se o único seam disponível é raso demais (teste de caller único quando o bug precisa de múltiplos callers, teste unitário que não consegue replicar a chain que disparou o bug), um teste de regressão ali dá falsa confiança.

**Se nenhum seam correto existe, isso em si é o finding.** Anote. A arquitetura do codebase está impedindo o bug de ser travado. Flague para a próxima fase.

Se um seam correto existe:

1. Transforme a repro minimizada em um teste falhando naquele seam.
2. Veja falhar.
3. Aplique o fix.
4. Veja passar.
5. Re-rode o feedback loop da Fase 1 contra o cenário original (não-minimizado).

---

## Fase 6 — Cleanup + post-mortem

Obrigatório antes de declarar concluído:

- [ ] Repro original não reproduz mais (re-rode o loop da Fase 1)
- [ ] Teste de regressão passa (ou ausência de seam está documentada)
- [ ] Toda instrumentação `[DEBUG-...]` removida (`grep` no prefixo)
- [ ] Protótipos descartáveis deletados (ou movidos para local claramente marcado como debug)
- [ ] A hipótese que se mostrou correta está declarada no commit/PR message — para que o próximo debugger aprenda

**Então pergunte: o que teria prevenido este bug?** Se a resposta envolve mudança arquitetural (sem bom seam de teste, callers emaranhados, acoplamento escondido) encaminhe para a skill de melhoria de arquitetura com os specifics. Faça a recomendação **depois** do fix estar pronto, não antes — você tem mais informação agora do que quando começou.
