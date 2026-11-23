#!/usr/bin/env python3
"""
Cinematic Prompt Studio - bulk_builder.py

Stamp a list of per-item variations into the canonical Cinematic Prompt Studio templates
(character sheet / storyboard / video prompt) and write copy-ready files at
scale (1, 10, or 100). The model supplies a compact JSON spec of what varies;
this script handles the repetitive assembly, timing, validation, and file I/O.

USAGE
    python bulk_builder.py SPEC.json --out OUTPUT_DIR [--zip]

The fenced ```text prompt body is what the user copies. Each item also gets a
standalone .txt file, plus a combined index.md and a manifest.csv.

SPEC FORMAT (see references/bulk-generation.md for the full guide)
{
  "mode": "character_sheet" | "storyboard" | "video_prompt" | "production_image" | "thumbnail",
  "dialogue": false,                      # video_prompt only (default false)
  "global": {                             # shared defaults, overridable per item
    "style": "ultra-realistic commercial video",
    "duration": "12 seconds",            # storyboard / video
    "shots": 8,                          # storyboard / video
    "aspect_ratio": "16:9",              # storyboard / production_image / thumbnail
    "palette": "...",                    # thumbnail
    "fingerprint": "...",                # thumbnail (style of the analyzed reference)
    "environment": "neon-lit night market"
  },
  "items": [
    { "name": "Aya the welder", "character": "...", "personality": "..." },
    ...
  ]
}

Per-item fields by mode:
  character_sheet  : name, character, personality, style?
  storyboard       : name|project, subject, environment?, style?, duration?, shots?,
                     shots_list? (list of "Title - action" strings; auto-scaffolded if absent)
  video_prompt     : name, subject, scene, style?, duration?, shots?,
                     shots_seq? (list of {title, action, dialogue?}; auto-scaffolded if absent)
  production_image : name, subject, scene, style?, shot_size?, angle?, lighting?, action?,
                     aspect_ratio?   (shot_size/angle/lighting auto-rotate across the set)
  thumbnail        : name, title|topic, subject?, hook?, expression?, text?, palette?,
                     fingerprint?, style?, aspect_ratio?   (hook/expression auto-rotate)
"""

import argparse
import csv
import json
import re
import sys
import zipfile
from pathlib import Path

CHAR_CAP = 2000  # hard cap for video prompts

# Canonical 8/10/12 storyboard beat structures (PDF 2)
STRUCTURES = {
    8:  ["Opener / establishing shot", "First action impact", "Process or escalation",
         "Texture or detail close-up", "Main transformation or reveal", "Peak motion or conflict",
         "Final build / emotional setup", "Hero ending / payoff"],
    10: ["Establish world", "Introduce character", "Trigger action", "First escalation",
         "Detail close-up", "Motion peak", "Transformation or twist", "Emotional reaction",
         "Hero reveal", "Final payoff"],
    12: ["Establishing beat", "Character intention", "First action", "Detail action",
         "Process beat", "Environmental shift", "Escalation", "Peak action",
         "Slow-motion / hero beat", "Final detail", "Presentation / reveal", "Emotional payoff"],
}

# Camera grammar rotation so each auto-scaffolded panel looks different (PDF 2/3)
CAMERAS = ["wide establishing shot", "medium shot", "low-angle tracking shot",
           "extreme close-up", "overhead beauty shot", "side tracking shot",
           "slow push-in", "hero close-up", "handheld natural lag", "rack focus",
           "POV shot", "tight reaction shot"]

# Production-image variety rotations (so a set of 50/100 stills isn't near-duplicates)
SHOT_SIZES = ["extreme wide shot", "wide shot", "medium shot", "medium close-up",
              "close-up", "macro detail shot"]
ANGLES = ["eye-level", "low angle", "high angle", "over-the-shoulder",
          "profile", "three-quarter", "top-down"]
LIGHTING = ["golden-hour backlight", "blue-hour ambience", "soft overcast daylight",
            "moody neon night", "warm interior practical light", "hard directional sunlight",
            "rim-lit silhouette", "diffused studio softbox"]

