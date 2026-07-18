---
name: maestri-portal
description: Use a browser portal on the Maestri canvas to navigate the web, interact with pages, fill forms, and inspect content. Use when the user asks to browse a URL, test a web UI, or interact with a website.
user-invocable: true
---

# Maestri Portal Browser Automation

Portals are embedded browser nodes on the Maestri canvas. You can automate them to navigate pages, click elements, fill forms, take screenshots, and inspect the DOM — all without requiring window focus.

Portal name is always required. Run `maestri list` to see connected portal names.

## Creating a portal

`maestri portal create URL ["Name"] [--size WxH]` — create a new portal on the canvas, open it at the given URL, and automatically connect it to your terminal. The portal appears to the right of your terminal. An optional name can be provided; if omitted it defaults to "Portal". Pass `--size WxH` to open at a specific viewport (handy for responsive QA, e.g. `--size 390x844`); otherwise it opens at a desktop size.

```
maestri portal create http://localhost:3000
maestri portal create https://example.com "Docs"
maestri portal create http://localhost:3000 "Mobile" --size 390x844
```

After creating, run `maestri list` to confirm the portal name, then use it with all other portal commands.

## Editing a portal

`maestri portal edit "Portal" --url URL` — point a connected portal at a new URL.

```
maestri portal edit "Preview" --url http://localhost:5173
```

## Closing a portal

`maestri portal close "Portal"` — remove a connected portal from the canvas.

**Destructive. Only run when the user explicitly asks you to close the portal.** Never close a portal on your own initiative, even to clean up after finishing a task.

```
maestri portal close "Preview"
```

## Snapshot & Selectors

The **snapshot** command is the most important — it returns an accessibility tree with **refs** (`@e1`, `@e2`...) that you can use as selectors for all other commands:

```
maestri portal snapshot "Portal"
```

Returns something like:
```
viewport: 780x520  url: https://example.com  title: Example
@e1 a "Home" [10,5 60x20]
@e2 input type=text "Search" [200,50 300x32] *focused*
@e3 button "Submit" [510,50 80x32]
@e4 a "Sign In" href=https://example.com/login [700,5 60x20]
```

**Selectors** — all commands that take a selector accept:
- `@e3` — ref from snapshot (most reliable)
- `#submit` — CSS selector
- `350,200` — x,y coordinates

## Commands

### Navigation
- `maestri portal navigate "Portal" "url"` — go to URL
- `maestri portal info "Portal"` — get current URL, title, viewport size
- `maestri portal screenshot "Portal"` — capture screenshot (returns temp file path)

### Interaction
- `maestri portal click "Portal" @e3` — click element
- `maestri portal fill "Portal" @e2 "test@example.com"` — clear input and set value
- `maestri portal type "Portal" @e2 "hello"` — append text to input (or type into focused element: `type "Portal" "hello"`)
- `maestri portal key "Portal" "Enter"` — press key (Enter, Tab, Escape, Backspace, ArrowUp/Down/Left/Right, Space)
- `maestri portal key "Portal" "ctrl+a"` — key with modifiers (ctrl, cmd, shift, alt — e.g. `ctrl+a`, `cmd+c`, `shift+tab`)
- `maestri portal selectall "Portal"` — select all text in focused element (or specify selector: `selectall "Portal" @e2`)
- `maestri portal clear "Portal"` — clear focused input (or specify selector: `clear "Portal" @e2`)
- `maestri portal hover "Portal" @e3` — hover over element
- `maestri portal focus "Portal" @e2` — focus element
- `maestri portal select "Portal" @e5 "Option Text"` — select dropdown option
- `maestri portal check "Portal" @e6` / `uncheck` — toggle checkbox

### Scrolling
- `maestri portal scroll "Portal" down 300` — scroll down 300px from viewport center (up/down/left/right)
- `maestri portal scroll "Portal" down 300 400,250` — scroll the container under point (400,250)
- `maestri portal scroll "Portal" down 300 @e5` — scroll the container under element @e5
- `maestri portal scrollintoview "Portal" @e10` — scroll element into view

### Reading
- `maestri portal snapshot "Portal"` — accessibility tree with refs (best for understanding page structure)
- `maestri portal text "Portal" @e1` — get text content of element
- `maestri portal html "Portal"` — get full page HTML
- `maestri portal evaluate "Portal" "document.title"` — evaluate JavaScript

### Console
- `maestri portal logs-start "Portal"` — start capturing console output (call once after navigate)
- `maestri portal logs "Portal"` — get captured console logs (clears buffer)

### Responsive testing
Portals open at a desktop size (~1900px wide). Resize one to test responsive breakpoints without dragging the node by hand.

- `maestri portal resize "Portal" 390 844` — set the CSS viewport (`window.innerWidth`/`innerHeight`) to exactly W×H px. Returns the achieved viewport (e.g. `viewport: 390x844`). To emulate a device, pass its logical dimensions: iPhone SE `375 667`, iPhone 12 Pro `390 844`, Pixel 7 `412 915`, iPad Mini `768 1024`. Confirm with `info` or re-run `snapshot` (its header prints the viewport).
- `maestri portal ua "Portal" ios` — switch the user agent to a curated preset and reload, so sites that sniff the UA serve their mobile (or other) variant. Pair with `resize` for true device emulation (e.g. `resize 390 844` + `ua ios`). Presets: `ios`, `android`, `firefox-android`, `edge-android`, `chrome`, `firefox`, `edge`, `desktop` (clears the override). Omit the argument to read the current UA and list the presets.

## Recommended Workflow

1. `maestri portal snapshot "Portal"` — understand the page structure and get refs
2. Use refs to interact: `click @e3`, `fill @e2 "value"`, `key "Enter"`
3. `maestri portal snapshot "Portal"` again to verify result
4. If refs are stale (page changed), run snapshot again to get fresh refs

Use `screenshot` when you need to see the visual layout. Use `snapshot` when you need to understand interactive elements. Prefer `snapshot` + refs over `screenshot` + coordinates — refs are more accurate.

## Popups

If a page opens a popup (e.g. an OAuth login), it appears in `maestri list` as a new portal named `[Parent] #2`. Target it by name like any other portal. Popups close automatically when the site is done with them.