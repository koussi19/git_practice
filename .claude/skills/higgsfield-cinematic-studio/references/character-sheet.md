# 🎭 Character Sheet — Knowledge & Workflow

Source of truth for premium character-sheet prompts (AI image tools, film pitch decks, animation dev, AI video workflows, consistent character creation). Read this fully before generating a character sheet. Goal: turn a reference image or a rough idea into a complete production-grade character sheet prompt.

## Table of contents
1. Flow (intake → output → follow-up)
2. What a character sheet must include
3. Character identity fields
4. Face / performance / wardrobe / material guidance
5. Layout & style flexibility
6. Reference-image rules & strict consistency rule
7. The prompt template
8. Output format (exact)
9. Higgsfield image generation for character sheets
10. Bulk notes

---

## 1) Flow

**Intake question (ask this, then wait):**
> 🎭 Upload a character reference image or describe your character. Include style, age, outfit, personality, and world if you know them.

Keep intake short — do not ask many questions. If the user gives only a small idea, **expand it automatically** into a rich character (but never fabricate the character itself from an empty selection — see the menu/starter rule in SKILL.md).

After the user answers, produce the character sheet (section 8), then ask the follow-up:
> **Do you want me to create a storyboard with this character? If yes, tell me the scene idea, duration, and number of shots.**

---

## 2) A character sheet must include
- Full-body turnaround: front, 3/4 front, side, back, 3/4 back
- Expressive head studies (multiple angles)
- Hero cinematic portrait
- Costume breakdown
- Accessories and props
- Material close-ups
- Height reference
- Production notes
- Personality cues
- Motion and body-language notes
- Strict identity-consistency rule

## 3) Character identity fields
Capture (infer/expand sensibly when the user is brief): Name · Alias or symbolic role · Age · Height · Build · Ethnicity or design language · World/setting · Style · Personality · Core conflict · Emotional baseline · Movement rhythm · Signature behavior · Key prop · Wardrobe · Color palette.

## 4) Face / performance / wardrobe / material guidance

**Face design** — describe face shape; bone structure; skin tone & texture; eye shape, color, spacing, expression; hair style, texture, volume, motion; distinctive marks; asymmetry; imperfections; emotional readability. Never make characters generic — every character should feel like a real performer with a story.

**Performance direction** — the character should feel like an actor caught mid-moment, not a static mannequin: micro-expressions, lip tension, eyebrow movement, eye focus, subtle body tension, transitional emotion, natural posture, movement habits, idle behavior.

**Wardrobe** — should reveal personality and world: fabric type, fit, wear, stitching, wrinkles, dirt/aging, practicality, symbolic meaning, accessories, footwear, prop logic.

**Material accuracy** — fabric stretch, leather grain, metal scratches, skin softness, hair detail, dirt/smudges/marks, surface realism (stylized realism if requested).

## 5) Layout & style flexibility

**Layout** — should feel like a premium film production board. Avoid boring symmetrical grids; use a clean, art-directed layout: curated art-direction board, slightly asymmetrical composition, premium studio pitch-board layout, handwritten-style production notes, annotation callouts, wardrobe breakdown, hero portrait section, turnaround section, expression-study section, prop/material study section.

**Style (support any)** — Pixar-style stylized realism · anime production sheet · semi-realistic cinematic design · hyper-realistic film concept art · fashion editorial character sheet · clay animation character design · cartoon comedy character sheet · fantasy game character concept · horror creature character sheet · nostalgic cel animation character sheet.

## 6) Reference-image rules & strict consistency rule

If the user uploads a reference image, use it as the key identity reference and **preserve**: face identity, body proportions, hairstyle, outfit, color palette, props, style, personality impression. Do not change the character unless the user asks.

**Strict consistency rule — always include this line verbatim in the prompt:**
> Maintain perfect continuity in face, proportions, hairstyle, outfit, accessories, color palette, and material details across every view. No reinterpretation between angles.

---

## 7) Prompt template

Fill every bracket from the user's input (expanding a small idea as needed). Keep the structure.

```text
Create a high-end cinematic character design sheet intended for a premium film or animation production.

Character:
[describe character: name/role, age, height, build, ethnicity or design language, world/setting]

Personality:
[traits, emotional baseline, inner conflict, behavior, movement rhythm, signature behavior]

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
[requested style]
Cinematic lighting, emotional readability, high production value, sharp detail, clean background, professional concept art presentation.

Consistency Rule:
Maintain perfect continuity in face, proportions, hairstyle, outfit, accessories, color palette, and material details across every view. No reinterpretation between angles.

Negative:
No generic model sheet, no boring grid, no identity drift, no inconsistent outfit, no extra characters, no watermark, no logo, no blurry details, no plastic-looking materials unless requested.
```

> Aspect ratio is allowed in character-sheet/image prompts when useful (e.g. add `Aspect Ratio: 16:9` or `3:2` for a wide pitch-board). It is forbidden only in *video* prompts.

---

## 8) Output format (exact)

```
## 🎭 Character Sheet Prompt
**Use Reference Image 1 if uploaded.**
​```text
[premium character sheet prompt from the template]
​```

## 🔁 Next Step
**Do you want me to create a storyboard with this character? If yes, tell me the scene idea, duration, and number of shots.**
```

---

## 9) Higgsfield image generation for character sheets

Only when the user chose "prompts + images" and the Higgsfield MCP is connected (see `references/higgsfield-mcp.md`).

- **Recommended model:** **Nano Banana Pro** — best for fine detail, readable labels/callouts, and multi-panel pitch-board layouts. For a single faithful character (portrait/fashion) consider **Soul**, or a trained **Soul character** for a reusable identity.
- **Reference image:** if the user uploaded one, upload it via the MCP and pass it as the identity reference so the sheet preserves the face/outfit.
- **Aspect ratio:** pass a wide ratio (e.g. `16:9` or `3:2`) as the tool **parameter** to fit a turnaround board.
- Write the prompt first, show it, then generate. Surface the result; offer a refinement pass or to proceed to a storyboard.

## 10) Bulk notes
For 10 or 100 character sheets, see `references/bulk-generation.md`. Each sheet keeps this template; only the per-character fields vary. Reuse the same Style and Consistency Rule across the batch for a coherent set unless the user wants variety.
