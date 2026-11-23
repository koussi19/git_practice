# 🛰️ Higgsfield MCP — Integration & Generation

How Cinematic Prompt Studio turns prompts into actual **images and videos** through the Higgsfield MCP. Read this when the user picks generation depth **B (prompts + images)** or **C (prompts + video)**, or any bulk run that includes media.

## Table of contents
1. Two golden rules
2. Connection detection
3. Not-connected notice (verbatim + link)
4. 💳 Credit awareness & confirmation (MANDATORY)
5. Model selection (friendly → resolve via models_explore)
6. Model-aware prompt length
7. Reference image/storyboard upload flow
8. Image generation workflow
9. Video generation workflow + Seedance vs Kling pipelines
10. Aspect ratio, duration & the no-aspect-ratio rule
11. Reusable identity (Soul / Elements)
12. Asset reuse & dependency
13. Error handling

---

## 1) Two golden rules
1. **Always write and show the prompt(s) first, then generate.** The prompt is the deliverable the user keeps; generation is a bonus that can fail or cost credits.
2. **Never generate without a credit estimate and a yes.** Every image/video call — single or bulk — goes through the confirmation step in section 4 first. No exceptions.

## 2) Connection detection
The Higgsfield MCP is connected if its tools are available in this session (e.g. `generate_image`, `generate_video`, `models_explore`, `balance`, `media_upload`).
- If available → proceed (then always do section 4 before generating).
- If **not** available → show the notice in section 3 and continue in **prompts-only** mode.

Do not claim generation succeeded unless a tool actually returned a result.

## 3) Not-connected notice (show verbatim)

```text
⚠️ Higgsfield MCP isn't connected, so I can't generate images or videos yet — but I can still write every prompt for you.

To enable image + video generation:
1. Open this link and connect Higgsfield MCP:
   https://higgsfield.ai/mcp?fpr=3066&fp_sid=mcp
2. Follow the setup steps to authorize the connector.
3. Come back and say "ready" — I'll generate from the prompts I just made.

Want me to continue with prompts only for now?
```

## 4) 💳 Credit awareness & confirmation (MANDATORY — applies to every generation)
This gate applies to **character sheets, storyboards, production images, thumbnails, videos, and all bulk/project runs**. No batch — and no single generation — begins without it.

**Steps**
1. **Get the real per-item cost.** Call the generation tool with `get_cost: true` to preflight cost without submitting a job. Never guess or hardcode prices — they vary by model and settings. (Optionally call `balance` to show remaining credits.)
2. **Compute the total.** For a batch: per-item cost × count. For a multi-stage project: sum every stage into one combined estimate.
3. **Show the summary and STOP:**

```text
💳 Generation Summary
• Type:   <e.g. Production Images>
• Count:  <e.g. 100>
• Model:  <e.g. Nano Banana Pro>
• Est. credits: <total>   (≈ <per-item> each)
• Your balance: <balance, if known>

Proceed?
  ✅ Yes
  ❌ No
```

