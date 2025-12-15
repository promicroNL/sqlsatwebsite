# SQLSat Website Agent Notes

## Overview
- This repository hosts the SQLSaturday.com static site built with Jekyll and published via GitHub Pages. Content is generated from Jekyll layouts, data files under `_data`, and markdown sources in `_posts` and the project root.

## Build and Automation
- GitHub Actions runs `.github/workflows/ci.yml` on every push/PR. It checks out the repo, sets `JEKYLL_VERSION=3.8`, and uses the `jekyll/builder` Docker image to run `jekyll build --future`, writing the site to `_site`. The action mounts the repo into `/srv/jekyll` and exposes `_site` for artifacts.【F:.github/workflows/ci.yml†L1-L15】
- Because the workflow mirrors GitHub Pages expectations, any migration should plan to replace this step with the new framework’s build command while preserving PR validation.

## Content Model for Events
- New events require **two primary files**:
  1. A YAML data file in `_data/events` named `SQLSatNNNN.yml` containing event metadata (title, date, modality flags, registration links, maps, sponsors, rooms, social links, etc.). The keys drive how sections render (e.g., schedule, sponsors, rooms, pre-cons, countdown).【F:submitpr.md†L65-L122】
  2. A post in `_posts` named `yyyy-mm-dd-SQLSat-NNNN.markdown` that points to the data file via the `data` frontmatter key and sets title, tags, thumbnail, and layout `event`. File naming controls chronological ordering on the site.【F:documentation/eventpost.md†L11-L75】【F:submitpr.md†L23-L64】
- Optional shortlink HTML files (e.g., `jax.html`, `nyc.html`) in the repository root redirect city slugs to the current event, using the `redirect` layout with a `redirect` URL value.【F:README.md†L12-L12】【F:documentation/redirectfile.md†L8-L20】

## How Jekyll Renders Events
- `_layouts/event.html` pulls `page.data` from the post frontmatter to load `site.data.events[...]`. It then renders sections such as event date/status, modality (virtual/physical/hybrid), capacity, registration CTA, table of contents, optional countdown, social links, and per-section content (location, sponsors, rooms, pre-cons, schedule, speakers, volunteers, contact, downloads). Presence or truthy values of keys in the data file toggle visibility of these sections and links.【F:_layouts/event.html†L1-L200】
- Assets referenced by event data (logos, sponsor images) live in `assets/img/**`. Ensure paths remain valid or update during migration.

## Key Repository Locations
- `_config.yml` defines global Jekyll settings and navigation for the site.
- `_includes/` and `_layouts/` contain reusable HTML/Markdown templates; `event.html` is central for event pages.
- `documentation/` holds user-facing instructions for event posts, data files, and redirect pages to guide contributors.【F:documentation/index.md†L5-L14】
- Root-level `.html` files primarily serve as redirects for specific cities/regions.

## Migration Notes
- Preserve the event data schema from `_data/events` and the coupling with `_posts` when moving to a new framework; this pairing drives routing, ordering, and rendering.
- Replicate the automation that builds previews on PRs; ensure future pipelines install dependencies and run the equivalent of `jekyll build --future` for the new stack.
- Maintain contributor guidance (currently in `documentation/` and `submitpr.md`) so event organizers can continue adding/updating events with minimal friction.
