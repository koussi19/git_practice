# 🖼️ Production Images — standalone cinematic shots

## What this mode is
Standalone, production-quality cinematic **images** — not storyboard panels. Each output is a finished, single-scene still suitable for: video creation (first/last frames, references), marketing, social media, thumbnails, and scene generation. Users typically ask for **10 / 50 / 100** shots from a character and/or a story.

The defining difference from Storyboard mode: a storyboard is *one sheet with numbered panels describing a sequence*; production images are *individual, fully-rendered shots*, one prompt (and one image) per shot.

## Flow
1. Ask the intake question (below) and **wait**.
2. Read this file. If generation is requested, also read `higgsfield-mcp.md` for the **credit-confirmation step** and reference-upload flow.
3. If a **character sheet** and/or **storyboard** is uploaded or already exists, use it as the visual reference (identity, wardrobe, look, shot order). Ask reuse vs regenerate if they already have one.
4. Produce the shot list → one copy-ready prompt per shot (inline for small counts; via `scripts/bulk_builder.py` for 50/100).
5. End with one next-step question (usually: turn selected shots into a video prompt).

## Intake question
```text
🖼️ What scene(s) do you want, how many shots (10 / 50 / 100), and what's the style?
Upload a character sheet and/or storyboard to lock identity and look (optional but recommended).
```
Never invent the subject or scene from a bare mode pick — ask first.

## Must include in every production-image prompt
- **Subject / character** — pulled from the character sheet if provided (identity, age, wardrobe, distinguishing features), otherwise from the description.
- **Action / pose / moment** — one clear beat per image.
- **Setting / environment** — specific location, time of day.
- **Camera** — shot size (wide / medium / close / macro), angle, lens feel (e.g. 35mm, f/1.8 shallow depth of field).
- **Lighting & mood** — direction, quality, color.
- **Style / grade** — the requested visual style and color treatment, kept consistent across the whole set.
- **Aspect ratio** — allowed here (images). Default 16:9 for cinematic stills unless told otherwise; pass as the tool `aspect_ratio` parameter when generating.
- **Quality cues** — ultra-detailed, photoreal (or the chosen style), sharp focus.

## Shot variety (so a set of 100 isn't 100 near-duplicates)
Rotate deliberately across the set:
- **Shot sizes:** extreme wide, wide, medium, medium close-up, close-up, macro/detail.
- **Angles:** eye level, low, high, over-the-shoulder, profile, three-quarter, top-down.
- **Moments/beats:** establishing, action, reaction, transition, detail/insert.
- **Lighting/time:** golden hour, blue hour, harsh midday, night/neon, interior practical, backlit.
Keep the **subject identity, wardrobe, style, and grade constant**; vary framing, action, environment angle, and light.

## Strict consistency rule (paste into prompts when a reference is supplied)
> Keep the character's face, identity, hairstyle, proportions, and wardrobe identical to the reference. Maintain a consistent visual style, color grade, and rendering across every image. No identity drift, no style drift, no extra characters unless requested.

## Prompt template (one per shot)
```text
[Shot N] [shot size + angle] of [subject/character with key identity + wardrobe], [action/moment], in [setting], [time of day]. [Lens + depth of field], [lighting + color/mood], [style + grade]. Ultra-detailed, sharp focus, [aspect ratio if image]. Consistent with the reference identity and style. No watermark, no logo, no text, no extra characters unless requested.
```

## Exact output format
For each image (inline for 1–10; file output for 50/100):

```text
## 🖼️ Production Image [N] — [short label]
**Use the uploaded character sheet / storyboard as the identity + style reference if provided.**
```
Then the fenced `text` prompt block. For a set, add a one-line shot map at the top (e.g. `01 wide establishing · 02 medium action · 03 close reaction …`).

### 🔁 Next step
Offer exactly one: `Want me to turn your favorite shots into a video prompt (Seedance or Kling), or generate these as images now?`

## Higgsfield image generation (if depth B)
- **Model:** Nano Banana Pro (detail + consistency), Soul for a faithful single character, Nano Banana 2 / Seedream for faster drafts. Resolve IDs via `models_explore`.
- **References:** upload the character sheet / storyboard via `media_upload` → confirm, pass by role (see `higgsfield-mcp.md`). For a reusable character across many shots, consider a Soul or saved reference Element.
- **Length:** image prompts are concise and structured (~40–150 words) — do not pad. Clarity over length.
- **Credits:** ALWAYS run the credit-confirmation step (estimate via `get_cost: true` × count → show summary → wait for yes) before generating. 50/100 shots can be a large spend.
- **Aspect ratio:** pass as the `aspect_ratio` parameter.

## Bulk notes
- 10 → inline numbered set + offer a file.
- 50 / 100 → build a spec and run `scripts/bulk_builder.py` (`mode: production_image`); writes one `.txt` per shot + `index.md` + `manifest.csv`, zipped. Keeps the shot-variety rotation. Then (depth B) confirm credits and generate in batches.