4. **Wait for the user.** On **Yes** → generate. On **No** → stop; offer a smaller count, a cheaper model, or prompts-only.
5. **Low balance:** if balance is clearly below the estimate, warn first; suggest reducing the count or topping up. If a tool returns a billing/recovery signal, surface the top-up option (use the tool's recovery metadata) rather than silently failing.

For **controlled batches** (10/100 with media), re-checkpoint between batches so the user can stop mid-run.

## 5) Model selection
Recommend by task, let the user override. **Do not hardcode machine model IDs** — call `models_explore` for the current catalog, exact IDs, supported `aspect_ratios`, `parameters`, and `medias[].roles`, then use what it returns. Present friendly names.

**Images**
| Use case | Recommended (friendly) | Why |
|---|---|---|
| Character sheet (turnaround + labels) | **Nano Banana Pro** | Best fine detail, readable callouts, multi-panel, up to 4K |
| Storyboard (multi-panel + shot titles) | **Nano Banana Pro** | Strong panel borders + small readable text |
| Production stills / cinematic shots | **Nano Banana Pro** (Soul for a faithful single character) | Detail + cross-shot consistency |
| YouTube thumbnails | **Nano Banana Pro** | Sharp text rendering + branding control |
| Single faithful character / portrait / fashion | **Soul** (or a trained Soul character) | Identity-faithful |
| Fast drafts / variations | **Nano Banana 2 / Seedream** | Quicker iteration for bulk |
| Branded product / DTC ad frames | **Marketing Studio image** | Commercial framing |

**Video**
| Use case | Recommended (friendly) | Why |
|---|---|---|
| Scenes / products / environments, identity continuity (default) | **Seedance** | Reference-driven, strong continuity (note: limited for people) |
| People, dialogue, multi-shot, native audio | **Kling 3.0** | Multi-shot + audio + lip-sync + Elements consistency |
| Branded product ad video | **Marketing Studio video** | Commercial ad workflow |

Offer the choice cleanly, e.g.:
```text
Pick an image model: 1) Nano Banana Pro (best detail — default)  2) Soul (faithful character)  3) Seedream (fast)
```
```text
Pick a video model: 1) Seedance (scenes/products — default)  2) Kling 3.0 (people, dialogue, multi-shot + audio)
```

## 6) Model-aware prompt length
Write the **optimal** length for the model; never pad to a maximum. Clarity beats length.

| Model | Target length | Guidance |
|---|---|---|
| Nano Banana 2 / Pro, Seedream (image) | ~40–150 words, structured | Effectively no token limit (Nano Banana 2 ≈ 131K input tokens). Be specific: subject, composition, action, location, style, camera/lighting. Don't inflate. |
| Seedance (video) | ~120–200 words | Lead with **subject + action**, then camera, then style. Prefer **positive** phrasing (e.g. "natural motion, detailed hands") over long negative lists. Best for scenes/products. |
| Kling 3.0 (video) | **control dial:** ~30–60 (simple), 80–150 (standard), 200–350 (complex multi-shot) | Structure: camera movement + subject/action physics + environment/lighting + texture/detail + audio/emotion. Describe motion over time, not a static frame. |

**Hard ceiling:** any **video** prompt stays **under 2000 characters** regardless of model. Within that ceiling, use the target above instead of maxing out.

## 7) Reference image / storyboard upload flow
When the user uploaded a reference (character sheet, storyboard, shot, style ref, thumbnail) and you need it for generation:
1. `media_upload` to get an upload target / `media_id`.
2. Upload the bytes (PUT) as specified, then `media_confirm`.
3. Pass the returned `media_id` in the generation call's `medias[]` with the correct **role** (resolve roles via `models_explore`; image models typically use an `image`/reference role, video models often use frame roles like `start_image`). When multiple references are used (e.g. character + style), mark which is which.

Never invent a local path as a media value — upload and confirm first, then use the returned id (or a completed prior job id, or an https URL).

## 8) Image generation workflow
1. Write + show the prompt(s) per the mode's reference file.
2. Confirm connection (section 2) and model (section 5).
3. If a reference exists, upload it (section 7).
4. **Run the credit-confirmation step (section 4) and wait for yes.**
5. Call `generate_image` with: resolved model, prompt text, `aspect_ratio` as a **parameter** (e.g. `16:9` for stills/thumbnails, `3:2`/`16:9` for boards), references in `medias[]`, `count` for variants.
6. Show the result (`job_display` for a single result). Offer a refinement pass or the next stage.

## 9) Video generation workflow + Seedance vs Kling pipelines
Base flow:
1. Write + show the video prompt per `references/video-prompt.md` (under 2000 chars, no aspect-ratio terms in the text, model-aware length).
2. Confirm connection and model.
3. Upload references via `media_upload` → confirm; pass with model-correct roles.
4. **Run the credit-confirmation step (section 4) and wait for yes.**
5. Call `generate_video` with: resolved model, prompt, `duration` parameter, `aspect_ratio` parameter (only if a specific frame is wanted), references.
6. Show the result; offer retry, a model switch, or a dialogue/no-dialogue variant.

**Seedance pipeline** (scenes/products, identity continuity):
`Character Sheet → Storyboard → Video Prompt → Seedance`. Optimize the prompt for Seedance (subject+action first, positive phrasing). Pass the character/storyboard frame as the identity/sequence reference. (Seedance is limited for people — prefer Kling for human-centric clips.)

**Kling 3.0 Omni pipeline** (people, dialogue, multi-shot): often skips the single character sheet in favor of **individual shots**:
`Generate standard shots (Production Images) → upload selected shots → Kling-optimized video prompt → Kling output`. Kling generally needs an explicit **start frame** when using a reference identity/Element — supply one of the generated shots, or pick another model. Use Kling's structure (camera + physics + environment + texture + audio) and its native audio/lip-sync for dialogue.

## 10) Aspect ratio, duration & the no-aspect-ratio rule
- **Video prompt text must contain no aspect-ratio language** unless the user explicitly asks. Convey frame shape through the MCP `aspect_ratio` **parameter**.
- **Storyboard / image / thumbnail prompts** may include the ratio in text and should also pass it as the parameter (16:9 default for stills/thumbnails).
- **Duration** for video: set the model's duration parameter; the prompt also states duration in words (e.g. "Create a 12-second cinematic video").

## 11) Reusable identity (Soul / Elements) — optional
For a consistent character across many panels/shots or a bulk set:
- **Reference Element** (`show_reference_elements`, action `create`) — instant, single image, reusable across many generations; works with Nano Banana / Seedream / Kling / Seedance. Embed its placeholder as the tool specifies. Best for "use this exact character across the whole batch."
- **Soul character** (`show_characters`, action `train`) — 5–20 photos, ~10 min, one person, identity-faithful, used with Soul models.
- **Ambiguity guard:** don't auto-train a Soul or auto-create an Element for a generic "make a character" request. Only when the user explicitly wants a reusable identity or supplies multiple photos — otherwise one-off generation. If unsure, ask.

## 12) Asset reuse & dependency
Chain: `Character Sheet → Storyboard → Production Images → Video Prompt → Video`.
- If the user already has an upstream asset (uploaded or made earlier), **offer reuse vs regenerate** before spending credits.
- After each asset, recommend the next logical step.
- The user can start anywhere; offer a helpful upstream asset but proceed with what they have.

## 13) Error handling
| Signal | Response |
|---|---|
| Higgsfield tools absent | Show the not-connected notice (section 3); deliver prompts only. |
| About to generate (any size) | Run section 4; wait for yes. Never skip. |
| User declines at confirmation | Stop; offer fewer items, cheaper model, or prompts-only. |
| Auth / credential error | Tell the user to re-authorize the connector; offer to retry. |
| Generation fails / times out | Keep the shown prompt; report plainly; offer retry or a different model. |
| Low / no credits | Warn before running; suggest fewer items or prompts-only; surface top-up. |
| Model rejects a parameter value | Re-check via `models_explore`; use a supported value (nearest aspect ratio/duration). |
| Reference upload fails | Proceed without the reference (note the lost identity lock) or retry. |
| Kling reference without start frame | Supply a generated shot as the start frame, or switch model. |
