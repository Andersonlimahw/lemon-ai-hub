---
name: prompts-mobile-release
description: Ready-to-paste prompts for mobile release — App Store and Google Play go/no-go audits, App Store Connect automation, Play Console API, store listing optimization, and macOS/SwiftUI validation loops.
---

# Prompts — Mobile & Release

Receitas para tirar app da máquina e colocar na loja com decisão auditável. Os release agents decidem GO/NO_GO — nunca submetem nem pagam sem aprovação humana.

## R1 — Go/No-Go iOS

**Skills:** `apple-store-release-agent`
**Quando:** build Expo/RN iOS candidato a release; você quer auditoria antes de apertar submit.

```text
Rode apple-store-release-agent no app <app>: audite build iOS,
metadata da App Store, App Privacy, TestFlight, IAP/RevenueCat,
paridade i18n, screenshots e review notes.
Sucesso: decisão GO / GO_WITH_WARNINGS / NO_GO com cada bloqueio
listado, acionável e com dono; nada submetido sem minha aprovação.
```

## R2 — Go/No-Go Android + automação Play

**Skills:** `google-play-release-agent` + `google-play-developer-api`
**Quando:** release Android; tracks, staged rollout e listing via API.

```text
Rode google-play-release-agent no app <app> para o go/no-go do
release <versão>. Onde couber automação (upload para track
<internal/closed/production>, rollout <X>%), use
google-play-developer-api e me mostre os passos antes de executar.
Sucesso: decisão auditável + plano de rollout por track; nenhuma
ação irreversível sem confirmação.
```

## R3 — Automação App Store Connect

**Skills:** `app-store-connect-api`
**Quando:** tarefa repetitiva no App Store Connect: TestFlight, IAP, provisioning, metadata, relatórios.

```text
Automatize com app-store-connect-api: <tarefa — ex.: distribuir
build <n> para o grupo TestFlight <grupo>, criar IAP <produto>,
baixar relatório de vendas <período>>.
Sucesso: operação executada com resposta da API como evidência;
credenciais nunca em log ou código.
```

## R4 — Listing que converte

**Skills:** `aso`
**Quando:** app no ar mas instalações fracas — auditar a listing antes de comprar tráfego.

```text
Audite com aso a listing de <app> (<URL App Store/Play>): keywords,
título/subtítulo, screenshots, conversão vs concorrentes <apps>.
Sucesso: lista priorizada de mudanças na listing com hipótese de
impacto cada; textos prontos dentro dos limites de caracteres.
```

## Veja também

- `vercel-react-native-skills` — performance RN/Expo antes do release (trilha [prompts-vercel-react](../prompts-vercel-react/SKILL.md)).
- `computer-use-swiftui-loop` — loop de validação visual para apps macOS/SwiftUI (Computer Use, exclusivo do app Codex).
- `imagegen-frontend-mobile` — gerar screenshots/artes de listing.
