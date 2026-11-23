# 📦 Bulk Generation — 1 / 10 / 50 / 100 + Full Projects

How Cinematic Prompt Studio produces many character sheets, storyboards, production images, video prompts, or thumbnails at once — efficiently and without flooding the chat — and how it runs a complete multi-asset **project** in one go. Read this when the user asks for more than one item, says "10" / "50" / "100" / "a batch" / "a set," or wants a full pipeline (e.g. "1 sheet → 10 storyboards → 100 shots").

## Table of contents
1. Intake (what to confirm)
2. Scale rules (1 / 10 / 50 / 100)
3. The spec JSON (all five modes)
4. Running `scripts/bulk_builder.py`
5. Output the user gets
6. Bulk + Higgsfield media (MANDATORY credit confirmation & batching)
7. Quality vs. scale
8. Worked example
9. Full multi-asset project pipeline

---

## 1) Intake — confirm before building
1. **Mode(s)** — character sheet, storyboard, production images, video prompt (dialogue / no-dialogue), or thumbnail. (A project can chain several — see section 9.)
2. **Count** — 1, 10, or 100 (production images also commonly 50). Any number works.
3. **Base concept + what varies** — e.g. "100 cyberpunk street vendors, vary trade / age / ethnicity," "50 cinematic shots of my character across a city," or "100 thumbnails like this one, vary the hook." This is the one thing you must get from the user; do not invent the concept.
4. **Generation depth** — prompts only · prompts + images · prompts + video.
5. **Model** (if generating media) — see `references/higgsfield-mcp.md`.

