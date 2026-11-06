# Prompt: MERU-branded HTML artifact for the US aesthetics demand read

Paste everything below the line into a new Claude session, with `artifact_data.json`, `summary.md`, and `assets/meru_logo_green.png` and `assets/meru_logo_white.png` attached or in the working directory.

---

Build a single-file, MERU-branded HTML artifact that presents the results of our one-time read on US aesthetics demand (Q1 2019 to Q3 2026). The audience is MERU colleagues and a client-facing reader who has not seen the workbook. The question the page answers: **is ADCS's aesthetics weakness the market or the company?**

Use the Artifact tool. Load the `artifact-design` skill and the `dataviz` skill before writing any code. Use the `meru-brand-standards` skill for brand values, with the notes below.

## Inputs

- `artifact_data.json` holds everything the page needs. Embed it inline in the HTML as a JS object. Do not fetch it at runtime. Top-level keys: `index` (31 quarters), `price_vs_volume`, `events`, `commentary` (143 tagged quotes), `headline`.
- `index` fields: `tox_full_index`, `tox_AE_index`, `tox_full_yoy_pct`, `tox_AE_yoy_pct`, `tox_full_usd`, `tox_AE_usd`, the matching `fil_*` fields, component dollars (`abbv_us_botox_cosmetic`, `abbv_us_juvederm`, `evolus_toxin_jeuveau`, `evolus_filler_evolysse`, `galderma_us_neuro_est`, `galderma_us_filler_est`), and `estimate_flags`. Index base is the 2019 average = 100. "full" includes Galderma from 2023 and is chained so there is no level break. "AE" is AbbVie plus Evolus only.
- `summary.md` holds the four answers and the caveats. Use its wording and numbers. Do not recompute or restate headline figures differently.
- Logos: `assets/meru_logo_green.png` (light backgrounds, 385x83, aspect 4.64) and `assets/meru_logo_white.png` (dark or green backgrounds). Embed as base64 data URIs.

## Brand

- Font: Segoe UI, with `system-ui, sans-serif` fallback.
- Colors (define as CSS tokens on `:root`): MERU green `#09B582` (primary), charcoal `#414042` (body text), dark green `#03492E`, navy `#08203C`, light green tint `#F0FAF6` (alternating rows), border `#CCCCCC`, muted `#888888`, white.
- Header: green logo on a white band with a thin green rule beneath. Section titles in green bold with a green underline, as in MERU Word documents. Tables: green header row with white bold text, alternating white and `#F0FAF6` rows, light gray borders.
- Footer: "This document is confidential and intended for internal use only" in muted 8pt-equivalent text.
- Writing: no em dashes (use commas, semicolons, or periods), American English, dates as MM/DD/YYYY, negative numbers in parentheses for dollar figures (percent changes may use a minus sign), direct and concise, no preamble.
- Provide a dark mode that is a deliberate set of tokens, not an inversion. Use the navy as the dark surface and the white logo.
- Chart colors: for the two chart series use blue `#2a78d6` (neurotoxin) and orange `#eb6834` (filler). Both passed the dataviz palette validator on a light surface. Re-validate for the dark surface with `scripts/validate_palette.js --mode dark` and adjust steps if needed. Keep MERU green for chrome, headings, and callouts, not for data series.

## Page structure (single scrolling page, readable at 390px width)

