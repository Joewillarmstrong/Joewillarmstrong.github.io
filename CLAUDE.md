# Joe Armstrong — Sync Briefs (portfolio site)

Static site shared with music publishers and music supervisors. No build step, no dependencies.

- `index.html` — the whole front end (HTML, CSS, JS). Loads `portfolio.json` at runtime.
- `portfolio.json` — one entry per brief; this is the content. Shown in id order, oldest (SB-001) first.
- `templates/brief.template.json` — skeleton for a new entry.
- `scripts/validate.py` — schema/consistency check. `--next` prints the next free id.
- `scripts/serve.sh` — validates, then previews at http://localhost:8000.

## Adding a brief
1. `python3 scripts/validate.py --next` for the id.
2. Copy the template into `portfolio.json` (append to the array) and fill it in.
3. Run `python3 scripts/validate.py` — it must pass before anything is published.
4. Preview with `scripts/serve.sh` and open the case study.

## Conventions
- `title` is `Client – Spot` with a spaced en dash; the page splits on it.
- `format` is `Ad`, `TV` or `Film`. `video.url` may be empty (shows "Video coming soon").
- Pitches come from ONE assigned publisher's catalogue; keep `assigned_publisher` accurate.
- Keep the disclaimer on every entry: practice briefs, not affiliated with the original productions.
- Don't rename ids or slugs once shared; `#SB-00X` links are deep links.
- Australian spelling (en-AU).
