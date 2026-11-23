#!/usr/bin/env python3
"""
Cinematic Prompt Studio - project_export.py

Turn a folder of generated assets into a clean, professional, reproducible
PROJECT: the standard categorized directory tree, consistent asset names,
metadata/log files, and one (or several, size-split) ZIP packages.

Works for both delivery modes:
  - Claude Desktop  : scaffold/assemble the tree at a local path the user picks.
  - Claude Web      : assemble the tree in the working dir, then ZIP for download.

USAGE
    # 1) Make the empty standard tree
    python project_export.py scaffold "PROJECT_DIR"

    # 2) Package an assembled tree -> metadata + ZIP(s)
    python project_export.py package "PROJECT_DIR" --name "Cyberpunk Detective" \
        --max-zip-mb 500 --meta meta.json

    # Helper: print the correct asset filename for a category + index
    python project_export.py name "Production Images" 7 png   ->  Shot_007.png

STANDARD STRUCTURE (mirrors desktop & ZIP identically)
    Project Name/
    ├── Character Sheets/
    ├── Storyboards/
    ├── Production Images/
    ├── Thumbnails/
    ├── Video Prompts/
    ├── Generated Videos/
    ├── Reference Images/
    └── Project Files/        (metadata, logs, manifest)

NAMING (consistent across every workflow)
    CharacterSheet_001.png  Storyboard_001.png  Shot_001.png  Thumbnail_001.png
    VideoPrompt_001.txt     Video_001.mp4       Reference_001.png
Each generated media asset should sit next to its source prompt as a matching
.txt (e.g. Shot_001.png + Shot_001.txt) so the prompt always travels with it.

--meta meta.json (all keys optional) is supplied by the skill:
    {
      "project_name": "Cyberpunk Detective",
      "created": "2026-06-08",
      "models": {"images": "Nano Banana Pro", "video": "Kling 3.0"},
      "credits_used": 2450,
      "settings": {"aspect_ratio": "16:9", "style": "neo-noir"},
      "prompt_history": [{"asset": "Shot_001.png", "prompt": "..."}],
      "workflow_history": ["Generated character sheet", "Generated 100 shots"],
      "notes": "..."
    }
"""

import argparse
import json
import sys
import zipfile
from datetime import date
from pathlib import Path

CATEGORY_DIRS = [
    "Character Sheets", "Storyboards", "Production Images", "Thumbnails",
    "Video Prompts", "Generated Videos", "Reference Images", "Project Files",
]

# category -> asset filename prefix
PREFIX = {
    "Character Sheets": "CharacterSheet",
    "Storyboards": "Storyboard",
    "Production Images": "Shot",
    "Thumbnails": "Thumbnail",
    "Video Prompts": "VideoPrompt",
    "Generated Videos": "Video",
    "Reference Images": "Reference",
}

