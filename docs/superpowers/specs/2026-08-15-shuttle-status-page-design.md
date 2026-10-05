# Shuttle Status Page — Design

Date: 2026-08-15
Status: Approved for implementation (autonomous session; user review happens on the PR)

## Goal

A public page showing the status of each of the three wafer.space shuttles
(GF180MCU Run 1, Run 2, Run 3). Each shuttle displays a series of milestone
"stops", with a small animated rocket flying between the last completed stop
and the next upcoming one.

Requested stops (per shuttle, where applicable):

* Early Bird Deadline
* Final Order Date
* GDS In Date
* GF Mask Manufacturing
* GF Wafer Manufacturing
* Dicing & Sorting
* Bare Dies Shipped
* Chip on Board Packaging
* Chip on Board Packaged Shipped

## Approaches considered

1. **Hardcode stops in the page front matter.** Simple, but duplicates dates
   already stored in `_data/runs.yml`; the two would drift.
2. **Extend `_data/runs.yml` with a `stops:` list per run.** Single source of
   truth. Existing consumers (`_includes/components/countdown.html`,
   `_includes/pricing-2col-slot.html`) access runs by explicit key or filter on
   `status == 'active' and featured`, so adding new keys and a third run is
   verified safe. **← Chosen.**
3. **A new `_data/shuttle_status.yml`.** Keeps `runs.yml` untouched but splits
   shuttle facts across two files.

## Data model

Each run in `_data/runs.yml` gains a `stops:` list:

```yaml
stops:
  - title: "Early Bird Deadline"
    date: "2026-04-30"            # optional, ISO 8601, machine-readable
    display_date: "30 April 2026" # free text shown to visitors ("TBD", "Est. …")
    status: "done"                # optional: done | current | pending
```

* Explicit `status` always wins. If absent, the template falls back to
  comparing `date` against build time (`site.time`). Explicit status is the
  primary mechanism because estimated dates drift from reality (Run 1's
  `timeline:` in runs.yml said dies ship 28 April 2026; the news posts show
  wafers only arrived 27 May 2026).
* Run 3 was announced upstream while this feature was in progress (campaign
  opened 1 August 2026), so its `stops:` use the real announced dates. Hard
  deadlines carry machine-readable dates; manufacturing stages are
  display-only estimates so a passed estimate never auto-flips to done.
* Run 1 omits the "Early Bird Deadline" stop — Run 1 had no early bird
  pricing, and inventing a date would be fabrication.
* The existing `timeline:` keys are left untouched for compatibility.

## Page

New `status.html` at the repository root (URL `/status.html`), following the
`faq.html` pattern exactly: `layout: default` front matter, then
`{% include layouts/nav/nav.html %}`, `{% include layouts/header/page-title.html %}`,
then page sections.

* Three shuttle cards: `col-lg-4` each on desktop, stacked on mobile.
* Per shuttle: name, a derived status badge, and a vertical timeline of stops.
  * Badge: all stops done → "Delivered"; Final Order Date stop done →
    "In Flight"; active run still taking orders → "Boarding"; anything else →
    "Coming Soon".
* Each stop: a dot on a vertical rail, title, and `display_date`. Done stops
  get a filled dot with a checkmark; the first not-done stop gets a highlighted
  "current" treatment.
* A "Status" entry is added to `_data/navigation.yml`.

## Rocket

* Inline SVG rocket (self-contained, themeable, no emoji font variance),
  rendered by Liquid into the connector segment between the last done stop and
  the first not-done stop:
  * No stops done → rocket sits at the launch pad above the first stop.
  * All stops done → rocket shown "landed" at the final stop, flame off.
* Animation is pure CSS (no JS): a keyframe animation floats the rocket up and
  down along its connector segment, plus a flickering exhaust flame.
  `prefers-reduced-motion: reduce` disables both.
* Statuses are computed at build time. This is acceptable because statuses are
  editorially controlled in `runs.yml` and the site rebuilds on every content
  change.

## Styling

Added to `assets/css/custom.css` (the established site-override stylesheet) in
its own commented section, matching the file's existing structure. Colors use
the theme's existing palette classes where possible and degrade sensibly in
dark mode.

## Testing / verification

* `jekyll build` passes (baseline verified before changes).
* Rendered page screenshot-verified with Playwright (desktop + mobile widths).
* The `docs/` directory is added to Jekyll's `exclude:` list so this spec does
  not become a live page on the site (where muffet would link-check it).

## Data accuracy notes (for review)

* Run 1 "Chip on Board Packaged Shipped" is marked *current* (in progress),
  not done: the last verifiable public info (news post of 3 June 2026) says
  CoB packaging was still being worked through. Crowd Supply's updates page
  403-blocks bots, so completion could not be verified. Correct in
  `_data/runs.yml` if this has since finished.
* Run 2 mask/wafer manufacturing dates are estimates derived from the
  submission deadline (extended to 14 July 2026) plus the ~12-week fab time
  observed for Run 1, landing on the published 16 October 2026 delivery
  estimate.
* Run 3 deadline stops use the announced dates (early bird 30 September 2026,
  orders close 9 December 2026, GDS in 16 December 2026); its manufacturing
  stages are estimates anchored to the published 16 April 2027 delivery.