# Thumbnail variety rotations (hold brand constant, rotate the hook + emotion)
HOOKS = ["curiosity gap", "shocking result", "warning / common mistake", "big number or list",
         "before vs after", "this vs that comparison", "direct question", "transformation reveal"]
EXPRESSIONS = ["wide-eyed shock", "excited grin", "intense focus", "skeptical raised brow",
               "jaw-drop amazement", "confident smirk", "worried concern", "pointing reaction"]


def parse_duration_seconds(duration):
    """Best-effort seconds from a duration string/number ('12 seconds' -> 12.0)."""
    if isinstance(duration, (int, float)):
        return float(duration)
    if not duration:
        return 12.0
    m = re.search(r"(\d+(?:\.\d+)?)", str(duration))
    return float(m.group(1)) if m else 12.0


def timecodes(duration, num_shots):
    """Evenly spaced [MM:SS.s-MM:SS.s] beats. Reproduces the PDF timing tables
    (12s/8 = 1.5s each, 15s/10 = 1.5s each, 20s/10 = 2s each, etc.)."""
    total = parse_duration_seconds(duration)
    n = max(int(num_shots), 1)
    step = total / n

    def fmt(t):
        mm = int(t // 60)
        ss = t - mm * 60
        return f"{mm:02d}:{ss:04.1f}"

    return [f"[{fmt(i*step)}-{fmt((i+1)*step)}]" for i in range(n)]


def slugify(text, fallback):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", str(text or "").strip()).strip("-").lower()
    return s[:60] or fallback


def merged(item, glob):
    out = dict(glob or {})
    out.update({k: v for k, v in item.items() if v not in (None, "")})
    return out


# ---------------------------------------------------------------------------
# Builders (return the full prompt body that goes inside the ```text block)
# ---------------------------------------------------------------------------

def build_character_sheet(it):
    character = it.get("character", "[describe character]")
    personality = it.get("personality", "[traits, emotional baseline, inner conflict, behavior, movement rhythm]")
    style = it.get("style", "[requested style]")
    ar = it.get("aspect_ratio")
    ar_line = f"\nAspect Ratio:\n{ar}\n" if ar else ""
    return f"""Create a high-end cinematic character design sheet intended for a premium film or animation production.

Character:
{character}

Personality:
{personality}

Design Requirements:
- Full-body turnaround: front, 3/4 front, side, back, 3/4 back
- Consistent face, body proportions, hairstyle, outfit, colors, accessories, props, and materials across all views
- Expressive head studies from multiple angles
- Cinematic hero portrait
- Wardrobe, accessories, props, and material close-ups
- Height reference scale
- Handwritten-style production notes and callouts
- Dynamic art-directed layout, not a generic grid
- Slightly asymmetrical premium studio pitch-board composition

Performance Direction:
The character must feel like a real actor caught mid-moment, not a posed mannequin. Include natural posture, expressive eyes, subtle facial tension, and emotionally readable body language.

Style:
{style}
Cinematic lighting, emotional readability, high production value, sharp detail, clean background, professional concept art presentation.{ar_line}

Consistency Rule:
Maintain perfect continuity in face, proportions, hairstyle, outfit, accessories, color palette, and material details across every view. No reinterpretation between angles.

Negative:
No generic model sheet, no boring grid, no identity drift, no inconsistent outfit, no extra characters, no watermark, no logo, no blurry details, no plastic-looking materials unless requested."""


def build_storyboard(it):
    project = it.get("project") or it.get("name", "[title]")
    duration = it.get("duration", "12 seconds")
    shots = int(it.get("shots", 8))
    style = it.get("style", "[visual style]")
    subject = it.get("subject", "[character or subject description]")
    environment = it.get("environment", "[location/world]")
    ar = it.get("aspect_ratio", "16:9")

    shots_list = it.get("shots_list")
    if not shots_list:
        beats = STRUCTURES.get(shots, STRUCTURES[8])[:shots]
        shots_list = [f"{b} - {subject} in {environment}, {CAMERAS[i % len(CAMERAS)]}"
                      for i, b in enumerate(beats)]
    seq = "\n".join(f"{i+1}. {line}" for i, line in enumerate(shots_list))

    return f"""Create a professional cinematic storyboard sheet.

Project:
{project}

Duration:
{duration}

Panels:
{shots}

Aspect Ratio:
{ar}

Style:
{style}

Character/Subject:
{subject}

Environment:
{environment}

Storyboard Layout:
Clean widescreen production storyboard sheet with numbered panels, clear shot titles, camera notes, action notes, timing hints, and strong visual flow. Use a professional layout with readable panel structure.

Continuity Rules:
- Same character identity throughout
- Same outfit, proportions, props, and style throughout
- Same environment logic and lighting direction throughout
- Each panel must be a distinct cinematic shot
- Strong variety in camera angles: wide, medium, close-up, extreme close-up, overhead, low angle, tracking, hero shot where useful

Shot Sequence:
{seq}

Visual Direction:
Use clear cinematic composition, readable silhouettes, emotional progression, strong pacing, and dynamic motion. Prioritize shot grammar, continuity, and story clarity.

Footer Notes:
Include camera tips, timing flow, style notes, and continuity reminders.

Negative:
No watermark, no logo, no random text inside panels, no inconsistent costume, no identity drift, no messy layout, no extra characters unless requested."""


def build_video(it, dialogue):
    duration = it.get("duration", "12 seconds")
    shots = int(it.get("shots", 8))
    subject = it.get("subject", "[subject]")
    scene = it.get("scene", "[scene]")
    style = it.get("style", "[style]")
    tcs = timecodes(duration, shots)

    seq_in = it.get("shots_seq")
    blocks = []
    for i in range(shots):
        if seq_in and i < len(seq_in):
            s = seq_in[i]
            title = s.get("title", f"Beat {i+1}")
            action = s.get("action", f"{subject}, {CAMERAS[i % len(CAMERAS)]}")
            line = s.get("dialogue")
        else:
            beats = STRUCTURES.get(shots, STRUCTURES[8])
            title = beats[i % len(beats)]
            # compact + length-robust: Subject/Scene declared once at top; vary only the camera
            action = f"{CAMERAS[i % len(CAMERAS)]}; natural movement, emotional beat"
            line = None
        block = f"{tcs[i]}\nSHOT {i+1} - {title}\n{action}"
        if dialogue:
            spk = (line or {}).get("speaker") if isinstance(line, dict) else None
            text = (line or {}).get("line") if isinstance(line, dict) else line
            # If the model supplied a line, always include it. For the auto-scaffold
            # fallback, attach dialogue only to alternating beats (cinematic + keeps length down).
            if text or seq_in:
                block += f"\nDialogue:\n{spk or 'Character'}:\n\"{text or '[line]'}\""
            elif i % 2 == 0:
                block += "\nDialogue:\nCharacter:\n\"[line]\""
        blocks.append(block)
    sequence = "\n\n".join(blocks)

    if dialogue:
        rules_extra = "- Dialogue must be short, natural, and timed to the shots"
        no_dialogue_lines = ""
        audio = "Clear dialogue, natural room tone, movement sounds, object sounds, atmosphere, and realistic effects. No background music."
        negs = ("No background music, no subtitles, no text on screen, no watermark, no logo, no UI, "
                "no aspect ratio, no extra characters unless requested, no off-story events, no identity drift, "
                "no style drift, no costume drift, no environment drift.")
    else:
        rules_extra = "- No dialogue"
        no_dialogue_lines = "- No subtitles\n- No text on screen\n"
        audio = ("Natural sound effects only: environment sounds, movement sounds, object sounds, breathing, "
                 "ambience. No background music.")
        negs = ("No background music, no subtitles, no text on screen, no watermark, no logo, no UI, "
                "no aspect ratio, no extra story events, no extra characters unless requested, no identity drift, "
                "no style drift, no costume drift, no environment drift.")

    return f"""Create a {duration} cinematic video.

Reference:
Use the uploaded storyboard/image as the exact visual and timing reference if provided.

Subject:
{subject}

Scene:
{scene}

Style:
{style}

Rules:
- Follow the shot order exactly if a storyboard is provided
- Each panel is one separate cinematic shot beat if a storyboard is provided
- Maintain character, outfit, environment, lighting, and prop continuity
{rules_extra}
{no_dialogue_lines}- No background music
- Natural sound design only
- Do not mention aspect ratio

Shot Sequence:
{sequence}

Audio:
{audio}

Negative:
{negs}"""


def build_production_image(it, idx=0):
    subject = it.get("subject", "[subject/character]")
    scene = it.get("scene", "[setting]")
    style = it.get("style", "[visual style]")
    ar = it.get("aspect_ratio", "16:9")
    action = it.get("action") or "a natural, emotionally readable moment"
    shot_size = it.get("shot_size") or SHOT_SIZES[idx % len(SHOT_SIZES)]
    angle = it.get("angle") or ANGLES[idx % len(ANGLES)]
    lighting = it.get("lighting") or LIGHTING[idx % len(LIGHTING)]
    return f"""Create a standalone, production-quality cinematic still.

Reference:
Use the uploaded character sheet / storyboard as the identity and style reference if provided.

Shot:
{shot_size}, {angle}.

Subject:
{subject}, {action}.

Setting:
{scene}.

Lighting & Mood:
{lighting}.

Style:
{style}. Cinematic color grade, ultra-detailed, sharp focus, high production value.

Aspect Ratio:
{ar}

Consistency:
Keep face, identity, hairstyle, proportions, wardrobe, and visual style identical to the reference. No identity drift, no style drift.

Negative:
No watermark, no logo, no text on screen, no UI, no extra characters unless requested, no duplicate limbs, no distortion."""


def build_thumbnail(it, idx=0):
    title = it.get("title") or it.get("topic", "[video title]")
    subject = it.get("subject", "the host/subject")
    style = it.get("style", "[brand visual style]")
    palette = it.get("palette", "[brand palette]")
    fingerprint = it.get("fingerprint", "match the reference thumbnail's layout, colors, and text style")
    ar = it.get("aspect_ratio", "16:9")
    hook = it.get("hook") or HOOKS[idx % len(HOOKS)]
    expr = it.get("expression") or EXPRESSIONS[idx % len(EXPRESSIONS)]
    text = it.get("text") or "[3-5 word hook]"
    return f"""Create a high-CTR YouTube thumbnail, 16:9 (1280x720).

Reference:
Use the uploaded thumbnail / style reference for branding if provided.

Video:
{title}

Concept / Hook:
{hook}.

Subject:
{subject}, {expr}; bold crop, strong rim light, high contrast against the background.

Background:
High-contrast scene supporting the hook; clean, uncluttered.

Color Palette:
{palette}

Text:
"{text}" - large, bold, high-contrast with outline/shadow, placed clear of the face. 3-5 words max.

Branding:
{fingerprint}. Keep palette, text style, and framing consistent with the brand across variations.

Style:
{style}. Ultra-sharp, punchy, instantly readable at small size.

Aspect Ratio:
{ar}

Negative:
No clutter, no tiny text, no low contrast, no face obstruction, no distortion, no watermark unless it is the brand logo."""


# ---------------------------------------------------------------------------
# Validation (video prompts only)
# ---------------------------------------------------------------------------
ASPECT_TOKENS = re.compile(r"\b(16:9|9:16|1:1|4:3|3:4|21:9|vertical|horizontal|landscape|portrait)\b", re.I)


def validate_video(body):
    warnings = []
    if len(body) > CHAR_CAP:
        warnings.append(f"OVER CAP: {len(body)} chars (>{CHAR_CAP}) - compress this prompt")
    if "No background music" not in body:
        warnings.append("missing 'No background music'")
    # flag positive aspect-ratio specs, but ignore the negative 'no aspect ratio' rule line
    for m in ASPECT_TOKENS.finditer(body):
        ctx = body[max(0, m.start()-12):m.start()].lower()
        if "no aspect" not in ctx:
            warnings.append(f"aspect-ratio term '{m.group(0)}' in prompt text (remove unless user asked)")
            break
    return warnings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Cinematic Prompt Studio bulk prompt builder")
    ap.add_argument("spec", help="Path to spec JSON")
    ap.add_argument("--out", default="cineprompt_output", help="Output directory")
    ap.add_argument("--zip", action="store_true", help="Also produce a .zip of the output dir")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    mode = spec.get("mode")
    VALID_MODES = ("character_sheet", "storyboard", "video_prompt", "production_image", "thumbnail")
    if mode not in VALID_MODES:
        sys.exit(f"Bad mode: {mode!r} (use {' | '.join(VALID_MODES)})")
    dialogue = bool(spec.get("dialogue", False))
    glob = spec.get("global", {})
    items = spec.get("items", [])
    if not items:
        sys.exit("Spec has no items.")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    prompts_dir = out / "prompts"
    prompts_dir.mkdir(exist_ok=True)

    label = {"character_sheet": "Character Sheet", "storyboard": "Storyboard",
             "video_prompt": f"Video Prompt {'With' if dialogue else 'Without'} Dialogue",
             "production_image": "Production Image", "thumbnail": "Thumbnail"}[mode]
    header = {"character_sheet": "## 🎭 Character Sheet Prompt\n**Use Reference Image 1 if uploaded.**",
              "storyboard": "## 🎞️ Storyboard Prompt\n**Use Reference Image 1 if uploaded.**",
              "video_prompt": f"## 🎬 {label}",
              "production_image": "## 🖼️ Production Image Prompt\n**Use the uploaded character sheet / storyboard as the reference if provided.**",
              "thumbnail": "## 📺 Thumbnail Prompt\n**Use the uploaded thumbnail / style reference for branding if provided.**"}[mode]

    index_lines = [f"# Cinematic Prompt Studio - Bulk {label}", f"_{len(items)} item(s)_\n"]
    manifest_rows = []
    total_warnings = 0

    for i, raw in enumerate(items, 1):
        it = merged(raw, glob)
        item_id = str(raw.get("id") or f"{i:03d}")
        name = (raw.get("name") or raw.get("project") or raw.get("subject")
                or raw.get("title") or raw.get("topic") or f"item-{item_id}")
        slug = f"{item_id}-{slugify(name, 'item')}"

        if mode == "character_sheet":
            body = build_character_sheet(it)
        elif mode == "storyboard":
            body = build_storyboard(it)
        elif mode == "production_image":
            body = build_production_image(it, i - 1)
        elif mode == "thumbnail":
            body = build_thumbnail(it, i - 1)
        else:
            body = build_video(it, dialogue)

        warns = validate_video(body) if mode == "video_prompt" else []
        total_warnings += len(warns)

        block = f"{header}\n```text\n{body}\n```\n"
        (prompts_dir / f"{slug}.txt").write_text(body + "\n")

        index_lines.append(f"\n---\n\n### {i}. {name}  \n`prompts/{slug}.txt`" +
                           (f"  \n⚠️ {'; '.join(warns)}" if warns else "") + f"\n\n{block}")
        manifest_rows.append({"index": i, "id": item_id, "name": name,
                              "file": f"prompts/{slug}.txt", "chars": len(body),
                              "warnings": "; ".join(warns)})

    (out / "index.md").write_text("\n".join(index_lines))
    with (out / "manifest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["index", "id", "name", "file", "chars", "warnings"])
        w.writeheader()
        w.writerows(manifest_rows)

    if args.zip:
        zip_path = out.with_suffix(".zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for p in out.rglob("*"):
                if p.is_file():
                    z.write(p, p.relative_to(out.parent))
        print(f"Zipped -> {zip_path}")

    print(f"Built {len(items)} {label} prompt(s) -> {out}/")
    print(f"  - prompts/   ({len(items)} .txt files)")
    print(f"  - index.md   (combined, copy-ready blocks)")
    print(f"  - manifest.csv")
    if total_warnings:
        print(f"  ⚠️ {total_warnings} validation warning(s) - see manifest.csv / index.md")


if __name__ == "__main__":
    main()
