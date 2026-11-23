# 🎬 Video Prompt — Knowledge & Workflow

Source of truth for cinematic AI video prompts (with or without dialogue) from a storyboard image, a character reference, or a rough idea. Read this fully before generating a video prompt. Goal: polished, copy-ready, consistent prompts that are strong enough for professional AI video generation.

## Table of contents
1. Flow & dialogue logic
2. Global video rules (hard)
3. Reference use
4. What a video prompt must include
5. Shot timing tables
6. Camera / style / sound libraries
7. Negative rules
8. Templates (no-dialogue · with-dialogue · matching-from-storyboard)
9. Solo self-talk example
10. Output formats (exact)
11. Higgsfield video generation
12. Bulk notes

---

## 1) Flow & dialogue logic

**Intake question (ask this, then wait):**
> 🎬 Do you want a video prompt with dialogue or without dialogue? You can upload a storyboard image or describe the scene.

You must have a real scene / character / storyboard before generating. If the user only picked dialogue/no-dialogue but gave **no scene**, ask:
> 🎬 Describe the scene or upload a storyboard image so I can build the prompt.

- **Without dialogue + scene given** → create the video prompt immediately.
- **With dialogue** → ask once:
  > 🎙️ Who is speaking, and what is the conversation about? You can use 1, 2, or 3 characters.
  Then create the prompt immediately.

**Dialogue completion rule:** treat any understandable answer as enough — do not ask again. Enough examples: "he is alone," "he talks to himself," "2 characters arguing," "they talk about escaping," "make it emotional," "survival dialogue," "the girl warns him," "the monster whispers," "a mother talks to her child," "the chef talks to himself while cooking." If vague, intelligently write short natural dialogue matching the storyboard, character, tone, and scene.
- **Solo** → inner monologue / spoken self-talk.
- **2 characters** → short back-and-forth.
- **3 characters** → very short, clearly labeled lines.

## 2) Global video rules (HARD — never break)

- Always include `No background music.`
- **Character cap: under 2000 characters, target 1800–1950.** Never exceed 2000. If too long, auto-compress while preserving scene quality, motion, style, and important detail.
- **Never** put aspect-ratio language in a video prompt — no `16:9`, `9:16`, `1:1`, `vertical`, `horizontal`, `landscape`, `portrait`, or "aspect ratio" — unless the user explicitly asks. (Aspect ratio belongs only in storyboard/image prompts, or as an MCP `aspect_ratio` parameter.)
- **Without dialogue** → include `No dialogue, no subtitles, no text on screen. No background music.`
- **With dialogue** → include `No subtitles, no text on screen. No background music.`

## 3) Reference use
- **Storyboard image uploaded** → use it as the exact shot structure, timing, framing, and sequence reference. **Do not reinterpret the storyboard as one single scene** — each panel is one separate cinematic shot beat.
- **Character image uploaded** → preserve exact identity, outfit, face, body proportions, props, style.
- **Both** → storyboard = sequence reference; character image = identity reference.

## 4) A video prompt must include
Duration · Reference instructions · Subject · Scene · Style · Rules · Shot sequence · Camera direction · Sound design · Dialogue section (if needed) · Negative rules · `No background music` · No aspect ratio unless explicitly asked.

## 5) Shot timing tables

```
12 seconds / 8 shots
[00:00–00:01.5] [00:01.5–00:03.0] [00:03.0–00:04.5] [00:04.5–00:06.0]
[00:06.0–00:07.5] [00:07.5–00:09.0] [00:09.0–00:10.5] [00:10.5–00:12.0]

15 seconds / 8 shots
[00:00–00:01.8] [00:01.8–00:03.4] [00:03.4–00:05.2] [00:05.2–00:07.0]
[00:07.0–00:08.8] [00:08.8–00:10.6] [00:10.6–00:12.8] [00:12.8–00:15.0]

15 seconds / 10 shots → 1.5 seconds per shot
20 seconds / 10 shots → 2 seconds per shot
```
For other combos, divide duration evenly across shots and format as `[MM:SS.s–MM:SS.s]`. `scripts/bulk_builder.py` has a `timecodes()` helper that reproduces these tables.

## 6) Camera / style / sound libraries

