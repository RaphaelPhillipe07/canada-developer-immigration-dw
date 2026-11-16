# Guia Canadá — Atlas Editorial design system

## Design rationale and inspiration

Researched 15 November 2026 before proposing changes. This is an original direction for an educational data atlas, with the approved Atlas Bento identity retained.

- [Wise Design](https://wise.design/): reference for confident typography, generous page rhythm, purposeful navigation and friendly consumer experience. Borrow the clarity, not Wise's branding.
- [Datawrapper — 10 ways to use fewer colors](https://www.datawrapper.de/blog/10-ways-to-use-fewer-colors-in-your-data-visualizations): emphasize a few meaningful categories; use direct labels so a projector audience understands the evidence without hover. Use subdued comparator marks and a consistent highlight.
- [Canada.ca — Canadian identity](https://www.canada.ca/en/heritage-canadian-identity.html): geographic and national identity belongs in map and small flag contexts; avoid using flags as data encodings.

## Core experience

Homepage → Why → Sources → Explorer → Comparison → 10 analytical slides → methodology. One primary homepage CTA: Conheça o projeto. Keep routes, approved wording, data, units and periods in src/data.ts. Each slide must have a full question, direct answer, supporting evidence, smaller methodological note, and source/reference period. Missing salaries always say Sem dado.

## Tokens

| Token | Value | Role |
| --- | --- | --- |
| canvas | #F5F1E9 | Warm cream page |
| surface | #FFFCF7 | Cards and controls |
| surface-muted | #ECE5D9 | Secondary blocks |
| ink | #212C28 | Main text |
| ink-muted | #58635D | Secondary text |
| primary | #B3343F | Canadian crimson CTA and data highlight |
| primary-dark | #882631 | Hover |
| primary-soft | #F6E4DE | Answer surface and active tabs |
| forest | #193F35 | Map backdrop and editorial contrast |
| border | #DCD9CE | Subtle separators |
| data-neutral | #AAB8AF | Comparator marks |
| data-secondary | #4B796A | Second comparison series |
| data-periods | #C9D7CB, #91AE9D, #5D8A75, #DFA99D, #AF3340 | Chronological categories |

Typography: Bricolage Grotesque 600–800 for titles, large answer and numeric highlights; Instrument Sans 400–700 for body and UI. Desktop hero 72–84px; chapter title 48–60px; slide question 36–44px; answer 27–34px; chart labels 15–17px; body 17–18px; metadata 13–14px. Do not use tiny uppercase beyond short section labels. Tabular numerals for metrics.

Spacing scale 4/8/12/16/24/32/48/64px. Main width 1280px. Desktop gutter 40px, mobile 20px. Cards radius 20–28px; inputs 10px; badges 999px. One subtle elevated card shadow; no blanket shadow on every nested panel.

## Page composition

### Homepage

A slim cream nav with leaf brand and pill active section. Hero is a deliberate 55/45 bento: left cream editorial headline, supporting paragraph and single red CTA; right Canadian landscape photograph in large rounded crop. Overlay one salary fact card, plus a compact geographic outline or three-metric strip anchored below; no extra primary buttons. Under hero include restrained 13 jurisdições / 3 indicadores / 10 consultas labels as scope facts (not invented results). Footer carries IFAL credit.

### Guided chapters

Use explicit numbered progress 01 Projeto / 02 Dados / 03 Explorar / 04 Comparar / 05 Consultas. Three source/intent cards use strong icon boxes, clear titles, realistic whitespace, and a small source/period footer. Every chapter has persistent back/next navigation. No long scrolling document replacing guided flow.

### Explorer

Main left area is a real geographic outline of Canada's 13 provinces/territories. Fill muted sequential cream/red scale; null values use diagonal hatch and text. Selected region gets thick dark boundary plus visible selected-state badge. Map backdrop warm cream, with a dark forest legend/title band or dark forest inset for visual contrast. Do not draw fake geographic polygons from memory. Use verified GeoJSON/SVG and attribution. Keep schematic tile map as fallback only, explicitly labeled.

Metric tabs as segmented controls with icons, 44px targets and selected background. Right area selected province card shows a small actual provincial flag, name, code, metric values and comparison action. Ranking below/alongside has direct values; selected ranking row and map synchronize. Users can also select all regions from keyboard-accessible list; map cannot be the sole control.

### Comparison

Two symmetrical province cards with small flag and province name, aligned selectors and matching row order. Direct metric values plus small aligned comparison bars. Selected colors crimson vs forest. Never imply housing is currency: use percent, and state lower housing burden is favorable.

### Analytical slides

Question row: Consulta 01 de 10 chip + complete question, max two/three lines. Answer panel immediately below, pale-rose background, crimson left rail, visible Resposta label and large dark answer. This avoids a dominant red slab overpowering all charts.

Evidence is the largest body area, with chart left ~72% and compact methodology/source aside ~28%. Chart title + explicit unit. Asides use a thin left border, no heavy nested box. Never duplicate source in two places. Bottom controls previous + direct slide numbers + next, active slide crimson, shortcut hint optional. Fullscreen isolates deck.

Preferred slide evidence:
1. Horizontal salary ranking, all nine published values labeled CAD/h.
2. Stacked arrival chart plus top-three total/2011–2021 evidence; named periods visibly keyed.
3. Descending horizontal housing ranking with direct percentages, all jurisdictions preserved.
4–7. Scatter plot with reference median lines, highlighted qualifying province codes and visible compact table of exact values. Do not replace all these relational charts with identical dense tables. Full table available as accessible fallback/toggle.
8. Two groups in aligned bars or table for salary and housing, coverage shown explicitly. Distinct units stay separate.
9. Score ranking 0–100, first two highlighted, direct values.
10. Four-row missing-salary table with clear Sem dado pill and census metrics, units in headers.

## Charts and motion

Use locally bundled Recharts (React/SVG) or locally installed Chart.js; remove remote runtime CDN dependence. Keep src/charts.tsx as integration layer and data in src/data.ts. Tooltip supplements direct labels. Chart fallback table remains accessible, stable and available offline.

Motion uses installed motion package. Route/slide enter: opacity 0→1, y 10→0 in 220ms, no exit delay. Buttons: 140ms color and translateY(-1px), press scale .98. Metric/map transitions 240ms; chart draw 400ms once per data change. Animated progress line 220ms. Do not animate every table row or run decorative loops. Respect prefers-reduced-motion: remove positional animation and disable chart animation. Use transitions on transform/opacity/color, never transition: all.

## Acceptance review

- 1440×900 and fullscreen 1280×720: no truncated question/answer, controls reachable, evidence labels readable. Compact mode may reduce padding, not hide meaning.
- 390px mobile: one column, full-width controls, table scroll within table container only.
- All ten questions distinct and unchanged; all ten answers visible without interaction.
- Tab traversal, active state, focus outline, arrow keys, fullscreen and Escape tested.
- No hover-only names/units/value dependencies. Color never sole selected/qualifying signal.
- Missing map/flag assets degrade to province abbreviation and region list.
- Browser review after first implementation and a second review after corrections.
