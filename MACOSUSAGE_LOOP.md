Use a skill `computer-use-swiftui-loop` neste repo:

`/Users/andersonlimadev/Projects/IA/lemon-code-project/lemon-code-app`

Objetivo: rodar o loop de validação visual do app macOS `dev.andersonlima.lemoncodeapp` com Computer Use, seguindo os arquivos já criados:

- `.agents/skills/computer-use-swiftui-loop/SKILL.md`
- `.ai/agents/computer-use-swiftui-validator.md`
- `.ai/agents/computer-use-fix-implementer.md`
- `docs/test-plans/computer-use-loop/loop.md`
- `docs/test-plans/computer-use-loop/findings.md`
- `docs/plans/specs/swiftui-computer-use-validation-loop.spec.md`
- `docs/evals/swiftui-computer-use-validation-loop.json`

Regras:
- Use `rtk` em todo comando shell.
- Antes de editar, capture o app com Computer Use.
- Navegue apenas por ações seguras.
- Não clique em `Run`, `Assign`, `Start`, `Install`, `Remove`, `Delete`, `Discard`, `Commit`, `Push` ou `PR` sem confirmação explícita.
- Para cada problema encontrado, salve primeiro em `docs/test-plans/computer-use-loop/findings.md`.
- Depois implemente apenas fixes pequenos em Views SwiftUI ou Stores de UI diretamente ligados ao finding.
- Após cada fix rode:
  - `rtk swift build`
  - `rtk swift test --filter ViewCompileCanaryTests`
  - teste específico se houver Store/ViewModel afetado
- Reabra/revalide com Computer Use e atualize o finding como `fixed`.
- Ao final rode `rtk swift test`, `rtk git diff --check`, valide JSON dos evals, e entregue resumo com arquivos tocados e findings corrigidos.

Comece abrindo `docs/test-plans/computer-use-loop/loop.md` e `docs/test-plans/computer-use-loop/findings.md`, depois capture o estado atual do app com Computer Use.