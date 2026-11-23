# 📺 YouTube Thumbnail — on-brand variations

## What this mode is
A dedicated YouTube thumbnail workflow. The user uploads an existing thumbnail (and/or a character sheet, storyboard, or style reference), and you generate **1 / 10 / 100** new thumbnail prompts (and images) that match the same visual style and branding. Designed for high click-through and brand consistency, with bulk support for A/B testing at scale.

## Flow
1. Ask the intake question (below) and **wait**.
2. Read this file. If generating, also read `higgsfield-mcp.md` for the **credit-confirmation step** and upload flow.
3. If an existing thumbnail is uploaded, **analyze it** and extract its style fingerprint (below). Re-apply that style to new concepts.
4. Produce the variations → one copy-ready prompt each (inline for small counts; via `scripts/bulk_builder.py` for 100).
5. End with one next-step question.

## Intake question
```text
📺 Upload your existing thumbnail (or a style reference), tell me the video topic/title, and how many variations you want (1 / 10 / 100).
A character sheet or brand reference helps keep it consistent.
```
Never invent the topic, face, or brand from a bare mode pick — ask first.

## Analyze the uploaded thumbnail — extract the style fingerprint
When a thumbnail (or style reference) is provided, read and reuse:
- **Layout & composition** — subject placement (left/right third), focal point, negative space, how busy vs clean.
- **Color** — dominant palette, background treatment, contrast level, saturation.
- **Text** — presence, word count, font weight/style, color, outline/shadow, placement, ALL-CAPS or not. (Keep text short — 3–5 punchy words max.)
- **Face / subject treatment** — expression intensity, crop, lighting on the face, cut-out vs in-scene, glow/outline.
- **Branding** — logos, recurring colors, watermarks, channel style cues, consistent border/frame.
- **Effects** — arrows, circles, glows, drop shadows, gradients, emoji/sticker accents.
State the fingerprint briefly, then generate new concepts that **preserve branding consistency** while varying the hook.

## Thumbnail design principles (apply to every prompt)
- **One clear focal point**; instantly readable at small size.
- **High contrast** subject-vs-background; bold, saturated, punchy.
- **Expressive face** when relevant (strong, clear emotion) — faces drive clicks.
- **Minimal text** — 3–5 words, large, high-contrast, with outline/shadow for legibility; never cover the face.
- **Rule of thirds**; leave the bottom-right relatively clear (timestamp overlay) and respect title-safe margins.
- **16:9, 1280×720** target (pass as the `aspect_ratio` parameter / image canvas).
- **Brand consistency** across a set: same palette, same text style, same framing logic — vary the concept, not the identity.

## Variation strategy (so 100 thumbnails aren't 100 clones)
Vary across: facial expression/emotion, hook angle (curiosity / result / warning / number / before-after), background scene, text phrasing, color accent, subject pose/crop, and effect treatment — **while holding the brand style constant**.

## Prompt template (one per thumbnail)
```text
YouTube thumbnail, 16:9, for a video titled "[title/topic]". [Subject/character with key identity + expressive emotion], [crop/pose], [placement per composition]. Background: [scene/treatment, high contrast]. Color palette: [palette]. Text: "[3–5 word hook]" in [font weight/style, color, outline/shadow], placed [position], not covering the face. [Effects: glow/arrow/etc.]. Match the style and branding of the reference thumbnail: [fingerprint cues]. Bold, high-contrast, ultra-sharp, click-optimized. No clutter, no watermark unless it's the brand logo.
```

## Exact output format
For each thumbnail (inline for 1–10; file output for 100):

```text
## 📺 Thumbnail [N] — [hook angle]
**Use the uploaded thumbnail / style reference for branding if provided.**
```
Then the fenced `text` prompt block. For a set, add a one-line concept map at the top.

### 🔁 Next step
Offer exactly one: `Want me to generate these as images now (Nano Banana Pro), or produce more variations / a different hook angle?`

## Higgsfield image generation (if depth B)
- **Model:** Nano Banana Pro — strongest text rendering and brand/style control (ideal for thumbnails). Resolve IDs via `models_explore`.
- **References:** upload the existing thumbnail / style ref / character via `media_upload` → confirm, pass by role; mark which image is style vs character (see `higgsfield-mcp.md`).
- **Length:** concise, structured prompts (~40–150 words) — clarity over length.
- **Credits:** ALWAYS run the credit-confirmation step before generating (estimate × count → summary → wait for yes). 100 variations is a meaningful spend.
- **Aspect ratio:** 16:9 via the `aspect_ratio` parameter.

## Bulk notes
- 10 → inline numbered set + offer a file.
- 100 → build a spec and run `scripts/bulk_builder.py` (`mode: thumbnail`); writes one `.txt` per variation + `index.md` + `manifest.csv`, zipped, holding the brand fingerprint constant while rotating hooks/expressions. Then (depth B) confirm credits and generate in batches.
