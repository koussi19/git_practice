# 🎞️ Storyboard — Knowledge & Workflow

Source of truth for cinematic storyboard prompts (AI image tools) and the automatic matching video prompt. Read this fully before generating a storyboard. Goal: clean, cinematic storyboard prompts in any style with strong shot structure, duration, timing, camera logic, and continuity.

## Table of contents
1. Flow (intake → output → follow-up)
2. What a storyboard must include
3. Best shot structures (8 / 10 / 12)
4. Camera grammar & continuity rules
5. Storyboard layout types
6. Reference handling
7. The prompt template
8. Automatic matching video prompt rule
9. Output format (exact)
10. Higgsfield image generation for storyboards
11. Bulk notes

---

## 1) Flow

**Intake question (ask this, then wait):**
> 🎞️ What is the video idea, duration, number of shots, style, and will you upload or describe a character?

If the user doesn't know duration / shot count, suggest:
- 8 shots = 12 seconds
- 10 shots = 15 seconds
- 12 shots = 15–20 seconds

When the user gives a story idea only, **automatically create the full panel sequence** — do not wait for beat-by-beat instructions. After producing the storyboard (section 9), ask the follow-up:
> **Do you want the matching video prompt with dialogue or without dialogue?**

---

## 2) A storyboard must include
Project title · Duration · Number of panels · Aspect ratio 16:9 · Visual style · Character or subject · Environment · Panel layout · Shot titles · Timing hints · Camera notes · Action notes · Continuity rules · Negative rules.

## 3) Best shot structures

**8-shot / 12s:** 1) Opener / establishing · 2) First action impact · 3) Process or escalation · 4) Texture or detail close-up · 5) Main transformation or reveal · 6) Peak motion or conflict · 7) Final build / emotional setup · 8) Hero ending / payoff.

**10-shot / 15s:** 1) Establish world · 2) Introduce character · 3) Trigger action · 4) First escalation · 5) Detail close-up · 6) Motion peak · 7) Transformation or twist · 8) Emotional reaction · 9) Hero reveal · 10) Final payoff.

**12-shot / 15–20s:** 1) Establishing beat · 2) Character intention · 3) First action · 4) Detail action · 5) Process beat · 6) Environmental shift · 7) Escalation · 8) Peak action · 9) Slow-motion / hero beat · 10) Final detail · 11) Presentation/reveal · 12) Emotional payoff.

## 4) Camera grammar & continuity

**Camera grammar (each panel must look visually different):** wide establishing · medium · close-up · extreme close-up · overhead · low-angle · side tracking · handheld natural lag · push-in · pull-back · whip pan · hero shot · POV · texture macro · reaction close-up.

**Continuity — preserve:** same character identity, outfit, proportions, props, environment logic, lighting direction, visual style, emotional progression. **Avoid:** identity drift, costume drift, extra characters, random new locations, repeated camera angles, crowded text inside panels, messy panel layout.

## 5) Storyboard layout types
1. **Clean infographic** — white background, black borders, bold titles, numbered panels, footer notes.
2. **Professional production** — cream paper, pencil/ink notes, red camera boxes, blue motion arrows, timing notes.
3. **Previs** — low-detail figures, simple shapes, camera arrows, motion clarity, blocking-first.
4. **Cinematic commercial** — realistic shots, luxury lighting, emotional progression, shallow depth of field.
5. **Anime production board** — handwritten notes, manga motion lines, sound effects, timing notes, dramatic angles.

## 6) Reference handling
- **Character image uploaded** → use as Reference Image 1; preserve exact identity in all panels.
- **Story idea only** → auto-build the full panel sequence.

---

## 7) Prompt template

```text
Create a professional cinematic storyboard sheet.

Project:
[title]

Duration:
[duration]

Panels:
[number of shots]

Aspect Ratio:
16:9

Style:
[visual style]

Character/Subject:
[character or subject description]

Environment:
[location/world]

Storyboard Layout:
Clean widescreen production storyboard sheet with numbered panels, clear shot titles, camera notes, action notes, timing hints, and strong visual flow. Use a professional layout with readable panel structure.

Continuity Rules:
- Same character identity throughout
- Same outfit, proportions, props, and style throughout
- Same environment logic and lighting direction throughout
- Each panel must be a distinct cinematic shot
- Strong variety in camera angles: wide, medium, close-up, extreme close-up, overhead, low angle, tracking, hero shot where useful

Shot Sequence:
1. [shot title] — [action, camera, timing, emotion]
2. [shot title] — [action, camera, timing, emotion]
3. [shot title] — [action, camera, timing, emotion]
[continue until all shots are complete]

Visual Direction:
Use clear cinematic composition, readable silhouettes, emotional progression, strong pacing, and dynamic motion. Prioritize shot grammar, continuity, and story clarity.

Footer Notes:
Include camera tips, timing flow, style notes, and continuity reminders.

Negative:
No watermark, no logo, no random text inside panels, no inconsistent costume, no identity drift, no messy layout, no extra characters unless requested.
```

Build the Shot Sequence from the matching structure in section 3 (8/10/12), adapted to the user's story. Each panel = a distinct cinematic shot with varied camera grammar.

---

## 8) Automatic matching video prompt rule

After every storyboard prompt, **also create a matching video prompt unless the user says not to** (offer dialogue vs no-dialogue via the follow-up). Build it per `references/video-prompt.md`, using the storyboard as the exact shot/timing/sequence reference. The matching video prompt must say: `Use the storyboard image as the exact shot structure, timing, framing, and sequence reference.` and include duration, shot-by-shot sequence, camera instructions, style, natural sound design only, `No background music`, the dialogue / no-dialogue rule, and negatives.

> Note: the storyboard prompt itself uses `16:9` (image prompts may). The matching **video** prompt must **not** contain any aspect-ratio language unless the user explicitly asks — pass aspect ratio as an MCP parameter instead.

---

## 9) Output format (exact)

```
## 🎞️ Storyboard Prompt
**Use Reference Image 1 if uploaded.**
​```text
[professional storyboard prompt from the template]
​```

## 🔁 Next Step
**Do you want the matching video prompt with dialogue or without dialogue?**
```

If the user already asked for the matching video prompt, output it right after the storyboard (its own `## 🎬 Video Prompt …` block) per `references/video-prompt.md`.

---

## 10) Higgsfield image generation for storyboards

Only when the user chose "prompts + images" and the Higgsfield MCP is connected (see `references/higgsfield-mcp.md`).

- **Recommended model:** **Nano Banana Pro** — strongest for multi-panel layouts, panel borders, shot titles, and small readable text/callouts.
- **Aspect ratio:** pass `16:9` as the tool **parameter** for a widescreen board.
- **Character continuity:** if a character reference was uploaded, pass it so every panel keeps the same identity.
- Write the storyboard prompt first, show it, then generate the board. Offer to proceed to the matching video prompt and (option C) to render the video.

## 11) Bulk notes
For 10 or 100 storyboards, see `references/bulk-generation.md`. Hold Style, Aspect Ratio (16:9), and Continuity Rules constant across the batch; vary Project/Story/Environment per item. Each storyboard can carry its matching video prompt if requested.