You may expand the concept into distinct, non-repetitive variations (that's the value you add). Keep shared settings (style, duration, shots, aspect ratio, branding, continuity) constant across the batch unless the user wants variety.

## 2) Scale rules
- **1** → generate inline in chat using the normal mode flow (highest quality, copy-ready code block).
- **10** → generate inline as a clean numbered set (each in its own `text` block), **and** offer the downloadable file set (run the script). Good middle ground.
- **50 / 100** → **do not** paste them into chat. Instead:
  1. Produce a structured list of *distinct* variations (the creative differentiation is your job).
  2. Write a spec JSON (section 3) and run `scripts/bulk_builder.py` (section 4).
  3. Deliver the zipped file set (individual prompts + combined index + manifest) via the file-presentation tool.

The script handles the repetitive assembly (templates, timecodes, negatives, `No background music`, shot-variety rotation, the under-2000 cap check) so large batches take a fraction of a second and stay perfectly consistent.

## 3) The spec JSON

```json
{
  "mode": "video_prompt",
  "dialogue": false,
  "global": {
    "style": "ultra-realistic commercial video",
    "duration": "12 seconds",
    "shots": 8,
    "aspect_ratio": "16:9",
    "environment": "neon-lit night market"
  },
  "items": [
    { "name": "Aya the welder", "subject": "a welder", "scene": "sparks flying in a harbor workshop" },
    { "name": "Old Mback", "subject": "an elderly salvager", "scene": "sorting parts at dusk" }
  ]
}
```

`global` holds shared defaults; any field can be overridden per item. Per-item fields by mode:

| mode | required-ish fields | optional |
|---|---|---|
| `character_sheet` | `name`, `character`, `personality` | `style`, `aspect_ratio` |
| `storyboard` | `name`/`project`, `subject` | `environment`, `style`, `duration`, `shots`, `aspect_ratio`, `shots_list` |
| `video_prompt` | `name`, `subject`, `scene` | `style`, `duration`, `shots`, `shots_seq` |
| `production_image` | `name`, `subject`, `scene` | `style`, `shot_size`, `angle`, `lighting`, `aspect_ratio` |
| `thumbnail` | `name`, `title`/`topic` | `subject`, `hook`, `style`, `palette`, `text`, `aspect_ratio` |

- `production_image`: the script rotates shot size / angle / lighting across the set for variety while holding subject + style constant. Override per item with `shot_size`, `angle`, `lighting` if you want exact control.
- `thumbnail`: the script holds the brand fingerprint (`global.style`, `palette`, text style) constant and rotates `hook` / expression / `text` per item. Supply a `fingerprint` string in `global` (from the analyzed reference) so every variation stays on-brand.

- `shots_list` (storyboard): list of `"Title - action"` strings. If omitted, the script scaffolds from the 8/10/12 beat structure with rotating camera grammar.
- `shots_seq` (video): list of `{ "title": "...", "action": "...", "dialogue": { "speaker": "...", "line": "..." } }`. If omitted, the script scaffolds timed beats; with `dialogue:true` it adds short lines on alternating beats. **For best quality, supply `shots_seq` with real short lines** rather than relying on the scaffold.

## 4) Running the script

```bash
python scripts/bulk_builder.py SPEC.json --out OUTPUT_DIR --zip
```

- `--out` — output directory (created if missing).
- `--zip` — also produce `OUTPUT_DIR.zip` for download.

It prints a summary and flags any video prompt over 2000 characters so you can compress it. The 8-shot default lands comfortably under cap; dense 10–12 shot or all-dialogue prompts may warn — tighten wording or reduce lines when they do.

## 5) Output the user gets
```
OUTPUT_DIR/
├── prompts/        # one .txt per item (the copy-ready prompt body)
│   ├── 001-aya-the-welder.txt
│   └── 002-old-mback.txt
├── index.md        # all prompts as fenced text blocks with headers, in order
└── manifest.csv    # index, id, name, file, char count, warnings
```
Present `index.md` (or the `.zip`) with the file-presentation tool and a one-line summary.

## 6) Bulk + Higgsfield media (MANDATORY credit confirmation & batching)
When the depth is "+ images" or "+ video" for any count:
1. **Generate the prompts/files first** (above) so the user always has them, even if generation stops.
2. **Credit confirmation is mandatory.** Confirm the MCP is connected, then preflight the per-item cost with `get_cost: true`, multiply by the count, optionally call `balance`, and show the **Generation Summary** block (see `references/higgsfield-mcp.md` §4). **Wait for an explicit yes.** No batch starts without it.

```text
💳 Generation Summary
• Type:   <e.g. Production Images>
• Count:  100
• Model:  Nano Banana Pro
• Est. credits: <total>   (≈ <per-item> each)
• Your balance: <balance>

Proceed?  ✅ Yes   ❌ No
```

3. On **Yes**, generate media in **controlled batches** (e.g. 10 at a time) with a checkpoint between batches; stop and warn if credits run low. On **No**, offer a smaller count, a cheaper model, or prompts-only.
4. For a consistent recurring character across a large set, consider a reusable **Soul character** or **reference Element** (see `references/higgsfield-mcp.md` §11) so identity holds across every item.

## 7) Quality vs. scale
- 1–10: prefer hand-written shots (`shots_list` / `shots_seq`) — richest results.
- 100: lean on the scaffold for structure, but invest your effort in making the **variation list genuinely diverse** (vary subject, world, mood, palette, action) so the set doesn't feel copy-pasted.
- Always keep continuity fields constant within a set unless variety is the point.

## 8) Worked example (100 video prompts)
1. User: "Give me 100 short cinematic ad-style video prompts for street-food vendors around the world, no dialogue."
2. You: confirm — 100 · video · no dialogue · 12s/8 shots · style "ultra-realistic commercial video" · prompts only.
3. You: generate 100 distinct vendor variations (city, dish, vendor type, time of day, mood).
4. You: write `spec.json` (mode `video_prompt`, the 100 items) and run:
   `python scripts/bulk_builder.py spec.json --out street_food_100 --zip`
5. You: present `street_food_100.zip` + a 1-line summary, then offer to render a sample batch via Higgsfield if they want video.

## 9) Full multi-asset project pipeline
Users can request a whole project at once, e.g.:

> "Generate 1 character sheet, 10 storyboards, 100 production images, 50 video prompts, and 20 thumbnails."

Handle it as an ordered pipeline, not five disconnected batches:

1. **Plan & confirm scope.** Restate the full list and the shared concept/style. Ask anything genuinely missing (the core subject/brand) — never invent it.
2. **Estimate the whole project up front.** Build the prompts/specs for each stage, preflight each stage's per-item cost (`get_cost: true`) for the chosen models, and present **one combined estimate** before any generation:

```text
🗂️ Project Plan & Estimate
1. 🎭 Character Sheet × 1     — <model> — ~<credits>
2. 🎞️ Storyboard × 10         — <model> — ~<credits>
3. 🖼️ Production Images × 100  — <model> — ~<credits>
4. 🎬 Video Prompts × 50       — prompts only — 0
5. 📺 Thumbnails × 20          — <model> — ~<credits>
─────────────────────────────
Total est. credits: <sum>     Your balance: <balance>

Proceed with the full project?  ✅ Yes   ❌ No   ⚙️ Adjust
```

3. **Wait for yes.** Never start the pipeline without confirmation (this is the credit gate at project scale).
4. **Build in dependency order** so each stage can feed the next:
   `Character Sheet → Storyboards → Production Images → Video Prompts → Thumbnails`.
   - Use the character sheet as the identity reference for storyboards, production images, and thumbnails.
   - Offer to **reuse** any asset the user already has instead of regenerating it (saves credits).
   - Run each media stage with the mandatory per-stage credit checkpoint and controlled batches.
5. **Deliver** via `scripts/project_export.py`: assemble the standard project tree (categorized folders + consistent names + prompt siblings), write metadata/logs to `Project Files/`, and `package` into ZIP(s) — auto-split for large projects. Desktop → write to the user's folder; Web → present the ZIP(s) plus inline previews. See `references/asset-management.md`.

Prompts-only stages cost nothing and need no confirmation; only the media stages hit the credit gate. Always generate every prompt/file first, then media, then package.