**Camera language:** wide establishing · low-angle tracking · side tracking · crash zoom · slow push-in · aerial pull-back · handheld natural lag · overhead beauty · extreme close-up · hero close-up · macro texture · 360 orbit · dolly-in · whip pan · smooth connected animation between storyboard poses · rack focus · over-the-shoulder · POV · slow-motion hero beat · fast punchy cuts · natural camera drift · tight reaction shot.

**Style language (match the user):** Pixar CGI vivid expressive animation · anime cinematic cel animation · ultra-realistic commercial video · fashion film realism · food commercial macro realism · stylized cartoon comedy · dark magical realism · nostalgic 1990s anime · previs blocking animation · luxury cinematic commercial · horror atmosphere · fantasy film sequence · documentary realism · high-end product commercial · emotional cinematic realism · clay animation · stop-motion inspired · soft colorful stylized animation.

**Natural sound design (realistic only unless voice/dialogue requested):** footsteps · fabric movement · breathing · room tone · wind · fire crackle · steam hiss · knife taps · object impacts · water splashes · crowd murmur · soft ambience · character exhale · mechanical sounds · animal sounds · door creaks · snow crunch · rain taps · distant thunder · wood cracking · glass clink · paper rustle · chair movement · soft hand contact · nervous breathing · whispered voice · spoken self-talk. Always end with `No background music.`

## 7) Negative rules (always include)
No background music · no subtitles · no text on screen · no watermark · no logo · no UI · no aspect ratio unless explicitly asked · no extra characters unless requested · no identity drift · no style drift · no costume drift · no environment drift · no extra story events outside the storyboard/reference · no random camera changes · no inconsistent lighting · no unexplained object changes.

---

## 8) Templates

### 8a) Without dialogue

```text
Create a [duration] cinematic video.

Reference:
Use the uploaded storyboard/image as the exact visual and timing reference if provided.

Subject:
[subject]

Scene:
[scene]

Style:
[style]

Rules:
- Follow the shot order exactly if a storyboard is provided
- Each panel is one separate cinematic shot beat if a storyboard is provided
- Maintain character, outfit, environment, lighting, and prop continuity
- No dialogue
- No subtitles
- No text on screen
- No background music
- Natural sound design only
- Do not mention aspect ratio

Shot Sequence:
[00:00–00:01.5]
SHOT 1 - [title]
[action, camera, emotion, movement]

[00:01.5–00:03.0]
SHOT 2 - [title]
[action, camera, emotion, movement]
[continue until complete]

Camera:
[wide/medium/close-up/overhead/tracking/low angle/hero shot details]

Audio:
Natural sound effects only: [environment sounds, movement sounds, object sounds, breathing, ambience]. No background music.

Negative:
No background music, no subtitles, no text on screen, no watermark, no logo, no UI, no aspect ratio, no extra story events, no extra characters unless requested, no identity drift, no style drift, no costume drift, no environment drift.
```

### 8b) With dialogue

```text
Create a [duration] cinematic video.

Reference:
Use the uploaded storyboard/image as the exact visual and timing reference if provided.

Subject:
[subject]

Scene:
[scene]

Style:
[style]

Rules:
- Follow the shot order exactly if a storyboard is provided
- Each panel is one separate cinematic shot beat if a storyboard is provided
- Maintain character, outfit, environment, lighting, and prop continuity
- Dialogue must be short, natural, and timed to the shots
- No subtitles
- No text on screen
- No background music
- Natural sound design only
- Do not mention aspect ratio

Shot Sequence:
[00:00–00:02]
SHOT 1 - [title]
[action, camera, expression, movement]
Dialogue:
[Character]:
"[line]"

[00:02–00:04]
SHOT 2 - [title]
[action, camera, expression, movement]
Dialogue:
[Character]:
"[line]"
[continue until complete]

Audio:
Clear dialogue, natural room tone, movement sounds, object sounds, atmosphere, and realistic effects. No background music.

Negative:
No background music, no subtitles, no text on screen, no watermark, no logo, no UI, no aspect ratio, no extra characters unless requested, no off-story events, no identity drift, no style drift, no costume drift, no environment drift.
```

### 8c) Matching video prompt from a storyboard

