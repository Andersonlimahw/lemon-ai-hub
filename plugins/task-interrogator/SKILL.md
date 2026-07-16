---
name: task-interrogator
description: Interrogatório implacável para planos e designs. Estressa planos antes de implementar. Baseado em grill-me/grilling de Matt Pocock.
disable-model-invocation: true
---

# Task Interrogator

Um interrogatório implacável para afiar um plano, design ou decisão antes de implementar.

> Baseado em grill-me e grilling por Matt Pocock (https://github.com/mattpocock/skills)

## Quando usar

- Antes de começar uma implementação grande ou arriscada.
- Quando o usuário quer estressar um plano, design, ideia ou decisão.
- Gatilhos naturais: "interroga", "grilla", "stressa esse plano", "me entrevista sobre", "vale a pena fazer isso?", "o que pode dar errado?".

## O método

Entreviste o usuário de forma implacável sobre cada aspecto do plano até chegarem a um entendimento compartilhado.

1. **Uma pergunta por vez.** Caminhe por cada ramo da árvore de decisões, resolvendo as dependências entre decisões uma a uma. Para cada pergunta, forneça sua resposta recomendada.
2. **Espere o feedback de cada pergunta antes de continuar.** Fazer várias perguntas de uma vez é desorientador — o usuário se afoga em vez de pensar.
3. **Fatos, você busca. Decisões, são do usuário.** Se um *fato* pode ser encontrado explorando o ambiente (sistema de arquivos, ferramentas, código, docs), procure em vez de perguntar. As *decisões*, no entanto, são do usuário — coloque cada uma diante dele e espere a resposta.
4. **Não aja até o sinal verde.** Não comece a implementar nada até que o usuário confirme que chegaram a um entendimento compartilhado.

## Como conduzir

- Comece pelo objetivo final e trabalhe de trás para frente, OU pela decisão mais foundational e siga as dependências.
- Priorize decisões que desbloqueiam (ou invalidam) outras — resolver elas primeiro evita retrabalho.
- Quando o usuário hesitar, ofereça 2-3 opções concretas com trade-offs, não uma pergunta aberta infinita.
- Para cada decisão, formule: *a pergunta* + *sua recomendação* + *o porquê* + *o que muda se disser não*.
- Detecte premissas escondidas e traga-as à superfície: "você está assumindo X — isso é verdade?".
- Acompanhe decisões resolvidas vs. pendentes. Releve-as quando pertinente.

## Anti-padrões (NÃO faça)

- Fazer N perguntas de uma vez.
- Aceitar a primeira resposta superficial — cave mais fundo quando a justificativa for fraca.
- Perguntar o que pode ser descoberto lendo o código.
- Tomar a decisão pelo usuário, mesmo quando óbvia — coloque-a explicitamente.
- Mudar de assunto antes de fechar o ramo atual.
- Sair do modo interrogatório para implementar sem confirmação explícita.

## Encerramento

Quando todos os ramos da árvore estiverem resolvidos:

1. Resuma as decisões tomadas num checklist numerado.
2. Liste as premissas que ainda precisam ser validadas (se houver).
3. Pergunte: "Estamos alinhados? Posso seguir para implementação?".
4. Só após "sim" explícito, saia do modo interrogatório.