1. **Header and title.** Logo, title "US aesthetics demand, 2019 to Q3 2026", one-line subtitle stating the question. Date the page with today's date.
2. **The answer, up top.** One sentence verdict, then four answer cards, one per question in `summary.md` (decline depth, volume or price, is 2026 a real recovery, what ADCS would have done tracking the market). Each card: a big number, a one-line label, one or two short sentences. Numbers come from `headline`.
3. **Main chart.** Interactive line chart of `tox_full_index` and `fil_full_index` by quarter, with AbbVie-plus-Evolus-only as thin dashed companions that a toggle can show or hide. Event markers as vertical lines with short labels, staggered to avoid collisions. Use `events` filtered to the ten that appear in the PNG (COVID closures, reopening, 2021 rebound, rate hikes begin, Daxxify approved, last rate hike, Zepbound, AbbVie loyalty changes, Relfydess approvals, Evolysse launch); the full list goes in the table in section 7. Crosshair with a tooltip showing both indices, YoY growth, the dollar composite, and `estimate_flags` for the hovered quarter. Legend always present, direct labels on the last points. A "view as table" toggle.
4. **YoY growth view.** Same quarters, YoY percent for both categories, as two small multiples or one chart with a zero line. Shade Q1 2025 to Q4 2025 lightly. Do not use a dual axis anywhere.
5. **Who moved the market.** A grouped bar or small-multiple view of 2025 versus 2024 by company and category: AbbVie US Botox Cosmetic (down 10.6%), Evolus Jeuveau (up 3.0%), Galderma US neuromodulators (estimated, up 7.4%); AbbVie US Juvederm (down 17.9%), Galderma US fillers (estimated, up 2.1%). Show the share-shift story: the market fell about 5 to 6% while AbbVie fell far more. Mark every Galderma bar as an estimate with a hatched fill (texture, not color alone).
6. **Price versus volume.** A compact quarter-by-quarter strip for each category from `price_vs_volume`, one cell per quarter colored by call (mostly volume, price or promotions, share shift, inventory timing) with a legend and a confidence marker (high, medium, low as solid, thinner, or dotted outline). Clicking or tapping a cell opens its rationale and the matching quotes from `commentary` (same quarter, same category) with source links.
7. **Event log.** Table of all `events` with date, event, type, and evidence. Flag the rows marked "public record, not re-verified" with a visible tag.
8. **ADCS counterfactual.** A small calculator: input ADCS 2024 aesthetics revenue (default 100), toxin share of mix (default 74%), and output the market-tracking 2025 value and 2026 year-to-date versus 2025 and versus 2024. Use these market changes: toxin (5.3%) and filler (6.0%) for 2025 versus 2024; toxin +8.6% and filler +4.0% for 2026 YTD versus 2025 YTD; toxin +0.2% and filler (4.9%) for 2026 YTD versus 2024 YTD. State plainly that ADCS actuals were not available, so this is a benchmark to compare against, not a forecast. Persist nothing; no storage needed.
9. **Caveats and method.** The four required caveats verbatim in substance: manufacturer revenue is sell-in to practices, not patient treatments; single-company reads are distorted by share shifts (AbbVie losing share, Galderma gaining); US category splits are partly estimated; Merz and other private players are excluded. Then a short method list: AbbVie Q2 2020 full-quarter estimate, Galderma US split method, Galderma absent before 2023 and the chained index, Evolus international share, Revance and BeautyHealth not pulled, event dates not re-verified. Link to the sources in the workbook by filing name.
10. **Footer** with the confidentiality line.

## Behavior and quality bar

- No external libraries beyond what is allowed for artifacts; prefer inline SVG with small hand-written JS. If you load a charting library, pin an exact version from cdnjs and justify it.
- Hover layer on every chart and per-mark tooltips on bars and cells; keyboard focusable marks; visible focus rings; `prefers-reduced-motion` respected.
- Every estimated value is visibly marked as an estimate where it appears, including in tooltips. A reader should never mistake a Galderma US number for a reported figure.
- Text wears text tokens, never the series color. At least 4.5:1 contrast for body text in both themes.
- Layout: 16px side gutters at phone width, no horizontal page scroll, charts reflow, tables scroll inside their own container.
- Keep the page under about 1.5 MB. The JSON is about 100 KB; the commentary quotes are the bulk.
- After building, render the page at 1280px and 390px, in light and dark, and look at it for label collisions and overflow before publishing. Fix what you find.
- Publish privately. Do not add sharing or capabilities. Give me the link and a three-line description of what is on the page.

## Do not

- Do not use em dashes anywhere, including in alt text, tooltips, and code comments that render on the page.
- Do not restate the numbers differently from `summary.md` or `headline`. If a number needs to change, tell me why instead of editing it silently.
- Do not present the index as patient demand. Say "manufacturer sell-in" wherever a reader could otherwise assume treatments.
- Do not add findings that are not in the data. If a section cannot be built from `artifact_data.json`, say so and leave it out.