META_FILES = {"project_summary.md", "generation_log.md", "asset_manifest.json"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def scaffold(root: Path):
    """Create the full standard tree (idempotent)."""
    for d in CATEGORY_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
    return root


def asset_name(category: str, index: int, ext: str) -> str:
    prefix = PREFIX.get(category, "Asset")
    return f"{prefix}_{int(index):03d}.{ext.lstrip('.')}"


def human_size(n: int) -> str:
    f = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if f < 1024 or unit == "GB":
            return f"{f:.0f} {unit}" if unit == "B" else f"{f:.1f} {unit}"
        f /= 1024


def scan_assets(root: Path):
    """Return {category: [ {file, size, prompt_file}, ... ]} for known categories."""
    out = {}
    for cat in CATEGORY_DIRS:
        if cat == "Project Files":
            continue
        d = root / cat
        if not d.is_dir():
            continue
        rows = []
        for p in sorted(d.iterdir()):
            if not p.is_file() or p.suffix.lower() == ".txt":
                continue  # prompts are linked, not listed as separate assets
            sib = p.with_suffix(".txt")
            rows.append({
                "file": p.name,
                "size": p.stat().st_size,
                "prompt_file": sib.name if sib.exists() else None,
            })
        # also surface standalone prompt files (e.g. Video Prompts/*.txt)
        for p in sorted(d.glob("*.txt")):
            if not (p.with_suffix("") .name and any(r["prompt_file"] == p.name for r in rows)):
                rows.append({"file": p.name, "size": p.stat().st_size, "prompt_file": p.name})
        if rows:
            out[cat] = rows
    return out


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
def write_metadata(root: Path, meta: dict, assets: dict):
    pf = root / "Project Files"
    pf.mkdir(parents=True, exist_ok=True)
    name = meta.get("project_name") or root.name
    created = meta.get("created") or date.today().isoformat()

    total_assets = sum(len(v) for v in assets.values())
    total_bytes = sum(r["size"] for v in assets.values() for r in v)

    # asset_manifest.json
    manifest = {
        "project_name": name,
        "created": created,
        "generated": date.today().isoformat(),
        "models": meta.get("models", {}),
        "credits_used": meta.get("credits_used"),
        "settings": meta.get("settings", {}),
        "totals": {"assets": total_assets, "bytes": total_bytes,
                   "by_category": {k: len(v) for k, v in assets.items()}},
        "assets": assets,
        "prompt_history": meta.get("prompt_history", []),
        "workflow_history": meta.get("workflow_history", []),
        "notes": meta.get("notes", ""),
    }
    (pf / "asset_manifest.json").write_text(json.dumps(manifest, indent=2))

    # project_summary.md
    lines = [f"# {name} — Project Summary", "",
             f"- **Created:** {created}",
             f"- **Packaged:** {date.today().isoformat()}"]
    if meta.get("models"):
        lines.append(f"- **Models:** " + ", ".join(f"{k}: {v}" for k, v in meta["models"].items()))
    if meta.get("credits_used") is not None:
        lines.append(f"- **Credits used:** {meta['credits_used']}")
    if meta.get("settings"):
        lines.append(f"- **Settings:** " + ", ".join(f"{k}: {v}" for k, v in meta["settings"].items()))
    lines += ["", f"**Total assets:** {total_assets}  ({human_size(total_bytes)})", "",
              "| Category | Count |", "|---|---|"]
    for cat in CATEGORY_DIRS:
        if cat in assets:
            lines.append(f"| {cat} | {len(assets[cat])} |")
    if meta.get("notes"):
        lines += ["", "## Notes", meta["notes"]]
    (pf / "project_summary.md").write_text("\n".join(lines) + "\n")

    # generation_log.md
    log = [f"# {name} — Generation Log", "", f"_Packaged {date.today().isoformat()}_", ""]
    wh = meta.get("workflow_history", [])
    if wh:
        log.append("## Workflow history")
        log += [f"{i}. {step}" for i, step in enumerate(wh, 1)]
        log.append("")
    ph = meta.get("prompt_history", [])
    if ph:
        log.append("## Prompt history")
        for entry in ph:
            if isinstance(entry, dict):
                log.append(f"- **{entry.get('asset', '?')}** — {entry.get('prompt', '')}")
            else:
                log.append(f"- {entry}")
        log.append("")
    if not wh and not ph:
        log.append("_No workflow/prompt history supplied; see asset_manifest.json for the asset list._")
    (pf / "generation_log.md").write_text("\n".join(log) + "\n")

    return ["Project Files/asset_manifest.json",
            "Project Files/project_summary.md",
            "Project Files/generation_log.md"]


# ---------------------------------------------------------------------------
# Packaging (with size-based splitting)
# ---------------------------------------------------------------------------
def package(root: Path, name: str, max_mb: float):
    files = [p for p in sorted(root.rglob("*")) if p.is_file()]
    if not files:
        sys.exit("Nothing to package: the project tree is empty.")
    cap = int(max_mb * 1024 * 1024) if max_mb and max_mb > 0 else 0

    # bin-pack whole files (preserve structure); raw size is a safe over-estimate vs compressed
    parts, sizes = [[]], [0]
    for f in files:
        s = f.stat().st_size
        if cap and sizes[-1] and sizes[-1] + s > cap:
            parts.append([]); sizes.append(0)
        parts[-1].append(f); sizes[-1] += s

    base = root.parent
    written = []
    if len(parts) == 1:
        zname = base / f"{name}_Assets.zip"
        _write_zip(zname, parts[0], root)
        written.append(zname)
    else:
        for i, part in enumerate(parts, 1):
            zname = base / f"{name}_Part_{i:02d}.zip"
            _write_zip(zname, part, root)
            written.append(zname)
    return written, parts


def _write_zip(zip_path: Path, files, root: Path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            # arcname keeps the project folder name + category structure
            z.write(f, Path(root.name) / f.relative_to(root))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Cinematic Prompt Studio project export / packaging")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scaffold", help="Create the empty standard project tree")
    s.add_argument("dir")

    n = sub.add_parser("name", help="Print the correct asset filename")
    n.add_argument("category"); n.add_argument("index", type=int); n.add_argument("ext")

    p = sub.add_parser("package", help="Write metadata + ZIP(s) for an assembled tree")
    p.add_argument("dir")
    p.add_argument("--name", default=None, help="Project name (defaults to folder name)")
    p.add_argument("--max-zip-mb", type=float, default=500.0, help="Split into parts above this size (0 = never split)")
    p.add_argument("--meta", default=None, help="Path to meta.json (optional)")
    p.add_argument("--no-zip", action="store_true", help="Only write metadata, skip zipping")

    args = ap.parse_args()

    if args.cmd == "scaffold":
        root = scaffold(Path(args.dir))
        print(f"Scaffolded project tree at: {root}/")
        for d in CATEGORY_DIRS:
            print(f"  - {d}/")
        return

    if args.cmd == "name":
        print(asset_name(args.category, args.index, args.ext))
        return

    if args.cmd == "package":
        root = Path(args.dir)
        if not root.is_dir():
            sys.exit(f"Not a directory: {root}")
        name = args.name or root.name
        meta = {}
        if args.meta:
            meta = json.loads(Path(args.meta).read_text())
        if not meta.get("project_name"):
            meta["project_name"] = name

        assets = scan_assets(root)
        meta_files = write_metadata(root, meta, assets)
        total = sum(len(v) for v in assets.values())
        print(f"Project: {name}")
        print(f"  Assets: {total} across {len(assets)} categor(y/ies)")
        for mf in meta_files:
            print(f"  Wrote {mf}")

        if args.no_zip:
            print("  (skipped zipping: --no-zip)")
            return

        written, parts = package(root, name, args.max_zip_mb)
        if len(written) == 1:
            z = written[0]
            print(f"  Packaged -> {z.name}  ({human_size(z.stat().st_size)})")
        else:
            print(f"  Size split into {len(written)} parts (cap {args.max_zip_mb} MB):")
            for z, part in zip(written, parts):
                print(f"    {z.name}  ({human_size(z.stat().st_size)}, {len(part)} files)")


if __name__ == "__main__":
    main()
