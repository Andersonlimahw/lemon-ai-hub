# Teaching Workspace

Stateful teaching plugin — turns the current directory into a living learning workspace that persists across sessions.

Based on [teach](https://github.com/mattpocock/skills/tree/master/skills/productivity/teach) by **Matt Pocock**.

## What it does

When invoked, the agent treats your directory as a teaching workspace and progressively builds:

```
.
├── MISSION.md              # Why you're learning this
├── RESOURCES.md            # High-trust sources & communities
├── NOTES.md                # Preferences & scratchpad
├── lessons/                # *.html — self-contained interactive lessons
├── reference/              # *.html — cheat sheets, glossaries, syntax
├── learning-records/       # *.md — ADR-like records of what's been learned
└── assets/                 # Reusable components (stylesheets, widgets)
```

## Philosophy

```
knowledge  →  skills  →  wisdom
```

- **Knowledge** from curated, high-trust resources (never parametric guesses).
- **Skills** through interactive lessons with tight feedback loops.
- **Wisdom** by delegating to real-world communities.

Lessons target the user's **zone of proximal development** — challenging just enough. Storage strength (long-term retention) is preferred over fluency (illusory mastery) via retrieval practice, spacing, and interleaving.

## Install

```bash
/add-plugin teaching-workspace
```

## Usage

```
/teaching-workspace O que você gostaria de aprender?
```

The first session grounds the mission and populates `RESOURCES.md`. Subsequent sessions read the workspace state and continue from the user's zone of proximal development.

## License

MIT. Credit: Matt Pocock.
