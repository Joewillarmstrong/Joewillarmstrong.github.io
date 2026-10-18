#!/usr/bin/env python3
"""Validate portfolio.json so a bad entry can't break the live site.

Usage:
  python3 scripts/validate.py          # check everything, exit 1 on errors
  python3 scripts/validate.py --next   # print the next free brief id
"""
import json, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMATS = {"Ad", "TV", "Film"}
REQUIRED = ["id", "slug", "format", "title", "client_or_network", "year_released",
            "country", "original_track", "video", "brief_summary", "assigned_publisher",
            "playlist", "tracks", "tags", "date_completed", "disclaimer"]

def load():
    return json.loads((ROOT / "portfolio.json").read_text(encoding="utf-8"))

def check(entries):
    errs, ids, slugs = [], set(), set()
    if not isinstance(entries, list):
        return ["portfolio.json must be a JSON array"]
    for n, e in enumerate(entries):
        tag = e.get("id", f"entry #{n+1}")
        def err(msg): errs.append(f"{tag}: {msg}")
        for k in REQUIRED:
            if k not in e: err(f"missing field '{k}'")
        if errs and any(x.startswith(tag) and "missing" in x for x in errs): continue
        if not re.fullmatch(r"SB-\d{3}", e["id"]): err("id must look like SB-004")
        if e["id"] in ids: err("duplicate id")
        ids.add(e["id"])
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", e["slug"]): err("slug must be lowercase-hyphenated")
        if e["slug"] in slugs: err("duplicate slug")
        slugs.add(e["slug"])
        if e["format"] not in FORMATS: err(f"format must be one of {sorted(FORMATS)}")
        if " – " not in e["title"]: err("title should be 'Client – Spot' (en dash with spaces) so the page can split it")
        if not isinstance(e["year_released"], int): err("year_released must be a number")
        ot = e["original_track"]
        for k in ("artist", "title", "source_url"):
            if not ot.get(k): err(f"original_track.{k} is required")
        if not str(ot.get("source_url", "")).startswith("https://"): err("original_track.source_url must be an https URL")
        v = e["video"]
        if v.get("url") and not re.search(r"(youtu\.be/|v=|embed/|shorts/)[A-Za-z0-9_-]{11}", v["url"]):
            err("video.url must be a YouTube link (or empty for 'coming soon')")
        pl = e["playlist"]
        if pl.get("spotify_url"):
            m = re.fullmatch(r"https://open\.spotify\.com/playlist/(\w+)", pl["spotify_url"])
            if not m: err("playlist.spotify_url is not a Spotify playlist link")
            elif pl.get("embed_url") != f"https://open.spotify.com/embed/playlist/{m.group(1)}":
                err("playlist.embed_url does not match spotify_url")
        tr = e["tracks"]
        if [t.get("position") for t in tr] != list(range(1, len(tr) + 1)): err("track positions must run 1..n in order")
        for t in tr:
            for k in ("artist", "title", "note"):
                if not t.get(k): err(f"track {t.get('position')}: '{k}' is empty")
        if pl.get("track_count") != len(tr): err(f"playlist.track_count ({pl.get('track_count')}) != number of tracks ({len(tr)})")
        try: date.fromisoformat(e["date_completed"])
        except ValueError: err("date_completed must be YYYY-MM-DD")
    return errs

def main():
    try:
        entries = load()
    except json.JSONDecodeError as ex:
        print(f"portfolio.json is not valid JSON: {ex}"); sys.exit(1)
    if "--next" in sys.argv:
        nums = [int(e["id"][3:]) for e in entries if re.fullmatch(r"SB-\d{3}", e.get("id", ""))]
        print(f"SB-{max(nums, default=0) + 1:03d}"); return
    errs = check(entries)
    if errs:
        print("\n".join(f"✗ {x}" for x in errs)); sys.exit(1)
    print(f"✓ portfolio.json OK — {len(entries)} briefs")

if __name__ == "__main__":
    main()
