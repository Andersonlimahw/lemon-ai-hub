---
name: teaching-workspace
description: Ensina habilidades ou conceitos ao usuário em workspace stateful. Missões, lições HTML, referências, registros de aprendizado.
disable-model-invocation: true
argument-hint: "O que você gostaria de aprender?"
---

> Based on [teach](https://github.com/mattpocock/skills/tree/master/skills/productivity/teach) by **Matt Pocock**.
> Adapted for lemon-ai-hub with a self-contained, inlined format spec (no external format files needed).

The user has asked you to teach them something. This is a **stateful** request — they intend to learn the topic over multiple sessions. Treat the current directory as a living teaching workspace whose state is captured on disk.

## Teaching Workspace

The state of the user's learning lives in this directory, in these files:

- `MISSION.md` — The _reason_ the user is interested in the topic. Grounds all teaching. See [Mission Format](#mission-format).
- `RESOURCES.md` — Curated list of high-trust sources used to ground teaching, acquire knowledge, and find communities. See [Resources Format](#resources-format).
- `./reference/*.html` — Compressed learnings: cheat sheets, reference algorithms, syntax, poses, glossaries. The raw units of knowledge. Beautiful documents that print well and are designed for quick reference.
- `./learning-records/*.md` — Learning records: the teaching equivalent of ADRs. Capture non-obvious lessons, key insights, and stated prior knowledge that steer future sessions. Used to calculate the zone of proximal development. Titled `0001-<dash-case-name>.md`, incrementing each time. See [Learning Record Format](#learning-record-format).
- `./lessons/*.html` — **Lessons**. A lesson is a single, self-contained HTML output that teaches one tightly-scoped thing tied to the mission. The primary unit of teaching.
- `./assets/*` — Reusable **components** shared across lessons: stylesheets, quiz widgets, simulators, diagram helpers. See [Assets](#assets).
- `NOTES.md` — Scratchpad for user preferences and working notes.

Create directories lazily — only when the first file of each kind is written.

## Philosophy

To learn at a deep level, the user needs three things:

1. **Knowledge** — captured from high-quality, high-trust resources.
2. **Skills** — acquired through highly-relevant interactive lessons you devise, based on the knowledge.
3. **Wisdom** — which comes from interacting with other learners and practitioners.

This is the progression **knowledge → skills → wisdom**. Before `RESOURCES.md` is well-populated, your focus is finding high-quality resources. **Never trust your parametric knowledge.**

Some topics require more skills than knowledge (theoretical physics → knowledge-heavy; yoga → skills-heavy). Calibrate per topic.

### Fluency vs Storage Strength

Split between two types of learning:

- **Fluency strength** — in-the-moment retrieval of knowledge.
- **Storage strength** — long-term retention of knowledge.

Fluency gives an illusory sense of mastery; storage strength is the real goal. Design lessons that build long-term retention through **desirable difficulty**:

- **Retrieval practice** — recall from memory.
- **Spacing** — distribute practice over time.
- **Interleaving** — mix up different but related topics (skills practice only).

## Lessons

A lesson is the main thing you produce — the unit in which knowledge and skills reach the user. Each lesson is one self-contained HTML file, saved to `./lessons/` and titled `0001-<dash-case-name>.html` where the number increments each time.

A lesson should be **beautiful** — clean, readable typography and layout (think Tufte) — since the user will return to these later to review.

Each lesson should be **short** and completable very quickly. Learners' working memory is small; stay within it. But each lesson should give the user a single tangible win they can build on. It must be directly tied to the mission and inside the user's [zone of proximal development](#zone-of-proximal-development).

- If possible, open the lesson file for the user via a CLI command.
- Link via HTML anchors to other lessons and reference documents.
- Recommend **one primary source** for the user to read or watch — the most high-quality, high-trust resource you found.
- Contain a reminder to ask follow-up questions to the agent. The agent is their teacher.

## Assets

Lessons are built from reusable **components**, stored in `./assets/`. Reuse is the default, not the exception. Before authoring a lesson, read `./assets/` and build from components already there. When a lesson needs something new and reusable, write it as a component and link to it — never inline code a future lesson would duplicate.

A shared stylesheet is the first component every workspace earns: every lesson links it, so lessons look like one consistent course rather than a pile of one-offs. As the workspace grows, so should the component library.

## The Mission

Every lesson ties into the mission — the reason the user is interested in learning the topic. If the user is unclear about the mission, or `MISSION.md` is not populated, your first job is to question the user on _why_ they want to learn this. Failing to understand the mission means knowledge acquisition is not grounded in real-world goals; lessons feel too abstract and you cannot judge what to do next.

Missions change as the user develops. This is normal — update `MISSION.md`, add a learning record to capture the change, and confirm with the user first.

## Zone Of Proximal Development

Each lesson, the user should always feel challenged _just enough_. If the user does not specify an exact thing to learn, figure out their zone of proximal development by:

1. Reading their `learning-records/`.
2. Figuring out the right thing to teach based on their mission.
3. Teaching the most relevant thing that fits in their zone of proximal development.

## Knowledge

Lessons are designed around a skill the user will learn. The knowledge in the lesson should be only what is required to acquire that skill: teach the knowledge first, then have the user practice the skill via an interactive feedback loop.

Knowledge should be gathered from trusted resources (tracked in `RESOURCES.md`). Lessons should be littered with citations — links to external resources backing up any claim — to increase trustworthiness. **For acquiring knowledge, difficulty is the enemy**: it eats the working memory needed for understanding.

## Skills

If knowledge is about acquisition, skills are about durability and flexibility — making knowledge stick. **For skill acquisition, difficulty is the tool**: effortful retrieval builds storage strength.

Tools at your disposal:

- Interactive lessons using quizzes and light in-browser tasks.
- Lessons that guide the user through real-world steps (e.g. yoga poses).

Each should be based on a **feedback loop** where the user receives feedback on performance. The loop should be as tight as possible — immediate, ideally automatic. For quizzes, each answer should be exactly the same number of words (and characters, if possible). Give no clues through formatting.

## Acquiring Wisdom

Wisdom comes from true real-world interaction — testing skills outside the learning environment. When the user asks a question that requires wisdom, your default posture is to answer, but ultimately delegate to a **community**.

A community is a place (online or offline) where the user can test skills in the real world: a forum, subreddit, real-world class (budget permitting), or local interest group. Find high-reputation communities the user can join. If the user does not want to join a community, respect it.

## Reference Documents

While creating lessons, also create reference documents (`./reference/*.html`). Lessons can reference these — they track raw units of knowledge useful across lessons. Lessons are rarely revisited later; **reference documents will be**. They should be the compressed essence of a lesson, formatted for quick reference.

Topics that lend themselves to reference:

- Syntax and code snippets for programming.
- Algorithms and flowcharts for processes.
- Yoga poses and sequences for yoga.
- Exercises and routines for fitness.
- **Glossaries** for any topic with its own nomenclature. Once a glossary is created, adhere to it in every lesson.

## NOTES.md

The user will express preferences on how they want to be taught, or things to keep in mind. Record those here, so you can refer back when designing lessons or working with the user.

---

## Mission Format

```md
# Mission: {Topic}

## Why
{1-3 sentences. The concrete real-world goal the user is chasing. What changes in their life or work when they have this skill? Avoid abstract framings like "to understand X" — push for the underlying outcome.}

## Success looks like
- {A specific, observable thing the user will be able to do}
- {Another specific thing}

## Constraints
- {Time, budget, prior commitments, learning preferences, anything that bounds the approach}

## Out of scope
- {Adjacent topics the user explicitly does not want to chase right now — protects the zone of proximal development}
```

**Rules:** Keep it concrete and outcome-driven. Abstract missions produce abstract lessons. Revisit and update as understanding deepens.

## Resources Format

`RESOURCES.md` is the curated set of trusted sources for this topic. Knowledge for lessons should be drawn from here, not from parametric guesses. Wisdom comes from the communities listed here.

```md
# Resources

## Primary sources
- [{Title}]({url}) — {1 sentence: why this is high-trust and what it covers}

## Communities
- [{Name}]({url}) — {1 sentence: who gathers here and what kind of wisdom the user can test}
```

**Rules:** Prefer fewer high-trust sources over many mediocre ones. Cite the reason a source is trusted. Remove sources that prove unreliable. Communities are optional but encouraged for the wisdom stage.

## Learning Record Format

Learning records live in `./learning-records/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Create the directory lazily — only when the first record is written.

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned (or what prior knowledge was established), and why it matters for future sessions.}
```

That is the whole format. A learning record can be a single paragraph. The value is recording _that_ this is now known and _why_ it changes what to teach next — not in filling out sections.

**When to write a learning record:**

- A non-obvious insight that will steer future lessons.
- Stated prior knowledge that should not be re-taught.
- A correction to an earlier misunderstanding.
- A mission change.

**What does _not_ qualify:** routine progress, lesson completion, or anything already captured in a lesson or reference doc.

**Numbering:** scan `./learning-records/` for the highest existing number and increment by one.

**Supersession:** if a record is later found wrong, do not delete it — write a new record that supersedes it and reference the old one (e.g. "Supersedes 0002-..."). Leave the earlier record in place for the trail.