```text
Use the uploaded storyboard image as the exact shot structure, timing, framing, and sequence reference.

Create a [duration] cinematic video that follows the storyboard panel order exactly. Each panel is one separate cinematic shot beat. Do not reinterpret the storyboard as one single scene.

Preserve:
- Same character identity
- Same outfit and proportions
- Same environment
- Same lighting direction
- Same visual style
- Same props and story continuity

Rules:
- Follow the storyboard exactly
- Each panel is one separate cinematic shot beat
- Maintain continuity across every shot
- Do not mention aspect ratio
- No background music

Shot Sequence:
1. [shot 1]
2. [shot 2]
3. [shot 3]
[continue until all shots are complete]

Camera:
Follow the storyboard camera logic exactly. Use smooth connected motion between shots where appropriate.

Style:
[style details]

Audio:
Natural sound design only. No background music. Use realistic environmental sounds, movement sounds, breathing, impacts, footsteps, fabric, atmosphere, or object sounds as needed.

Dialogue:
[No dialogue / or include dialogue per shot]

Negative:
No background music, no subtitles, no text on screen, no watermark, no logo, no UI, no aspect ratio, no extra characters, no story events outside the storyboard, no identity drift, no style drift, no costume drift, no environment drift.
```

## 9) Solo self-talk example
If "he is alone and talks to himself," write short, emotional, natural self-talk:
```
[Character]:
"Stay calm."
[Character]:
"Just one more step."
[Character]:
"I can make it through this."
```

---

## 10) Output formats (exact)

**Without dialogue:**
```
## 🎬 Video Prompt Without Dialogue
​```text
[full video prompt without dialogue]
​```

## 🔁 Next Step
**Do you want to add dialogue, adjust the camera shots, or create a new storyboard from this video prompt?**
```

**With dialogue:**
```
## 🎬 Video Prompt With Dialogue
​```text
[full video prompt with dialogue]
​```

## 🔁 Next Step
**Do you want to adjust the dialogue, make it shorter, or create a new storyboard from this scene?**
```

Before finalizing, verify: contains `No background music`; correct subtitle/dialogue line for the chosen mode; full negatives; no aspect-ratio terms (unless explicitly requested); under 2000 characters.

---

## 11) Higgsfield video generation

Only when the user chose "prompts + video" and the Higgsfield MCP is connected (see `references/higgsfield-mcp.md`). **Always run the credit-confirmation step (estimate → summary → wait for yes) before generating.**

- **Aspect ratio:** pass as the MCP `aspect_ratio` parameter — never inside the prompt text.
- **Duration:** set via the model's duration parameter (the prompt also states the duration in words).
- **References:** pass a storyboard frame / shot as the start image / sequence reference and a character image as the identity reference, per the model's accepted media roles (check `models_explore`).
- Write the prompt first, show it, then confirm credits, then generate. If a call fails, keep the prompt and offer retry or a model switch.

### Model-aware length (don't max out)
The under-2000-char ceiling is a *ceiling*, not a target. Optimize to the model:
- **Seedance:** ~120–200 words. Lead with **subject + action**, then camera, then style. Prefer **positive** phrasing ("natural motion, detailed hands, physically accurate") over long negative lists — keep the required negatives, but don't bloat.
- **Kling 3.0:** length is a control dial — ~30–60 words (simple), 80–150 (standard), 200–350 (complex multi-shot). Structure each beat as camera + subject/action physics + environment/lighting + texture/detail + audio/emotion.

### Two model pipelines
**Seedance** (scenes, products, environments — strong continuity; limited for people):
`Character Sheet → Storyboard → Video Prompt → Seedance`. Use the character/storyboard frame as the identity/sequence reference and optimize the prompt for Seedance.

**Kling 3.0 Omni** (people, dialogue, multi-shot, native audio): often skips the single character sheet in favor of individual cinematic shots:
`Generate standard shots (Production Images) → upload selected shots → Kling-optimized video prompt → Kling output`. Kling generally needs an explicit **start frame** with a reference identity/Element — supply one of the generated shots. Use Kling's native audio + lip-sync for dialogue. Recognize this flow automatically when the user picks Kling or wants human dialogue/multi-shot.

## 12) Bulk notes
For 10 or 100 video prompts, see `references/bulk-generation.md`. Keep Style, Rules, negatives, and `No background music` constant; vary Subject/Scene (and Dialogue if used) per item. `scripts/bulk_builder.py` stamps the right template, auto-generates timecodes, enforces the under-2000 cap, and strips stray aspect-ratio terms.
